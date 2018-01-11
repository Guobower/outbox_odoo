# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Adesao(models.Model):
    _name = 'adesao'
    _description = 'Adesão de Contratos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Adesão",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição da Adesão",
        track_visibility="onchange")