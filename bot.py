from discord.ext import commands
import discord
import json

client = commands.Bot(command_prefix = ".",intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
	print("Bot is online!")

# Ping Command
@client.command
async def ping(ctx):
	ctx.send(f"Pong {round(client.latency*1000)} ms")

# Help Command
@client.command(pass_context=True)
async def help(ctx,*, number=1):
	if number == 1:
		myEmbed = discord.Embed(title="Help", description="The current prefix for me is .", color=discord.Color.green())

		myEmbed.add_field(name=".help", value="Tells you almost all the commands", inline=False)
		myEmbed.add_field(name=".clear", value="Clears a number of messages but only works when you have the Manage Messages permissions. Example: .clear 5. (5 means the number of messages that will be removed including yours)", inline=False)
		myEmbed.set_footer(text="Do .help with a number to switch pages")

	else:
		if number == 2:
			myEmbed = discord.Embed(title="Help Page 2", color=discord.Color.green())

			myEmbed.add_field(name=".ban", value="Bans someone in the server as long as you have ban permissions. Example: .ban @Pankake Reason Here", inline=False)
			myEmbed.add_field(name=".kick", value="Kicks someone in the server as long as you have kick permissions. Example: .kick @Pankake Reason Here)", inline=False)
			myEmbed.add_field(name=".unban", value="Unbans someone in the server as long as you have ban permissions. Example: .unban @Pankake Reason Here", inline=False)
    			
	
	await ctx.send(embed=myEmbed)
	
# Clear Command
@commands.has_permissions(manage_messages = True)
@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

  await ctx.send("Messages have been cleared")

# Kick Command
@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.kick(reason=reason)
  await ctx.send(f"{user} have been kicked sucessfully")

# Unban Command
@commands.has_permissions(ban_members=True)
@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} have been unbanned sucessfully")
    return

# Ban Command
@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"{user} have been bannned sucessfully")

# Reaction Roles
@commands.has_permissions(manage_messages=True)
@commands.has_permissions(manage_roles=True)
@client.command()
async def reactionrole(ctx, emoji, role: discord.Role,*,message):
	myEmbed = discord.Embed(description=message)
	msg = await ctx.send(embed=myEmbed)
	await msg.add_reaction(emoji)

	with open('reactionroles.json') as json_file:
		data = json.load(json_file)

		new_react_role = {
			'role_name':role.name,
			'role_id':role.id,
			'emoji':emoji,
			'message_id':msg.id
		}

		data.append(new_react_role)

	with open('reactionroles.json','w') as j:
		json.dump(data,j,indent=4)

@client.event
async def on_raw_reaction_remove(payload):
	with open('reactionroles.json') as reaction_file:
		data = json.load(reaction_file)
		for x in data:
			if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
				role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

				await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
					

@client.event
async def on_raw_reaction_add(payload):
	if payload.member.bot:
		pass
	else:

		with open('reactionroles.json') as reaction_file:
			data = json.load(reaction_file)
			for x in data:
				if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
					role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

					await payload.member.add_roles(role)


TOKEN = "ODU5MTY5MjM5MDA5MTk4MTIw.YNoxtQ.CVbXrw5MD4iUT1zUVtGTK-_Tk-g"

client.run(TOKEN)