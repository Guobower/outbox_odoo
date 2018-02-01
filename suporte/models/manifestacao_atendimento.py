# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Manisfestacao_atendimento(models.Model):
    _name = 'manifestacao_atendimento'
    _description = 'Manifestacao de atendimento'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição",
        track_visibility="onchange")
    
    grupo_atendimento = fields.One2many(
        comodel_name='grupo_atendimento',
        inverse_name='manifestacao_atendimento',
        string='Grupos de Atendimento',
        help='Grupos de atendimento vinculados a manifestação')