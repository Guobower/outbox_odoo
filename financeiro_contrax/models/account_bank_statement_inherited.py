# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Account_bank_statement_inherited(models.Model):
    _inherit = 'account.bank.statement'
    
    journal_id = field.Many2one(
        domain="[('id','=',1)]"
    )