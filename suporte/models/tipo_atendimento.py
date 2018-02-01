# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Tipo_atendimento(models.Model):
    _name = 'tipo_atendimento'
    _description = 'Tipo de atendimento'
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
    
    grupo_atendimento = fields.Many2one(
        string="Grupo de Atendimento",
        comodel_name='grupo_atendimento',
        help="Grupo de atendimento ao qual esta vinculado o tipo de atendimento")
    
    procedimento = fields.Text(
        string="Procedimento",
        help="Procedimento a ser seguido pelo atendente")
    
    orientacao = fields.Text(
        string="Orientação",
        help="Orientação ao atendente sobre onde buscar a informação necessária ao atendimento")
    
    tempo_resolucao = fields.Integer(
        string="Tempo Necessário para Resolução (dias)",
        help="Tempo necessário para a resolução desse tipo de atendimento em dias.")