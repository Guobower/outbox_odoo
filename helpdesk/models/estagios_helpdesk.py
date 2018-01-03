# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Estagios_helpdesk(models.Model):
    _name = 'estagios_helpdesk'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)