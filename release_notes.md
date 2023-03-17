# v2023.3.16 Release notes

Below are the latest updates in bot version 2023.3.16:


### The following functions have been added:
* groups - Generates groups of users via a react flow
* verify - Allows users to verify their identity via a react flow
* me - Allows users to see their own information
* attendance - Attendance process will be somewhat automated for verified users


### The following functions have been modified:
* helps has been removed in favor of the default "help"


### Release Notes
**Release Contributors**

These are the users who have written some functionality which has been added to the bot for this release:
* Flo03
  * new command: groups

* p5quared
  * new command: verify, me, attendance
  * improved deployment settings and features

  
**All Contributors**

All contributors to BMCC discord bot:
* Flo03
* p5quared

## Upcoming Goals/Tasks
* Field Validaiton
  * None of the for verification fields are validated at this time and could be used to break the bot. (don't get any funny ideas...)
* Server Welcome
  * The bot should be able to welcome new users to the server and provide them with some basic information.
* Refactoring
  * The code is a bit messy and could use some refactoring to make it more readable and maintainable.
  * In particular, the commands are all in one file and implementations could be broken out into separate file(s).
* Testing
  * Our current code coverage is 0%... We should probably fix that.



### Footer
If you would like to join this project to gain experience working with bots, servers, and git, feel free to reach out in the **collaboration** channel in the BMCC discord.
There is an unending list of things that could be implemented and improved which have difficulties ranging from very easy (only a few lines of code or no code)
to challenging (100+ lines and lots of Googling).

[Github Repo](https://github.com/p5quared/discord-bot/)