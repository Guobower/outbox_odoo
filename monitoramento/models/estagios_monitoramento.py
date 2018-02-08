# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Estagios_monitoramento(models.Model):
    _name = 'estagios_monitoramento'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)