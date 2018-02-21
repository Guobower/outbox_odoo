# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Sla(models.Model):
    _name = 'sla'
    _description = 'SLA'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Selection(
                            string="Servico",
                            selection=[('Ping', 'Latência')],
                            required=True,
                            track_visibility='onchange')
    
    contrato = fields.Many2one(
                               comodel_name='account.analytic.account',
                               string='Contrato',
                               required=True,
                               help='Contrato a verificar',
                               track_visibility='onchange')
    
    host = fields.Many2many(
                            comodel_name='host',
                            string='Host',
                            required=True,
                            help='Host para visualização',
                            track_visibility='onchange')
    
    data_inicio = fields.Date(
                              string='Data de Inicio',
                              help='Data de Inicio',
                              required=True,
                              track_visibility='onchange')
    
    data_termino = fields.Date(
                               string='Data de Termino',
                               help='Data de Termino',
                               required=True,
                               track_visibility='onchange')
    
    
    
    def gerar_sla(self, cr, user, ids, context=None):
        '''
        trabalhe_conosco = self.pool.get('trabalhe_conosco').browse(cr, user, ids[0])
        url = 'http://www.cinte.com.br/2016/trabalheConosco/'+str(trabalhe_conosco.curriculo) 
        res = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }
        
        return res
        '''
        import urllib
        sla = self.pool.get('sla').browse(cr, user, ids[0])
        parametros = { 'servico' : str(sla.name), 'inicio' : str(sla.data_inicio), 'final' :str(sla.data_termino)}
        url = 'http://syncron.cinte.com.br/scriptOdoo/sla/relatorioSla.php?' + urllib.urlencode(parametros)
        #url += '&inicio=' + str(sla.data_inicio)
        #url += '&final=' + str(sla.data_termino)
        
        for linha_host in sla.host:
            url += '&hosts[]=' + str(linha_host.host_id_centreon)
        
        res = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }
        
        return res
    
    def report_gerar_relatorio(self, cr, user, ids, host, data_inicio, data_termino, context=None):
        '''
            Descrição:
              Busca no banco do Centreon os dados para geração do relatório.
        
            Utilização:
              report_gerar_relatorio()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs do SLA em questão
              context
                Contexto atual
        '''
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
        '''
    
