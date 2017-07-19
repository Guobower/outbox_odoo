# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Plano_contas_destino(models.Model):
    _name = 'plano_contas_destino'
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True)
    
    codigo = fields.Char(
        string="Código",
        size=250,
        required=True)
    
    reduzido = fields.Char(
        string="Reduzido",
        size=250,
        required=True)
    
    