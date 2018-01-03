# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Sistemas_helpdesk(models.Model):
    _name = 'sistemas_helpdesk'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)