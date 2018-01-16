# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Grupo_servico(models.Model):
    _name = 'grupo_servico'
    _description = 'Grupos de Servicos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'grupo_servico': {
                'grupo_servico.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'grupo_servico.mt_descricao': lambda self, cr, uid, obj, ctx = None: obj.descricao
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