# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Status_adesao(models.Model):
    _name = 'status_adesao'
    _description = 'Status da adesao'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'status_adesao': {
                'status_adesao.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'status_adesao.mt_descricao': lambda self, cr, uid, obj, ctx = None: obj.descricao
            }
    }
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do status de adesão",
        track_visibility="onchange")