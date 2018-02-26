# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Conexoes_ativas(models.Model):
    _name = 'conexoes_ativas'
    _description = 'Conexoes ativas'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
                       string="Relatorio",
                       size=100,
                       required=True,
                       track_visibility='onchange')
    
    
    def report_gerar_relatorio(self, cr, user, ids, context=None):
        '''
            Descrição:
              Busca no banco do Radius os dados para geração do relatório.
        
            Utilização:
              report_gerar_relatorio()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs do relatório em questão
              context
                Contexto atual
        '''
        import requests
        r = requests.get('http://syncron.cinte.com.br/radacct/conexoes_ativas.php')
        
        retorno = list()
        if r.json():
            for linha in r.json():
                objeto = list()
                objeto.append(linha["username"])
                objeto.append(linha["framedipaddress"])
                objeto.append(linha["callingstationid"])
                objeto.append(linha["acctstarttime"])
                objeto.append("http://syncron.cinte.com.br/scriptOdoo/radacct/desconectar_cliente.php?mac="+linha["callingstationid"])
                retorno.append(objeto)
                #acctstoptime = null
        
        return retorno
    
