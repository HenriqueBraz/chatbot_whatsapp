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
from connection import Connection
import re
import os
import requests
import json
import logging



class wppbot:
    
    dir_path = os.getcwd()
    

    def __init__(self, nome_bot):
        
        self.bot = ChatBot(nome_bot)
        self.trainer = ListTrainer(self.bot)
        self.chrome = '/home/henrique/alfio_bot/chromedriver_linux64/chromedriver' #Setamos onde está nosso chromedriver.
        self.options = webdriver.ChromeOptions() #Configuramos um profile no chrome para não precisar logar no whats toda vez que iniciar o bot.
        self.options.add_argument(r"user-data-dir="+self.dir_path+"/profile/wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options) #Iniciamos o driver.
        self.con = Connection('xxxxxxxxx',9906,'root','xxxxxxx')
    
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
        self.element_presence(By.XPATH,'//span[@title = "{}"]',30)
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


    def responde(self,texto):
        #método responde: parâmetro texto que é o  retorno do método escuta.
        response = self.bot.get_response(texto)
        response = str(response)
        response = 'Alfio_bot: ' + response
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        self.caixa_de_mensagem = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        self.caixa_de_mensagem.send_keys(response)
        time.sleep(1)
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]/button',30)
        self.botao_enviar = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        self.botao_enviar.click()
        
    def rapidinha(self,texto):
        response = str(texto)
        response = 'Alfio_bot: ' + response
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        self.caixa_de_mensagem = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        self.caixa_de_mensagem.send_keys(response)
        time.sleep(1)
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]/button',30)
        self.botao_enviar = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        self.botao_enviar.click()    
        
        
    def treina(self,nome_pasta):
        for treino in os.listdir(nome_pasta):
            conversas = open(nome_pasta+'/'+treino, 'r').readlines()
            self.trainer.train(conversas)
            
            
    def aprender(self,ultimo_texto,frase_inicial,frase_final,frase_erro):
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
        self.caixa_de_mensagem = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        self.caixa_de_mensagem.send_keys(frase_inicial)
        time.sleep(1)
        self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]/button',30)
        self.botao_enviar = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        self.botao_enviar.click()
        self.x = True
        while self.x == True:
            texto = self.escuta()

            if texto != ultimo_texto and re.match(r'^::', texto):
                if texto.find('?') != -1:
                    ultimo_texto = texto
                    texto = texto.replace('::', '')
                    texto = texto.lower()
                    texto = texto.replace('?', '?*')
                    texto = texto.split('*')
                    novo = []
                    for elemento in texto:
                        elemento = elemento.strip()
                        novo.append(elemento)

                    self.trainer.train(novo)
                    self.caixa_de_mensagem.send_keys(frase_final)
                    time.sleep(1)
                    self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]/button',30)
                    self.botao_enviar = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
                else:
                    self.caixa_de_mensagem.send_keys(frase_erro)
                    time.sleep(1)
                    self.element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[3]/button',30)
                    self.botao_enviar = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
            else:
                ultimo_texto = texto

    def noticias(self):

        req = requests.get('https://newsapi.org/v2/top-headlines?sources=globo&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'Alfio_bot: ' + titulo + ' ' + link + '\n'

            self.caixa_de_mensagem.send_keys(new)
            time.sleep(1)
            
        
        
if __name__ == "__main__":
    
    con = Connection('sigma.blisk.solutions',9906,'root','mt14GWE04L6Csjuk')
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s-%(levelname)s-%(message)s')
    logging.disable(logging.DEBUG)
    bot = wppbot('Alfio_bot')
    bot.treina('treino/')
    bot.inicia('Treino_bot')
    bot.saudacao(['Alfio_bot: Oi sou o Alfio_bot e entrei no grupo!','Alfio_bot: Use :: no início para falar comigo!','Alfio_bot: Agora o mais importante: tenho um vasto(?) conhecimento sobre provas. Digite ::prova? seguido do nome da disciplina, grau (p1,p2 ou p3) e nome do professor (tudo em minúsculo e sem assentos) da prova desejada, e eu consultarei no meu banco de dados. Ex. ::estatistica p1 rossana','Alfio_bot: e de quebra, também posso dizer as noticias. Use ::noticias para ficar informado dos fatos mais recentes que eu conseguir ;)'])
    ultimo_texto = ''
    
    while True:

        texto = bot.escuta()
        
        if texto != ultimo_texto and texto == 'atrasado' or texto == 'atrasei' or texto == 'vou chegar tarde' or texto == 'onde é a sala' or texto == 'onde é a sala?' or texto == 'qual a sala?' or texto == 'qual a sala' or texto == 'que sala' or texto == 'onde é a aula?' or texto == 'onde e a aula?' or texto == 'vou me atrasar' or texto == 'to atrasado' or texto == 'e ae galera! Vou me atrasar!' or texto == 'e ae galera vo me atrasa' or texto == 'e ae galera vo me atrasa!' or texto == 'que sala?' or texto == 'que sala':
                bot.rapidinha('Eu não me atraso nunca. NUNCA!')
        
        elif texto != ultimo_texto and texto == 'show!' or texto == 'Show!' or texto == 'show' or texto == ' Show' or texto == 'legal' or texto == 'legal!' or texto == 'caralho!' or texto == 'caralho' or texto == 'que legal' or texto == 'que legal!' or texto == 'demais' or texto == 'demais!' or texto == 'massa' or texto == 'massa!' or texto == 'q orgulho' or texto == 'Dale' or texto == 'top' or texto == 'noes' or texto == 'Mito' or texto == 'Eita' or texto == 'Vamooo' or texto == 'caralho mano' or texto == 'BAITA' or texto == 'Valeu!' or texto == 'deuu' or texto == 'Que foda' or texto == 'Boa pai' or texto == 'boa pai' or texto == 'Caralho!' or texto == 'Caralho' or texto == 'boa' or texto == 'boaaa':
                bot.rapidinha('AMAZING!')
                
        elif texto != ultimo_texto and texto == 'provas' or texto == ' provas' or texto == 'prova' or texto == ' prova':
                bot.rapidinha('Alguém aí falou em provas? AMAZING! Digite ::prova? seguido do nome da disciplina, grau (p1,p2 ou p3) e nome do professor (tudo em minúsculo e sem assentos) da prova desejada, e eu consultarei no meu banco de dados. Ex. ::estatistica p1 rossana')
                
        elif texto != ultimo_texto and texto == 'noticias' or texto == ' noticias' or texto == 'noticia' or texto == ' noticia' or texto == 'notícias' or texto == ' notícias' or texto == 'notícia' or texto == ' notícia':
                bot.rapidinha('AMAZING! Alguém aí falou notícias? Eu sei tudo sobre notícias e fofocas. Pergunte pra mim, digite ::noticias')
                
        elif texto != ultimo_texto and re.match(r'^::', texto): ##Validação se possuí o comando :: no início para que ele responda.
            ultimo_texto = texto
            texto = texto.replace('::', '')
            texto = texto.lower()
            if (texto == 'aprender' or texto == ' aprender' or texto == 'ensinar' or texto == ' ensinar'):
                bot.aprender(texto,'Alfio_bot: Escreva ::  e depois  a pergunta; e após o ? a resposta.','Alfio_bot: Obrigado por ensinar. Não que eu precise, afinal eu sou o Alfio_bot, só errei uma vez na vida: quando pensei estar errado!','Alfio_bot: Você escreveu algo errado! Comece novamente..')
                
            elif (texto == 'noticias' or texto == ' noticias' or texto == 'noticia' or texto == ' noticia' or texto == 'notícias' or texto == ' notícias' or texto == 'notícia' or texto == ' notícia'):
                bot.noticias()
                    
                
            else:
                bot.responde(texto)
    


        
