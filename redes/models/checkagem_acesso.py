# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Checkagem_acesso(models.Model):
    _name = 'checkagem_acesso'
    _description = 'Checkagem de acesso'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Selection(
        string="IP/Login",
        selection=[('1', 'IP'),
                   ('2', 'Login')],
        required=True,
        track_visibility='onchange')
    
    valor = fields.Char(
        string="Valor",
        size=20,
        help="Valor",
        track_visibility="onchange")
    
    data_inicio = fields.Date(
        string='Data de Inicio',
        help='Data de Inicio',
        track_visibility='onchange')
    
    data_termino = fields.Date(
        string='Data de Termino',
        help='Data de Termino',
        track_visibility='onchange')
    
    
    def report_gerar_relatorio(self, cr, user, ids, name, valor, data_inicio, data_termino, context=None):
        '''
            Descrição:
              Busca no banco do Syncron os dados para geração do relatório.
        
            Utilização:
              report_gerar_relatorio()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              context
                Contexto atual
        '''
        import requests
        r = requests.get('http://syncron.cinte.com.br/radacct/checkagem_acesso.php?escolha='+str(name)+'&valor='+str(valor)+'&data_inicio='+str(data_inicio)+'&data_termino='+str(data_termino)+'')
        
        retorno = list()
        if r.json():
            for linha in r.json():
                objeto = list()
                objeto.append(linha["cliente"])
                objeto.append(linha["cliente_username"])
                objeto.append(linha["data_inicio"])
                objeto.append(linha["data_termino"])
                retorno.append(objeto)
        
        return retorno
    
