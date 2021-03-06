# -*- coding: utf-8 -*-
import asyncio
import configparser
import random

import discord
from discord.ext import commands
from PIL import Image

import mytype
import scorekeep
from vsimage import multi_imageconcat

bot = commands.Bot(command_prefix="-")

token = "Nzjdslkfjsdklfjsdlfsd.fdsfjksldjxckjvdskf.sdjfkl"

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print(bot.user)
    print("Ready!")


@bot.command(help="assigns your aesthetic")
async def myaesthetic(ctx): 
    await ctx.send(
        "{} your aesthetic is {} {} {}.".format(
            ctx.author.mention, *mytype.whataesthet()
        )
    )


@bot.command(name = 'mytype', help = "assigns your Pokemon type")
async def mytype1(ctx):
    urtype = mytype.whattype()
    if len(urtype) == 3:
        await ctx.send("{} you are {} {} {} type!".format(ctx.author.mention, *urtype))
    else:
        await ctx.send("{} you are {} {} type!".format(ctx.author.mention, *urtype))


@bot.command()
async def myclass(ctx):
    await ctx.send(
        "{}, you are a level {} {} {} with {}.".format(
            ctx.author.mention, random.randint(1, 20), *mytype.whatclass()
        )
    )


@bot.command(help = 'displays your current LeoBets score')
async def myscore(ctx):
    config = configparser.ConfigParser()  # initialize configparser
    config.read("betgame.ini")
    if (
        config["FIGHT"]["fighting"] == "True"
    ):  # check if fight happening currently, won't display score if it is
        await ctx.send("Fight underway, wait until it's over.")
        return
    score = scorekeep.readscore(str(ctx.author.id))  # read score and display
    await ctx.send("Your score is {}".format(score))


@bot.command(help='begins a LeoBets fight')
async def fight(ctx):
    config = configparser.ConfigParser()
    config.read("betgame.ini")
    if (
        config["FIGHT"]["fighting"] == "True"
    ):  # check if fight happening currently, won't display score if it is
        await ctx.send("Fight underway, wait until it's over.")
        return  # Starts fight on command !fight
    scorekeep.fightgame()  # Initialize configparser
    config.read("betgame.ini")

    p1f = config["FIGHT"]["p1f"]  # get variables generated by fightgame() and send fight message to channel
    p2f = config["FIGHT"]["p2f"]

    p1n = config["FIGHT"]["p1n"]
    p2n = config["FIGHT"]["p2n"]

    await ctx.send("The {} is fighting the {}! ({}:{})".format(p1f, p2f, p1n, p2n))

    im1 = Image.open("fight_image/{}.jpg".format(p1f))  # generate fight image and send to channel
    vs = Image.open("fight_image/divider.jpg")
    im2 = Image.open("fight_image/{}.jpg".format(p2f))

    im_list = [im1, vs, im2]
    multi_imageconcat(im_list).save("fightimage.jpg")
    await ctx.send(file=discord.File("fightimage.jpg"))
    await asyncio.sleep(60)  # wait for all bets to be in
    config.read("betgame.ini")  # Reread because changes have been made from bets
    winner = config["FIGHT"]["winner"]  # get winner from config
    await ctx.send("The {} won!".format(winner))
    config.set(
        "FIGHT", "winner", ""
    )  # clear variables from config file, not all of these are
    config.set("FIGHT", "loser", "")  # necessary in this build but they don't hurt
    config.set("FIGHT", "p1f", "")
    config.set("FIGHT", "p2f", "")
    config.set("FIGHT", "p1n", "")
    config.set("FIGHT", "p2n", "")
    config.set("FIGHT", "betters", "")
    config.set("FIGHT", "fighting", "False")  # end fight
    with open("betgame.ini", "w+") as configfile:  # update config file
        config.write(configfile)


@bot.command(help = 'Submits bet during fight in formate !bet {fighter} {bet}')
async def bet(
    ctx, fighter, bet: int
):
    config = configparser.ConfigParser()  # initialize configparser
    config.read("betgame.ini")
    betters = config["FIGHT"][
        "betters"
    ]  # get betters from config and refuse bet if message author
    if str(ctx.author.id) in betters:  # already bet
        await ctx.message.add_reaction("👎")
        await ctx.send("You already bet.")
        return
    if not config.has_option(
        "USERS", str(ctx.author.id)
    ):  # check if author is already stored in config
        await ctx.send(
            "Adding {}...".format(ctx.author.mention)
        )  # if not, add author using readscore()
        scorekeep.readscore(str(ctx.author.id))
    winner = config["FIGHT"]["winner"]  # get winner and loser from config
    loser = config["FIGHT"]["loser"]
    if winner == "":  # if winner empty, no bets
        await ctx.send("Fights done, go home.")
        return
    currentscore = int(
        scorekeep.readscore(str(ctx.author.id))
    )  # get message author current score
    if currentscore <= 0:  # if author broke, give money
        config.set(
            "DEBT", str(ctx.author.id), str(1000 + int(config["DEBT"][str(ctx.author.id)])),
        )
        currentscore = 1000
    if bet > currentscore:  # fail if bet higher than money available
        await ctx.message.add_reaction("👎")
        return
    if bet <= 0:  # fail if bet < 0
        await ctx.message.add_reaction("👎")
        return
    if fighter != winner and fighter != loser:  # fail if fighter not fighting
        await ctx.message.add_reaction("👎")
        return
    await ctx.message.add_reaction(
        "👍"
    )  # confirm succesful bet and add message author to betters
    config.set(
        "FIGHT", "betters", "{} {}".format(config["FIGHT"]["betters"], str(ctx.author.id)),
    )
    with open("betgame.ini", "w+") as configfile:
        config.write(configfile)
    if (
        fighter == winner
    ):  # if bet on winner, add money based on odds, if not lose money
        p1f = config["FIGHT"]["p1f"]
        p1n = int(config["FIGHT"]["p1n"])
        p2n = int(config["FIGHT"]["p2n"])
        if winner == p1f:
            scorekeep.writescore(str(ctx.author.id), currentscore + bet * (p2n / p1n))
        else:
            scorekeep.writescore(str(ctx.author.id), currentscore + bet * (p1n / p2n))
    else:
        scorekeep.writescore(str(ctx.author.id), currentscore - bet)


@bot.command(help = 'Tells author how much money they owe')
async def mydebt(ctx):
    debt = scorekeep.readgeneral(str(ctx.author.id), "DEBT", "betgame.ini")
    await ctx.send("You owe me {} points.".format(debt))


@bot.command(help = "allows you to repay some of the money you owe LeoBot")
async def paydebt(ctx, payment: int):
    config = configparser.ConfigParser()
    config.read("betgame.ini")
    if config["FIGHT"]["fighting"] == "True":
        await ctx.send("Wait for the fight to be over please.")
        return
    debt = int(scorekeep.readgeneral(str(ctx.author.id), "DEBT", "betgame.ini"))
    currentscore = int(scorekeep.readscore(str(ctx.author.id)))
    if payment > currentscore:
        await ctx.message.add_reaction("👎")
        return
    if payment <= 0:
        await ctx.message.add_reaction("👎")
        return
    if payment > debt:
        payment = debt
    newdebt = debt - payment
    newscore = currentscore - payment
    scorekeep.writegeneral(str(ctx.author.id), round(newdebt), "DEBT", "betgame.ini")
    scorekeep.writescore(str(ctx.author.id), newscore)
    if newdebt == 0:
        await ctx.send("We're square now, stay on my good side punk.")
    else:
        await ctx.send("You still owe me {} points.".format(newdebt))


@bot.command(aliases=["lb"])
async def leaderboard(ctx):
    config = configparser.ConfigParser()  # initialize configparser
    config.read("betgame.ini")
    if config["FIGHT"]["fighting"] == "True":  # Won't display if fighting
        await ctx.send("Fight underway, wait until it's over.")
        return
    board = scorekeep.leaderboard()  # get current leaderboard from config
    lbmess = ""  # generate leaderboard message
    for i in range(len(board)):
        tempstr = "{}. {} {}\n".format(len(board) - i, board[i][0], board[i][1])
        lbmess += tempstr
    await ctx.send(lbmess)

bot.run(token)
