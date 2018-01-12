# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Account_analytic_account_inherited(models.Model):
    _inherit = 'account.analytic.account' 
 
    _track = {
            'account.analytic.account': {
                'account.analytic.account.mt_stage_id': lambda self, cr, uid, obj, ctx = None: obj.status_contrato
            }
    }
    
    _defaults={
        'stage_id' : 1,
        'type': 'contract'
    }
    
    status_contrato = fields.Many2one(
        comodel_name='status_contrato',
        string='Status',
        help='Status do contrato',
        track_visibility='onchange')
    
    tipo_envio  = fields.Selection(
        selection=[('1', 'Correios'),
                   ('2', 'E-mail')],
        string='Tipo de envio do boleto',
        help='Forma escolhida pelo cliente para envio do boleto',
        track_visibility='onchange')
    
    data_base_vencimento = fields.Integer(
        string="Data de Vencimento dos Boletos",
        help="Data base para vencimento dos boletos",
        track_visibility='onchange')
    
    tipo_contrato = fields.Selection(
        selection=[('1', 'Banda Larga'),
                   ('2', 'Corporativo'),
                   ('3', 'Licitado'),
                   ('4', 'Provedor')],
        string='Tipo de Contrato',
        help='Tipo de contrato com o cliente',
        track_visibility='onchange')