#coding=utf-8

from openerp import fields, api, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ind_final = fields.Selection([
        ('0', u'Não'),
        ('1', u'Consumidor final')],
        string=u'Operação com Consumidor final', required=False,
        help=u'Indica operação com Consumidor final.', default='0') 