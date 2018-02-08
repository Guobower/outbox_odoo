# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Sistemas_monitoramento(models.Model):
    _name = 'sistemas_monitoramento'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)