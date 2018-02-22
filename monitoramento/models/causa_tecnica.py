# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Causa_tecnica(models.Model):
    _name = 'causa_tecnica'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)