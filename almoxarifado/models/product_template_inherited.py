# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Product_template_inherited(models.Model):
    _inherit = 'product.template'
        
    imobilizado = fields.Selection(
        selection=[('sim', 'Sim'), ('nao', 'Não')],
        string='Imobilizado',
        help='Este produto consta como ativo imobilizado da empresa?')