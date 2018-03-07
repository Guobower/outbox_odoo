# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Status_ocorrencia(models.Model):
    _name = 'status_ocorrencia'
    _description = 'Status de ocorrencias'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do status da ocorrência",
        track_visibility="onchange")