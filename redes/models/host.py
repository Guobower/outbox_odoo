# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Host(models.Model):
    _name = 'host'
    _description = 'Host'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Host Name",
        size=250,
        required=True,
        track_visibility='onchange')

    host_id_centreon = fields.Integer(
        string="Host ID no Centreon",
        required=True,
        track_visibility='onchange')
    
    contrato = fields.Many2one(
        string="Contrato",
        comodel_name='account.analytic.account',
        help="Contrato ao qual este host está vinculado")