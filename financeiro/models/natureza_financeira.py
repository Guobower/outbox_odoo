# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Natureza_destino(models.Model):
    _name = 'natureza_financeira'
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True)
    
    descricao = fields.Text(
        string="Descrição")