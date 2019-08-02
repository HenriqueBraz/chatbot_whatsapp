#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:55:42 2019

@author: henrique
"""
#Bibliotecas nativas do Python.
import os 
import time
import re
from selenium import webdriver
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot


class wppbot:
    

    def __init__(self, nome_bot): #Nosso contrutor terá a entrada do nome do nosso bot
#Setamos nosso bot e a forma que ele irá treinar.
        self.bot = ChatBot(nome_bot)
        self.bot.set_trainer(ListTrainer)
        self.chrome = '/home/henrique/chatbot/chatbot_whatsapp/chromedriver' #Setamos onde está nosso chromedriver.
        self.options = webdriver.ChromeOptions() #Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options) #Iniciamos o driver.