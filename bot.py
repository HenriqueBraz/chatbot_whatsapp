#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:55:42 2019

@author: henrique
"""
#Bibliotecas nativas do Python.
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import re
import os
import logging



class wppbot:
    
    dir_path = os.getcwd()
    

    def __init__(self, nome_bot):
        
        self.bot = ChatBot(nome_bot)
        self.trainer = ListTrainer(self.bot)
        #self.bot.set_trainer(ListTrainer)
        self.chrome = '/home/henrique/chatbot/chatbot_whatsapp/chromedriver' #Setamos onde está nosso chromedriver.
        self.options = webdriver.ChromeOptions() #Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
        self.options.add_argument(r"user-data-dir="+self.dir_path+"/profile/wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options) #Iniciamos o driver.
    
    
    def element_presence(self,by,xpath,time):
        """
         função responsável pela pausa até o carregamento do
         elemento procurado estar carregado
         """
        try:
             element_present = EC.presence_of_element_located((By.XPATH, xpath))
             WebDriverWait(self.driver, time).until(element_present)
        except Exception as e:
            logging.error('Erro no element_presence:' + str(e))    
        
        
        
    def inicia(self,nome_contato):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)
        self.element_presence(By.XPATH,'//*[@id="side"]/div[1]/div/label/input',30)
        self.caixa_de_pesquisa = self.driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/input')
        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)   
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)
        
    
    def saudacao(self,frase_inicial):
        #Ao usar este método devemos enviar a mensagem de saudação em uma lista.
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        self.caixa_de_mensagem = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        if type(frase_inicial) == list:

            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]/button',30)
                self.botao_enviar = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False
        
    def escuta(self):
        post = self.driver.find_elements_by_class_name('_1zGQT') #seta todas as mensagens no grupo
        ultimo = len(post) - 1 #pega o índice da última conversa.
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text #pega o texto da última conversa
        return texto    
        
        
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s-%(levelname)s-%(message)s')
    bot = wppbot('Alfio')
    bot.inicia('Lembrete')
    bot.saudacao(['Não liguem, sou um bot em teste'])
    logging.info(bot.escuta())
    


        