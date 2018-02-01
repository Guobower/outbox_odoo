# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Grupo_atendimento(models.Model):
    _name = 'grupo_atendimento'
    _description = 'Grupo de atendimento'
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
    
    tipo_atendimento = fields.One2many(
        comodel_name='tipo_atendimento',
        inverse_name='grupo_atendimento',
        string='Tipos de Atendimento',
        help='Tipos de atendimento vinculados ao grupo')
    
    manifestacao_atendimento = fields.Many2one(
        string="Manifestação de Atendimento",
        comodel_name='manifestacao_atendimento',
        help="Manifestação de atendimento ao qual esta vinculado o grupo de atendimento")