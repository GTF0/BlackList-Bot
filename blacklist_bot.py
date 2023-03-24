import discord
from discord.ext import commands
import random
import asyncio



# Replace ENTER_GUILD_ID_HERE with the actual ID of the guild
guild_id = ENTER_GUILD_ID_HERE.

# Replace blacklisted_user_ids with a list of the user IDs that you want to blacklist
blacklisted_user_ids = [1016407027221807194, 1049127730505064549, 1053020429750632559]

# Replace 123 with a list of the user IDs of the users who are allowed to use the blacklist command. Administrators are allowed to use this command by default.
admin_ids = [123]

# Enable all intents
intents = discord.Intents.all()

bot = commands.bot(command_prefix='.', intents=intents, help_command = None)


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))


@bot.command() ## lists all commands the bot has. 
async def cmds(ctx):
  # Create a list of all the commands
  commands = []
  for command in bot.commands:
    commands.append(f"**{command.name}**: {command.help}")

  # Divide the commands into pages of 10 commands each
  pages = [commands[i:i+10] for i in range(0, len(commands), 10)]

  # Set the initial page
  page = 0

  # Create the embed message
  embed = discord.Embed(title="Commands",
                        description="\n".join(pages[page]),
                        color=0x00ff00)

  # Send the embed message
  message = await ctx.send(embed=embed)

  # Add the emoji reactions
  await message.add_reaction("⏪")
  await message.add_reaction("⏩")

  # Wait for a reaction
  def check(reaction, user):
    return user == ctx.author and str(reaction.emoji) in ["⏪", "⏩"]

  while True:
    try:
      reaction, user = await bot.wait_for("reaction_add", check=check, timeout=60)
    except asyncio.TimeoutError:
      # Remove the emoji reactions after 60 seconds
      await message.clear_reactions()
      break
    else:
      # Update the page based on the reaction
      if str(reaction.emoji) == "⏪":
        page = max(page-1, 0)
      elif str(reaction.emoji) == "⏩":
        page = min(page+1, len(pages)-1)

      # Update the embed message
      embed = discord.Embed(title="Commands",
                            description="\n".join(pages[page]),
                            color=0x00ff00)
      embed.set_footer(text=f"Page {page+1}/{len(pages)}")
      await message.edit(embed=embed)
@bot.event
async def on_member_join(member):
  print("New member!")
  if member.id in blacklisted_user_ids:
    print("Found the target!")
    try:
      print("Sending DM to the target...")
      blacklist_msg = db.get("blacklist_msg")
      if blacklist_msg:
        await member.send(blacklist_msg)
      else:
        print("No blacklist message set.")
        
      print("Banning the target!")
      await member.ban(reason="blacklisted user!")

      # Send message to the channel, mentioning the user
      guild = bot.get_guild(guild_id)
      if guild:
        blacklist_channel_id = db.get("blacklist_channel")
        if blacklist_channel_id:
          channel = guild.get_channel(int(blacklist_channel_id))
          if channel:
            await channel.send(f"{member.mention} tried to join while being blacklisted!")
          else:
            print("Couldn't get the channel.")
        else:
          print("No blacklist channel set.")
      else:
        print("Couldn't get the guild.")
    except:
      print("Couldn't ban the target :(")
  else:
    print("New member isn't the target...")

@bot.command()
async def blacklisted(ctx):
  guild = bot.get_guild(guild_id)
  if guild:
    blacklisted_users = []
    for user_id in blacklisted_user_ids:
      user = guild.get_member(user_id)
      if user:
        blacklisted_users.append(user.mention)
      else:
        blacklisted_users.append(str(user_id))

    # Create an embed with the list of blacklisted users and IDs
    embed = discord.Embed(title="Blacklisted Users",
                          description=", ".join(blacklisted_users))
    embed.set_footer(
      text="Total Blacklisted Users: {}".format(len(blacklisted_users)))

    # Send the embed to the channel
    await ctx.send(embed=embed)
  else:
    await ctx.send("Couldn't get the guild.")

@bot.command()
async def banblacklisted(ctx):
  # Check if the user has the required permissions or is one of the specified users
  if ctx.author.guild_permissions.ban_members or ctx.author.id in [1054305659727908964, 1054513153662255114]:
    # Get a list of all the members of the server
    members = ctx.guild.members

    # Filter the members to get a list of blacklisted members
    blacklisted_members = [member for member in members if member.id in blacklisted_user_ids]

    # Ban each blacklisted member
    for member in blacklisted_members:
      try:
        await member.ban(reason="blacklisted")
      except:
        print(f"Couldn't ban user with ID {member.id} :(")

    # Create the embed message
    embed = discord.Embed(title="Blacklisted Members Ban",
                          description=f"{len(blacklisted_members)} blacklisted members banned.",
                          color=0xff0000)

    # Send the embed message in the chat
    await ctx.send(embed=embed)
  else:
    # Send a message to the user if they don't have the required permissions
    await ctx.send("You can't use this command, retard")

@bot.command()
async def detectb(ctx):
  # Check if the user has the required permissions
  if ctx.author.guild_permissions.manage_guild:
    # Get a list of all the members of the server
    members = ctx.guild.members

    # Filter the members to get a list of blacklisted members
    blacklisted_members = [member for member in members if member.id in blacklisted_user_ids]

    # Create the embed message
    embed = discord.Embed(title="Blacklisted Members Detection",
                          description=f"{len(blacklisted_members)} blacklisted members detected.",
                          color=0xff0000)

    # Add a field for each blacklisted member
    for member in blacklisted_members:
      embed.add_field(name=member.name, value=member.id, inline=False)

    # Send the embed message in the chat
    await ctx.send(embed=embed)
  else:
    # Send a message to the user if they don't have the required permissions
    await ctx.send("You can't use this command, retard")

@bot.command()
@commands.has_permissions(administrator=True)
async def setblacklistdm(ctx, value: bool):
    """Sets whether or not blacklisted users should receive a DM."""
    global send_dm
    send_dm = value
    await ctx.send(f"Blacklisted users will{' ' if send_dm else ' not '}receive a DM.")

# Clears the entire blacklist.
@bot.command()
@commands.has_permissions(administrator=True)
async def clearblacklist(ctx):
    global blacklisted_user_ids
    blacklisted_user_ids = []
    await ctx.send("The blacklist has been cleared.")

# Displays the total number of blacklisted users.
@bot.command()
async def blacklistcount(ctx):
    global blacklisted_user_ids
    count = len(blacklisted_user_ids)
    await ctx.send(f"The total number of blacklisted users is {count}.")

# Displays a list of all admin users.
@bot.command()
async def viewadmins(ctx):
    admins = []
    for id in admin_ids:
        user = await bot.fetch_user(id)
        admins.append(user.name)
    await ctx.send(f"The admins for this bot are: {', '.join(admins)}")

# Displays a help message explaining how to use the blacklist commands.
@bot.command()
async def help(ctx):
    help_message = """
The following commands are available for the blacklist:
- .blacklist <user_id>: Adds the specified user to the blacklist.
- .unblacklist <user_id>: Removes the specified user from the blacklist.
- .setblacklistchannel <channel_id>: Sets the channel where notifications of blacklisted users are sent. (Admin only)
- .setblacklistmsg <message>: Sets the message that blacklisted users receive when they try to join the server. (Admin only)
- .setblacklistdm <True/False>: Sets whether or not blacklisted users should receive a DM
- .blacklistchannel: Displays the channel where notifications of blacklisted users are sent.
- .blacklistmsg: Displays the message that blacklisted users receive when they try to join the server.
- .blacklistcount: Displays the total number of blacklisted users.
- .viewadmins: Displays a list of all admin users.
- .blacklisthelp: Displays this help message.
- .addadmin <user_id>: Adds the specified user to the list of admins who can use the blacklist command.
- .removeadmin <user_id>: Removes the specified user from the list of admins who can use the blacklist command.
- .clearblacklist: Clears the entire blacklist.
    """
    await ctx.send(help_message)

@bot.command()
async def blacklist(ctx, user: discord.Member = None):
  if user is None:
    await ctx.send("mention the user you want to blacklist, retard")
    return

  # Check if the user has the required permissions or is one of the specified users
  if ctx.author.id in [1054305659727908964, 1054513153662255114]: # you can configure the set of permissions by yourself. This is not difficult.
    # Send a Direct Message to the user
    try:
      await user.send(
        "Get the fuck out of here you stupid. Lmao"
      )
    except:
      print(f"Couldn't send message to user with ID {user.id} :(")

    # Add the user ID to the blacklist
    blacklisted_user_ids.append(user.id)

    # Ban the user
    try:
      print(f"Banning user with ID {user.id}")
      await user.ban(reason="blacklisted")
      await ctx.send(
        f"{user.name} has been BANNED & blacklisted. fuck this guy fr.")
    except:
      print(f"Couldn't ban user with ID {user.id} :(")
  else:
    # Send a message to the user if they don't have the required permissions
    await ctx.send("you cant use that, retard.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setblacklistchannel(ctx, channel_id: int):
    """Sets the channel where notifications of blacklisted users are sent. (Admin only)"""
    channel = bot.get_channel(channel_id)
    if not channel:
        return await ctx.send("Invalid channel ID. Please try again.")

    # Store the channel ID in a database or file
    # This code assumes that you have already set up a database or file storage for your bot
    # Replace `your_database` with the name of your database or file storage
    # Replace `blacklist_channel` with the name of the table or key where you want to store the channel ID
    # This code uses SQLite as an example, but you can use any database or file storage that you prefer
    conn = sqlite3.connect('your_database.db')
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS blacklist_channel (server_id INTEGER PRIMARY KEY, channel_id INTEGER)")
    c.execute("INSERT OR REPLACE INTO blacklist_channel (server_id, channel_id) VALUES (?, ?)", (ctx.guild.id, channel_id))
    conn.commit()
    conn.close()

    await ctx.send(f"Blacklist notifications will be sent to {channel.mention} from now on.")

@bot.command()
@commands.has_permissions(administrator=True)
async def addadmin(ctx, user_id:int):
    if str(user_id) in admin_ids:
        await ctx.send("User is already an admin.")
    else:
        admin_ids.append(str(user_id))
        await ctx.send("User has been added as an admin.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setblacklistmsg(ctx, *, message):
    """Sets the message that blacklisted users receive when they try to join the server."""
    guild_id = ctx.guild.id
    db.execute("UPDATE guild_settings SET blacklist_message = ? WHERE guild_id = ?", (message, guild_id))
    conn.commit()
    await ctx.send(f"Blacklist message set to:\n{message}")

@bot.command()
async def blacklistchannel(ctx):
    """Displays the channel where notifications of blacklisted users are sent."""
    if ctx.author.id not in admin_ids:
        return await ctx.send("You are not authorized to use this command.")
    channel_id = await get_blacklist_channel(ctx.guild.id)
    if channel_id is None:
        return await ctx.send("Blacklist channel has not been set.")
    channel = bot.get_channel(channel_id)
    if channel is None:
        return await ctx.send("Blacklist channel not found.")
    await ctx.send(f"Blacklist channel is set to: {channel.mention}")

@bot.command()
@commands.has_permissions(administrator=True)
async def unblacklist(ctx, user_id: int):
    """
    Removes the specified user from the blacklist.
    """
    if user_id in blacklisted_user_ids:
        blacklisted_user_ids.remove(user_id)
        await ctx.send(f"{user_id} has been removed from the blacklist.")
    else:
        await ctx.send(f"{user_id} is not in the blacklist.")

@bot.command()
async def blacklistmsg(ctx):
    """Displays the message that blacklisted users receive when they try to join the server."""
    # Check if user is admin
    if ctx.author.id not in admin_ids:
        await ctx.send("You do not have permission to use this command.")
        return

    # Get the current blacklist message
    current_msg = db.get("blacklist_message")
    if current_msg is None:
        await ctx.send("There is no current blacklist message.")
    else:
        await ctx.send(f"The current blacklist message is: {current_msg}")
@bot.command()
@commands.has_permissions(administrator=True)
async def removeadmin(ctx, user_id:int):
    if str(user_id) not in admin_ids:
        await ctx.send("User is not an admin.")
    else:
        admin_ids.remove(str(user_id))
        await ctx.send("User has been removed as an admin.")
bot.run(
  'Inset_your_bot_token_here')