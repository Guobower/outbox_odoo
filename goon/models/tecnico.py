# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models
import simplejson
import urllib
class Tecnico(models.Model):
    _name = 'tecnico'
    _description = 'Registro de Tecnicos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
                       string="Nome",
                       size=150,
                       required=True)
        
    codigo_usuario = fields.Char(
                                 string="Codigo do Usuario",
                                 size=5)
        
    codigo_verificacao = fields.Char(
                                     string="Codigo Verificador",
                                     size=8)
        
    usuario = fields.Many2one(
                              comodel_name='res.users',
                              string='Usuario',
                              help='Usuario vinculado ao tecnico',
                              track_visibility='onchange')
                              
    email = fields.Char(
                        string="E-mail",
                        size=100
                        )
    
    telefone = fields.Char(
                           string="Telefone",
                           size=30
                           )
        
    
    def sincronizar_dados(self, cr, user, ids, context=None):
        from suds.client import Client
        import json
        
        obj_companhia = self.pool.get('res.company').browse(cr, user, 1)
        tecnico = self.pool.get('tecnico').browse(cr, user, ids[0])
        
        client = Client(obj_companhia.url)
        
        '''
        CAMPOS DO WEBSERVICE CASO DESEJE ADICIONAR MAIS ALGUM CONTROLE
        agent_code
        externalID
        name
        email
        telefone
        True
        True
        isToUpdateMobileAgentTeam
        mobileAgentTeamExternalId
        startMonitoringTime
        finishMonitoringTime
        addess
        addressNumber
        addressComplement
        addressNeighborhood
        addressCity
        addressState
        addressZipcode
        '''
        retorno = json.loads(client.service.SaveOrUpdateMobileAgent(obj_companhia.auth_code, 
            obj_companhia.client_code, tecnico.codigo_usuario, tecnico.id, tecnico.name, 
            tecnico.email, tecnico.telefone, 'true', 'true', 'true', 1, 
            '','','','','','','','',''))
        
        if retorno['success']:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Sincronização Concluída!',
                    'text': 'Dados enviados para o Goon.',
                    'sticky': False
                    }
             }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Erro ao sincronizar!',
                    'text': 'Houve um erro ao sincronizar, contate o administrador do sistema.',
                    'sticky': False
                    }
             }