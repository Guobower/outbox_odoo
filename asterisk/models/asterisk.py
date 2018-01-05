# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Asterisk(models.Model):
    _name = 'asterisk'
    
    name = fields.Char(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        size=150,
        required=True)
    
    id_agent = fields.Integer(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    id_queue_call_entry = fields.Integer(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        required=True)
    
    id_contact = fields.Integer(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    callerid = fields.Char(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        size=15,
        required=True)
    
    datetime_init = fields.Datetime(
        string='Nome amigavel da coluna',
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    datetime_end = fields.Datetime(
        string='Nome amigavel da coluna',
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    duration = fields.Integer(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    status = fields.Char(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        size=32)
    
    transfer = fields.Char(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        size=6)
    
    datetime_entry_queue = fields.Datetime(
        string='Nome amigavel da coluna',
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    duration_wait = fields.Integer(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    uniqueid = fields.Char(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        size=32)
    
    id_campaign = fields.Integer(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna')
    
    trunk = fields.Char(
        string="Nome amigavel da coluna",
        help='Texto de descrição para o help do sistema, descrever o que é a coluna',
        size=20,
        required=True)
    
    
    def atualizar_dados_servidor(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Descreva aqui o objetivo da função e como ela deve executar.
        
            Utilização:
              atualizar_dados_servidor()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs dos registros selecionados
              context
                Contexto atual
        '''
        # Codifique a comunicação com o servidor do Asterix aqui
        
        # Busca o modelo do asterisk
        asterisk_obj = self.pool.get('asterisk')
        last_asterisk_obj = asterisk_obj.search(cr, uid,  [], limit=1, order='id desc')
        # Chama o método de criação/inserção no banco passando como parâmetro os campos e os conteúdos
        asterisk_obj.create(cr, uid, {'name': 'Teste', 'trunk':'Teste', 'callerid':'Teste', 'id_queue_call_entry': 1}, context=context)     
        
        # Retornando um alerta na tela do usuário, enquanto desenvolve você pode usar para saber 
        # se a comunicação está dando certo
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Título do Alerta! ' + str(last_asterisk_obj[0]),
                'text': 'Texto do Alerta.',
                'sticky': True
                }
        }
