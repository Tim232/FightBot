# -*- coding: utf-8 -*-

import configparser
import random

def writescore(author, score):                          #Writes score config file under section USERS option author
    config = configparser.ConfigParser()                #initialize configparser
    config.read('betgame.ini')                          #read config
    cutscore = round(score)                             #round score to integer
    config.set('USERS', str(author), str(cutscore))     #set option to cutscore
    with open('betgame.ini', 'w+') as configfile:       #update config file
        config.write(configfile)
        
def writegeneral(author, score, section, file):         #Generalized Writescore
    config = configparser.ConfigParser()                #initialize configparser
    config.read(file)                                   #read config
    config.set(section, str(author), str(score))        #set option to score
    with open(file, 'w+') as configfile:                #update config file
        config.write(configfile)

def readscore(author):                                  #gets score from config file, adds option if not present
    authstr = str(author)                               #casts author to string
    config = configparser.ConfigParser()                #initialize configparser
    config.read('betgame.ini')                          #read config
    if config.has_option('USERS',authstr):              #check if author is an option, if it is read value
        return config['USERS'][author]
    else:                                               #if it isn't, add option and read value    
        config.set('USERS', authstr, '1000')
        config.set('DEBT',authstr,'0')
        with open('betgame.ini', 'w+') as configfile:
            config.write(configfile)
        return readscore(author)
    
def readgeneral(author,section,file):                   #generalized form of readscore, reads from any section and any config
    authstr = str(author)                               #casts author to string
    config = configparser.ConfigParser()                #initialize configparser
    config.read(file)                                   #read config
    if config.has_option(section,authstr):              #check if author is an option, if it is read value
        return config[section][author]
    else:                                               #if it isn't, add option and read value    
        config.set(section, authstr, '0')
        with open(file, 'w+') as configfile:
            config.write(configfile)
        return readgeneral(author,section,file)
    
    
    
    
def leaderboard():                                      #generate list of lists [user,score] users
    config = configparser.ConfigParser()                # in order of score least to greatest
    config.read('betgame.ini')                          #initialize configparser
    userstup = config.items('USERS')                    #get list of tuples (user,score)
    users = [list(elem) for elem in userstup]           #convert to list of lists [user,score]
    for i in range(len(users)):                         #strip user of numbers and #, cast score to int
        users[i][0] = users[i][0].translate({ord(ch): None for ch in '#0123456789'})
        users[i][1] = int(users[i][1])
    users.sort(key = lambda x: x[1])                    #sort by score
    if len(users) > 10:                                 #cut to 10 users
        return users[-10:]
    else:
        return users


def fightgame():                                        #initializes fight variables
    config = configparser.ConfigParser()                #initialize configparser
    config.read('betgame.ini')
    fighters = config.items('FIGHTERS')                 #get fighter tuples (fighter,power) from config
    p1 = random.choice(fighters)                        #choose random different opponents
    p2 = random.choice(fighters)
    while p1 == p2:
        p2 = random.choice(fighters)
    p1f = p1[0]                                         #separate tuples
    p2f = p2[0]
    p1n = p1[1]
    p2n = p2[1]
    config.set('FIGHT', 'p1f', p1f)                     #set config file options to generated variables
    config.set('FIGHT', 'p2f', p2f)
    config.set('FIGHT', 'p1n', p1n)
    config.set('FIGHT', 'p2n', p2n)
    config.set('FIGHT', 'fighting', 'True')             #set fighting to True
    ftn = random.randint(1,int(p1n)+int(p2n))           #randomly decide winner based on odds
    if ftn <= int(p1n):
        config.set('FIGHT', 'winner', p1f)
        config.set('FIGHT', 'loser', p2f)
    else:
        config.set('FIGHT', 'winner', p2f)
        config.set('FIGHT', 'loser', p1f)
    with open('betgame.ini', 'w+') as configfile:       #update config
        config.write(configfile)
        