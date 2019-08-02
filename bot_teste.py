#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 20:10:42 2019

@author: henrique
"""

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import os

bot = ChatBot("Alfio")
#bot = ChatBot("Alfio", read_only=True)

trainer = ListTrainer(bot)

for arq in os.listdir('arq'):
    conversa = open('arq/' + arq, 'r').readlines()
    trainer.train(conversa)
    
while True:
    resq = input('Você: ')
    
    resp = bot.get_response(resq)
    print('Alfio_bot: ' + str(resp))

        




