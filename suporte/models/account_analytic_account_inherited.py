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
    
    adesao = fields.One2many(
        comodel_name='adesao',
        inverse_name='contrato',
        string='Adesoes',
        help='Adesões vinculadas ao contrato')
    
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
    
    
    def gerar_pdf_adesao(self, cr, user, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo imprimir um pdf da Adesão para assinatura do cliente.
        
            Utilização:
              gerar_pdf_adesao()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da adesão em questão
              context
                Contexto atual
        '''
        adesao = self.env.context.get('adesao')
        self.pool.get('adesao').gerar_pdf_adesao(cr, user, adesao, context=context)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'suporte.report_adesao',
            'context': context,
        }
    