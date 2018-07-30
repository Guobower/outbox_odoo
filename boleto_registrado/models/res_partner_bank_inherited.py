# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models

class Res_partner_bank_inherited(models.Model):
    _inherit = 'res.partner.bank'

    carteira = fields.Char(
        string="Carteira",
        size=2
    )

    variacao_carteira = fields.Char(
        string="Variação da Carteira",
        size=3
    )

