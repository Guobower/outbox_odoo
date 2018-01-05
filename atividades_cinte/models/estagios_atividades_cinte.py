# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Estagios_atividades_cinte(models.Model):
    _name = 'estagios_atividades_cinte'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)