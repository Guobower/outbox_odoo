# -*- coding: utf-8 -*-
from openerp import models, fields

class Account_account_inherited(models.Model):
    _inherit = 'account.account' 

    de_para = fields.Many2one(
        comodel_name='plano_contas_destino',
        string='Plano de Contas Destino - De/Para',
        help='Plano de Contas Destino para o De/Para')