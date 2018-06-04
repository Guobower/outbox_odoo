# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Tipo_ocorrencia(models.Model):
    _name = 'tipo_ocorrencia'
    _description = 'Tipo de ocorrencia'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do tipo da ocorrência",
        track_visibility="onchange")
        
    titulo_padrao = fields.Char(
        string="Titulo Padrao",
        size=250,
        track_visibility='onchange')
        
    texto_padrao = fields.Text(
        string="Texto Padrao",
        help="Texto padrão do tipo da ocorrência",
        track_visibility="onchange")