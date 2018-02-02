# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Protocolo(models.Model):
    _name = 'protocolo'
    _description = 'Protocolo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    

    _defaults = {
        'name': lambda self, cr, uid, context = {}: self.pool.get('ir.sequence').get(cr, uid, 'protocolo.protocolo_sequence'),
        }
    
    name = fields.Char(
        string="Protocolo",
        size=250,
        required=True,
        track_visibility='onchange')
    
    contrato = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Contrato',
        help='Contrato ao qual está vinculado o protocolo',
        track_visibility='onchange')
    
    adesao = fields.Many2one(
        comodel_name='adesao',
        string='Adesao',
        help='Adesão a qual está vinculado o protocolo',
        track_visibility='onchange')
