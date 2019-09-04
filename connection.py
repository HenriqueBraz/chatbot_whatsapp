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
    
    def __init__(self,host, port, user, bank_pass):
        """
        classe responsável pela conexão com o MySQL
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
        
        
    def data_bank_connection(self):
        """
        :return: retorna uma lista contendo os dados dos verticais
        """
        try:
            incorp_data_list = []
            conn = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.bank_pass)
            cur = conn.cursor()
            cur.execute("USE blisk")
            cur.execute("SELECT i.id as id_incorporadora, i.nome as nome_incorporadora, imap.id as id_imap,imap.usuario as usuario_imap,imap.senha as senha_imap,imap.endereco_imap as endereco_imap,imap.porta_imap as porta_imap FROM incorporadoras i INNER JOIN incorporadoras_imap imap ON i.id=imap.id_incorporadora AND imap.status='Ativo' WHERE i.status='Ativo'")
            #print(cur.description)
            for row in cur: 
                incorp_data_list.append(row)
        
            cur.close()
            conn.close()
            return incorp_data_list
        
        except Exception as e:
            logging.error('Erro em Connection, método data_bank_connection: ' + str(e)+'\n')
            
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
            
            
    def data_from_leads(self):
        """
        função responsável pela conexão com o MySQL - tabela leads INNER JOIN tabela produtos;
        :return: retorna uma lista contendo os dados das duas tabelas, 
        pegando somente as menssagens não lidas
        """
        try:
            leads_data_list = []
            conn = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.bank_pass)
            cur = conn.cursor()
            rand = (randint(1,10000))
            cur.execute("USE blisk")
            sql = ("UPDATE leads SET uniq_pool_id = '%s' WHERE status = 'unread' AND uniq_pool_id IS NULL;")
            cur.execute(sql, rand)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
            sql = ("SELECT l.*, p.nome_produto as produto_nome_produto, p.tipo_endereco as produto_tipo_endereco, p.endereco as produto_endereco, p.numero as produto_numero, p.complemento as produto_complemento, p.bairro as produto_bairro, p.cidade as produto_cidade, p.estado as produto_estado, p.tipo_produto as produto_tipo_produto, p.dormitorios as produto_dormitorios, p.vagas as produto_vagas, p.valor as produto_valor FROM leads l INNER JOIN produtos p ON l.codigo_produto = p.codigo_produto WHERE l.status = 'unread' AND l.uniq_pool_id = '%s' AND l.agendamento IS NULL; ")
            cur.execute(sql, rand)
            for row in cur: 
                leads_data_list.append(row)
                
            sql = ("UPDATE leads SET status = 'read' WHERE status = 'unread' AND uniq_pool_id= '%s';")
            cur.execute(sql, rand)
            conn.commit()    
            cur.close()
            conn.close()
            return leads_data_list
           
        except Exception as e:
            logging.error('Erro em Connection, método data_from_leads: ' + str(e) +'\n')


    def data_from_leads_comunicacao(self):
        """
        método que monitora a tabela leads_comunicacao, 
        buscando "WHERE processado=0"
        """
        try:
            leads_comunicacao_list = []
            conn = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.bank_pass)
            cur = conn.cursor()
            rand = (randint(1,10000))
            cur.execute("USE blisk")
            sql = ("UPDATE leads_comunicacao SET uniq_pool_id = '%s' WHERE processado=0 AND uniq_pool_id IS NULL;")
            cur.execute(sql, rand)
            sql = ("SELECT c.*,l.contato, l.nome FROM leads_comunicacao c INNER JOIN leads l on l.id = c.id_lead WHERE c.processado = 0 AND c.uniq_pool_id = '%s';")
            cur.execute(sql, rand)
            for row in cur:
                leads_comunicacao_list.append(row)
                
            sql = ("UPDATE leads_comunicacao SET processado = 1 WHERE processado = 0 AND uniq_pool_id= '%s';")
            cur.execute(sql, rand)    
            conn.commit()    
            cur.close()
            conn.close()
            return leads_comunicacao_list

        except Exception as e:
            logging.error('Erro em Connection, método monitoring: ' + str(e) +'\n')
       
    
 
    
    
    
    
