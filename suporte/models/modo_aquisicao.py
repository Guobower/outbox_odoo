# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Modo_aquisicao(models.Model):
    _name = 'modo_aquisicao'
    _description = 'Modo de Aquisicao'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'modo_aquisicao': {
                'modo_aquisicao.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'modo_aquisicao.mt_descricao': lambda self, cr, uid, obj, ctx = None: obj.descricao
            }
    }
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do grupo de serviço",
        track_visibility="onchange")