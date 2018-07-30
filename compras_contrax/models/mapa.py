# -*- coding: utf-8 -*-

from openerp import fields
from openerp import models


class Mapa(models.Model):
    _name = 'mapa'
    _description = 'mapa'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Many2one(
        comodel_name="purchase.order",
        string="Solicitacao",
        required=True,
        track_visibility='onchange')

    fornecedor1 = fields.Many2one(
        comodel_name="res.partner",
        string="Fornecedor 1",
        required=True,
        track_visibility="onchange"
    )

    fornecedor2 = fields.Many2one(
        comodel_name="res.partner",
        string="Fornecedor 2",
        track_visibility="onchange"
    )

    fornecedor3 = fields.Many2one(
        comodel_name="res.partner",
        string="Fornecedor 3",
        track_visibility="onchange"
    )

    item_mapa = fields.One2many(
        comodel_name='item_mapa',
        string='Itens do Mapa',
        inverse_name='mapa',
        track_visibility='onchange')


class Item_mapa(models.Model):
    _name = 'item_mapa'
    _description = 'item_mapa'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Many2one(
        comodel_name="product.product",
        string="Produto",
        required=True,
        track_visibility="onchange"
    )

    mapa = fields.Many2one(
        string="Mapa",
        comodel_name='mapa',
        help="Mapa de cotação ao qual o item está associado")

    quantidade = fields.Float(
        string="Quantidade",
    )

    valor_fornecedor1 = fields.Float(
        string="Fornecedor 1 - Valor",
    )

    valor_fornecedor2 = fields.Float(
        string="Fornecedor 2 - Valor",
    )

    valor_fornecedor3 = fields.Float(
        string="Fornecedor 3 - Valor",
    )

    total_fornecedor1 = fields.Float(
        string="Fornecedor 1 - Valor",
    )

    total_fornecedor2 = fields.Float(
        string="Fornecedor 2 - Valor",
    )

    total_fornecedor3 = fields.Float(
        string="Fornecedor 3 - Valor",
    )

    fornecedor_indicado = fields.Many2one(
        comodel_name="res.partner",
        string="Fornecedor 1",
        required=True,
        track_visibility="onchange"
    )

    fornecedor_escolhido = fields.Many2one(
        comodel_name="res.partner",
        string="Fornecedor 1",
        required=True,
        track_visibility="onchange"
    )

    justificativa = fields.Text(
        string="Justificativa",
        track_visibility="onchange"
    )