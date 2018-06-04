# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Contato_localidade(models.Model):
    _name = 'contato_localidade'
    _description = 'Contatos de localidades'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
                       string="Nome",
                       size=250,
                       required=True,
                       track_visibility='onchange')
                       
    contato = fields.Char(
                          string="Contato",
                          size=250,
                          required=True,
                          track_visibility='onchange')
                               
    localidade = fields.Many2one(
                                 string="Localidade",
                                 comodel_name='localidade',
                                 required=True,
                                 help="Localidade a qual o contato está vinculado")