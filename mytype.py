# -*- coding: utf-8 -*-

import random
import configparser

def whattype():         #return random pokemon type
    typelist = ['normal 😐','fighting 👊','flying 🌬️','poison ☠️','ground ⛰️','rock 🗿','bug 🐛','ghost 👻'
                ,'steel 🔩','fire 🔥','water 💦','grass 🌱','electric ⚡','psychic 👁‍','ice ❄️','dragon 🐉','dark 🌙','fairy ✨']
    type1 = random.choice(typelist).capitalize()
    ran = random.randint(1,100)
    if ran < 25:
        type2 = random.choice(typelist).capitalize()
        while type1 == type2:
            type2 = random.choice(typelist).capitalize()
        if type1 == 'Electric ⚡' or type1 == 'Ice ❄️':
            return ['an', type1, type2]
        else:
            return ['a', type1, type2]
    elif type1 == 'Electric ⚡' or type1 == 'Ice ❄️':
        return ['a', type1]
    else:
        return ['a', type1]
    
def whataesthet():          #return random list of two adjectives and a noun as an aesthetic
    config = configparser.ConfigParser()
    config.read('betgame.ini')
    adjectives = config['MYTYPE']['adjectives'].split('\n')
    nouns = config['MYTYPE']['nouns'].split('\n')
    
    adj1 = random.choice(adjectives)
    adj2 = random.choice(adjectives)
    while adj1 == adj2:
        adj2 = random.choice(adjectives)
    noun = random.choice(nouns)
    
    return adj1,adj2,noun

def whatclass():            #returns a race, class, and quirk for dnd character
    config = configparser.ConfigParser()
    config.read('betgame.ini')
    races = config['MYTYPE']['races'].split('\n')
    classes = config['MYTYPE']['classes'].split('\n')
    quirks = config['MYTYPE']['quirks'].split('\n')
    
    race    = random.choice(races)
    clas    = random.choice(classes)
    quirk   = random.choice(quirks)
    return race, clas, quirk

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
