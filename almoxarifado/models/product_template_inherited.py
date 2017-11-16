# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Product_template_inherited(models.Model):
    _inherit = 'product.template'
        
    imobilizado = fields.Selection(
        selection=[('sim', 'Sim'), ('nao', 'Não')],
        string='Imobilizado',
        help='Este produto consta como ativo imobilizado da empresa?')
    
    origem_compra = fields.Many2one(
        string='Origem das Compras',
        help='Principal estado de origem das compras',
        comodel_name='res.country.state')