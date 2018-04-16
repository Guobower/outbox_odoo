# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Res_partner_inherited(models.Model):
    _inherit = 'res.partner' 
 
    def sincronizar_dados(self, cr, user, ids, context=None):
        from suds.client import Client
        import json
        
        obj_companhia = self.pool.get('res.company').browse(cr, user, 1)
        parceiro = self.pool.get('res.partner').browse(cr, user, ids[0])
        
        client = Client(obj_companhia.url)
        
        if parceiro.is_company:
            fisica_juridica = 'J'
        else:
            fisica_juridica = 'F'
        
        if parceiro.number:
            numero = parceiro.number
        else:
            numero = 0
        
        if parceiro.email:
            email = parceiro.email
        else:
            email = ''
            
        retorno = json.loads(client.service.SaveOrUpdateCliente(
                             '9C5B5AD6D8274DFACCA449FD22E962A066A0B20C',
                             obj_companhia.client_code, 
                             parceiro.id_syncron,
                             parceiro.id_syncron,
                             parceiro.name,
                             fisica_juridica,
                             parceiro.cnpj_cpf,
                             'CNOR',
                             parceiro.street,
                             numero,
                             parceiro.street2,
                             parceiro.district,
                             parceiro.l10n_br_city_id.name,
                             parceiro.state_id.code,
                             parceiro.zip,
                             parceiro.phone,
                             parceiro.phone,
                             parceiro.mobile,
                             email,
                             parceiro.comment,
                             parceiro.name,
                             'true',
                             'true',
                             'External'
                             ))
        
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
                    'text': 'Houve um erro ao sincronizar, contate o administrador do sistema.' + str(retorno),
                    'sticky': True
                    }
            }
    
    
    
