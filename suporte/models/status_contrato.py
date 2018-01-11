# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Status_contrato(models.Model):
    _name = 'status_contrato'
    _description = 'Status de Contratos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'status_contrato': {
                'status_contrato.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'status_contrato.mt_descricao': lambda self, cr, uid, obj, ctx = None: obj.descricao
            }
    }
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do status de contrato",
        track_visibility="onchange")