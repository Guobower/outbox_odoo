# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models


class Account_analytic_account_inherited(models.Model):
    _inherit = 'account.analytic.account' 
 
    acrescimo_desconto = fields.One2many(
                                 comodel_name='acrescimo_desconto',
                                 inverse_name='contrato',
                                 string='Acréscimos/Descontos',
                                 help='Acréscimos e descontos recorrentes associadas ao contrato')


class Acrescimo_desconto(models.Model):
    """
    Classe para registro de acréscimos e descontos futuros no contrato.
    """

    _name = 'acrescimo_desconto'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Selection(
        selection=[('acres', 'Acréscimo'),
                   ('desc', 'Desconto')],
        string='Tipo',
        required=True,
        track_visibility='onchange')

    active = fields.Boolean(
        string="Ativo",
        track_visibility='onchange'
    )

    observacoes = fields.Text(
        string="Observações",
        track_visibility='onchange'
    )

    valor = fields.Float(
        string="Valor",
        required=True,
        track_visibility='onchange'
    )

    repeticoes = fields.Integer(
        string="Repetições",
        track_visibility='onchange'
    )

    repeticoes_executadas = fields.Integer(
        string="Repetições Executadas",
        track_visibility='onchange'
    )

    contrato = fields.Many2one(
        string="Contrato",
        comodel_name='account.analytic.account',
        required=True,
        track_visibility='onchange')

