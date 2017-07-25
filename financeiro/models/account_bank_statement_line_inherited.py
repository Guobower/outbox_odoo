# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Account_bank_statement_line_inherited(models.Model):
    _inherit = 'account.bank.statement.line'
    
    
    def gerar_recibo(self, cr, uid, ids, context=None):
        if ids:
            if not isinstance(ids, list):
                ids = [ids]
            context = dict(context or {}, active_ids=ids, active_model=self._name)
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'financeiro.report_recibo_caixa',
            'context': context,
        }