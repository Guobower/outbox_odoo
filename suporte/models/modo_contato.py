# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Modo_contato(models.Model):
    _name = 'modo_contato'
    _description = 'Modo de Contato'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do modo de contato",
        track_visibility="onchange")