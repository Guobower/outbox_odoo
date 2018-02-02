# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Account_analytic_account_inherited(models.Model):
    _inherit = 'account.analytic.account' 
 
    _track = {
            'account.analytic.account': {
                'account.analytic.account.mt_stage_id': lambda self, cr, uid, obj, ctx = None: obj.status_contrato
            }
    }
    
    _defaults = {
        'stage_id' : 1,
        'type': 'contract'
    }
    
    status_contrato = fields.Many2one(
        comodel_name='status_contrato',
        string='Status',
        help='Status do contrato',
        track_visibility='onchange')
    
    tipo_envio = fields.Selection(
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
    
    adesao = fields.One2many(
        comodel_name='adesao',
        inverse_name='contrato',
        string='Adesoes',
        help='Adesões vinculadas ao contrato')
    
    protocolo = fields.One2many(
        comodel_name='protocolo',
        inverse_name='contrato',
        string='Protocolos',
        help='Protocolos vinculados ao contrato')
    
    contrato_pdf = fields.Binary(
        string='Contrato Assinado',
        help='Contrato assinado pelo cliente.')
    
    contrato_pdf_filename = fields.Char("Contrato Assinado", 
        track_visibility='onchange')
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    
    date_start = fields.Date(
        track_visibility='onchange'
        )
    
    recurring_invoices = fields.Boolean(
        track_visibility='onchange'
        )
    
    recurring_interval = fields.Integer(
        track_visibility='onchange'
        )
    
    recurring_next_date = fields.Date(
        track_visibility='onchange'
        )
    
    recurring_rule_type = fields.Selection(
        track_visibility='onchange'
        )
    
    
    def ativar_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 13}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def inativar_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 12}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def suspender_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 14}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def cancelar_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 15}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def free_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 16}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def nunca_bloquear_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 17}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        