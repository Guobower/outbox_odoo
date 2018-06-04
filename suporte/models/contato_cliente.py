# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models


class Contato_cliente(models.Model):
    _name = 'contato_cliente'
    _description = 'Contatos do cliente'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Selection(
                            selection=[('1', 'E-mail'),
                                       ('2', 'Telefone')],
                            string="Tipo de Contato",
                            required=True,
                            help="Lista de contatos extras dos clientes, utilizada para envio de notificações.",
                            track_visibility='onchange')

    contato = fields.Char(
                            string="Contato",
                            size=250,
                            required=True,
                            track_visibility='onchange')

    cliente = fields.Many2one(
                            string="Cliente",
                            comodel_name='res.partner',
                            required=True,
                            help="Cliente ao qual o contato está vinculado")