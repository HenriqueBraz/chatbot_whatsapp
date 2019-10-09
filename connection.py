#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 22:05:02 2019

@author: henrique
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# connection - python 3.7.0
# by Henrique Keller Braz


import pymysql
from random import randint
import logging

class Connection(object):
    '''   
    def __init__(self,host, port, user, bank_pass):
        """
        construtor que inicia a conexão com o MySQL 
        :param host: nome do host, string
        :param port: numero da porta, int
        :param user: nome do usuario, string
        :param bank_pass: senha, string
        """
        self.host = host
        self.port = port
        self.user = user
        self.bank_pass = bank_pass
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s-%(levelname)s-%(message)s')
        logging.info('Construtor do Connection chamado com sucesso\n')
        #logging.disable(logging.DEBUG)
    '''      
    def __init__(self,host = 'localhost', port = 3306, user = 'django', bank_pass =  'root'):
        """
        construtor que inicia a conexão com o MySQL local
        :param host: nome do host, string
        :param port: numero da porta, int
        :param user: nome do usuario, string
        :param bank_pass: senha, string
        """
        self.host = host
        self.port = port
        self.user = user
        self.bank_pass = bank_pass
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s-%(levelname)s-%(message)s')
        logging.info('Construtor do Connection chamado com sucesso\n')
        #logging.disable(logging.DEBUG)
                         
        
    def busca_prova(self):
        """
        :return: retorna uma lista contendo os dados das provas
        """
        try:
             provas = []
             conn = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.bank_pass)
             cur = conn.cursor()
             cur.execute("USE gerenciador_tarefas")
             cur.execute("SELECT * from provas")   
             for row in cur: 
                 provas.append(row) 
        
             cur.close()
             conn.close()
             return provas
        
        except Exception as e:
            logging.error('Erro em Connection, método busca_prova: ' + str(e)+'\n')
            
    def data_bank_input_leads(self,lista):
        """
        função responsável por inputar os dados na tabela leads
        :param lista: lista vinda do parser para ser salva no banco
        :return: retorna False caso a lista esteja vazia
        """                        
        try: #conexão

            if lista == []:
                return False

            else:
                logging.info('\n' + str(lista) +'\n')
                conn = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.bank_pass)
                cur = conn.cursor()
                cur.execute("USE blisk")
                for i in range(len(lista)):
                    Id = str(lista[i][0])
                    sql_data = (Id,lista[i][1],lista[i][2],lista[i][3],lista[i][4],lista[i][5],lista[i][6],lista[i][7],lista[i][8],lista[i][9],lista[i][10])
                    sql = "INSERT INTO leads (id_mongo,data_email,nome,telefone,email,codigo_produto,id_incorporadora,origem_id,contato,periodo_contato,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cur.execute(sql, sql_data)
                        
                conn.commit()
                cur.close()
                conn.close()
                return True

        except Exception as e:
            logging.error('Erro em Conection, método data_bank_input, conexão: ' + str(e) + '\n')
            
            
   