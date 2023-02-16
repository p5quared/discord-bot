# :b:MCC Discord :b:ot
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Hello and welcome, _brave souls_,

What lies beyond is the repository which comprises the bot, _"The Sheriff"_ on the BMCC programming club server. This project is really a labor of love started and monitored monitored by yours truly, but maintained by YOU! 

My goal in creating this is to allow you to get a taste of the satisfaction of creating programs and seeing their effect on the world around you. You cannot get this feeling from class and as such this is like no classroom. 
Here there are:
* No Teachers
* No Students
* No Assignments
* No Grades
* No Judgement

Instead, you are the teacher and the student. You will pick your own assignments, and you will grade yourself (figuratively).

I hope that by engaging with this project you will strengthen your problem solving abilities, your ability to read other's code and documentation, and have a better idea of what it takes to be a part of a team of software engineers.

p5quared

## Getting Started

There are a few things you'll need to do to get started with this project before you can code:
1. Create Bot User
2. Setup Your Repo
3. Project Configuration
4. Pushing Your Changes

### Create Bot User
For obvious reasons, we don't want our changes to affect the live version of _The Sheriff_, so we must create our own bot that we can use to test our functions on our own private server.
* Go to the [discord developer portal](https://discord.com/developers/applications) and create a "New Application" and then a "New Bot" from within that Application.
* On the "Bot" page, enable all "Privileged Gateway Intents". 
* On "Oauth2" page, click "Reset Secret" button. This is like your bot's password, and should be treated as such.
* Create a file called ".env" and add ```CLENT_SECRET=[YOUR_TOKEN]``` to save your token (we'll use this later).
* Find the "URL Generator" page and select "Bot" and then "Administrator".
* Whenever you want, you can paste this link into your browser and then you will be able to add the bot to servers where you have permission to do so.
### Setup Your Repo
Because we have a number of people working on a number of different functions, we utilize git to keep things organized. Here's what we will do to get started:

1. Fork this repo.
2. Create a branch named <name_of_feature>
3. Make your changes.
4. Submite a pull request to the development branch.
5. Await review.

### Project Configuration
There are a couple changes we'll make to your code to make things run smoothly.

For the program to run at all, you'll need to be sending your bot's "password" to Discord. To do this, **add your .env file to your project directory.**

If you are testing your bot on a server with other bots, modify your command prefix so that it does not conflict with other bots (if two bots have the same command prefix, both bots will act on every command which clutters chats or affects your testing). 
```python
# This is the line you want to alter.
bot = Bot(command_prefix='<non_conflicting_prefix>', intents=_intents)
```
### :tada:Pushing Your Changes :tada:
Let's say you've created a new function for the bot! To add your changes do the following:
1. Ensure your changes have been committed.
2. Push your commits to your remote repository
3. Open a pull-request on the "next-release" branch.
If everything works according to plan, you're all set! Your changes will be on the next release for _The Sheriff_ and you will be added to the contributors!

#### Note On Changes 
Here are some rules that make things much easier for me to manage things:
* Only work on one command per pull request
	* If you want to do multiple things, follow all the steps, write a pull request, and then restart by making another fork and then write a pull request from **that** fork.
* Be very descriptive in your comments and in your pull-request text.

Read [here](https://blog.ploeh.dk/2015/01/15/10-tips-for-better-pull-requests/) for more tips on pull requests.
