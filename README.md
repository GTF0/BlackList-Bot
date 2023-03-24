# Blacklist Bot

## Overview
Blacklist Bot is a Discord bot designed to help server owners manage blacklisted users. It allows admins to add and remove users from a blacklist, and sends notifications when blacklisted users try to join the server.

## Features
* Blacklist commands: Admins can add and remove users from a blacklist using simple commands.
* Notifications: When a blacklisted user tries to join the server, the bot sends a notification to a specified channel and optionally sends a DM to the user.
* Customizable message: Admins can set a custom message to be sent to blacklisted users when they try to join the server.
* Admin management: Only admins specified in the code can use the blacklist commands.
* Help command: Displays a help message explaining how to use the blacklist commands.

## Usage
To use the bot, you must have a Discord server and have the necessary permissions to add a bot to your server.

1. Create a new Discord bot and add it to your server. You can follow these instructions to do this.
2. Copy the contents of `blacklist_bot.py` into a new file in your preferred text editor.
3. Replace the `guild_id` variable with the ID of your server.
4. Replace the `admin_ids` variable with a list of Discord user IDs for your admins.
5. Run the bot using `python3 blacklist_bot.py`.
6. Use the commands listed below to manage the blacklist.

## Commands
* `.blacklist <user_id>`: Adds the specified user to the blacklist. (Admin only)
* `.unblacklist <user_id>`: Removes the specified user from the blacklist. (Admin only)
* `.setblacklistchannel <channel_id>`: Sets the channel where notifications of blacklisted users are sent. (Admin only)
* `.blacklistchannel`: Displays the channel where notifications of blacklisted users are sent.
* `.setblacklistmsg <message>`: Sets the message that blacklisted users receive when they try to join the server. (Admin only)
* `.blacklistmsg`: Displays the message that blacklisted users receive when they try to join the server.
* `.setblacklistdm <True/False>`: Sets whether or not blacklisted users should receive a DM.
* `.clearblacklist`: Clears the entire blacklist.
* `.blacklistcount`: Displays the total number of blacklisted users.
* `.addadmin <user_id>`: Adds the specified user to the list of admins who can use the blacklist command. (Admin only)
* `.removeadmin <user_id>`: Removes the specified user from the list of admins who can use the blacklist command. (Admin only)
* `.viewadmins`: Displays a list of all admin users.
* `.blacklisthelp`: Displays a help message explaining how to use the blacklist commands.

## Overview 

That's it! With this README file and the blacklist_bot.py script, you should be ready to use Blacklist Bot to manage blacklisted users in your Discord server. If you have any questions or run into any issues, feel free to reach out to the bot's creator for help at zozyzop@gmail.com or my discord Nyxaris#0001
