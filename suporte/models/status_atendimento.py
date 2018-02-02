# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Status_atendimento(models.Model):
    _name = 'status_atendimento'
    _description = 'Status do atendimento'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do status do atendimento",
        track_visibility="onchange")