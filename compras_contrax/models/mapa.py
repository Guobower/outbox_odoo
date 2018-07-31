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

    ordem_fornecedor2 = fields.Many2one(
        comodel_name="purchase.order",
        string="Ordem do Fornecedor 2",
        track_visibility='onchange')

    ordem_fornecedor3 = fields.Many2one(
        comodel_name="purchase.order",
        string="Ordem do Fornecedor 3",
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

    def on_change_cotacao(self, cr, user, ids, cotacao, context=None):
        if cotacao:
            cotacao_obj = self.pool.get('purchase.order').browse(cr, user, cotacao)

            res = {
                'value': {
                    'fornecedor1': cotacao_obj.partner_id.id
                }
            }
            return res

    def gerar_mapa(self, cr, user, ids, context=None):
        mapa = self.pool.get('mapa').browse(cr, user, ids[0])

        for item in mapa.name.order_line:
            dados_item_mapa = {
                'name': item.product_id.id,
                'quantidade': item.product_qty,
                'mapa': ids[0]
            }

            self.pool.get('item_mapa').create(cr, user, dados_item_mapa)

    def duplicar_solicitacoes(self, cr, user, ids, context=None):
        mapa = self.pool.get('mapa').browse(cr, user, ids[0])

        if mapa.name:
            if mapa.fornecedor2:
                if not mapa.ordem_fornecedor2:
                    copy_id = self.pool.get('purchase.order').copy(cr, user, mapa.name.id, {'partner_id': mapa.fornecedor2.id})
                    mapa.write({'ordem_fornecedor2': copy_id})
            if mapa.fornecedor3:
                if not mapa.ordem_fornecedor3:
                    copy_id = self.pool.get('purchase.order').copy(cr, user, mapa.name.id, {'partner_id': mapa.fornecedor3.id})
                    mapa.write({'ordem_fornecedor3': copy_id})

    def gerar_ordens(self, cr, user, ids, context=None):
        mapa = self.pool.get('mapa').browse(cr, user, ids[0])

        self.remover_itens(mapa.name)
        self.remover_itens(mapa.ordem_fornecedor2)
        self.remover_itens(mapa.ordem_fornecedor3)

        for item in mapa.item_mapa:
            if item.fornecedor_escolhido == '1':
                self.remover_itens(mapa.ordem_fornecedor2, item.name)
                self.remover_itens(mapa.ordem_fornecedor3, item.name)
            elif item.fornecedor_escolhido == '2':
                self.remover_itens(mapa.name, item.name)
                self.remover_itens(mapa.ordem_fornecedor3, item.name)
            elif item.fornecedor_escolhido == '3':
                self.remover_itens(mapa.name, item.name)
                self.remover_itens(mapa.ordem_fornecedor2, item.name)

    def remover_itens(self, ordem, produto):
        for item in ordem.order_line:
            if item.product_id == produto.id:
                item.unlink()


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
        string="Fornecedor 1 - Total",
    )

    total_fornecedor2 = fields.Float(
        string="Fornecedor 2 - Total",
    )

    total_fornecedor3 = fields.Float(
        string="Fornecedor 3 - Total",
    )

    fornecedor_indicado = fields.Selection(
        selection=[('1', 'Fornecedor 1'),
                   ('2', 'Fornecedor 2'),
                   ('3', 'Fornecedor 3')],
        string="Fornecedor Indicado",
        help="Fornecedor indicado pelo sistema para a compra",
        track_visibility="onchange"
    )

    fornecedor_escolhido = fields.Selection(
        selection=[('1', 'Fornecedor 1'),
                   ('2', 'Fornecedor 2'),
                   ('3', 'Fornecedor 3')],
        string="Fornecedor Escolhido",
        help="Fornecedor escolhido para a compra",
        track_visibility='onchange'
    )

    justificativa = fields.Text(
        string="Justificativa",
        track_visibility="onchange"
    )

    fornecedor1 = fields.Char('Fornecedor 1', related='mapa.fornecedor1.name', store=True)

    fornecedor2 = fields.Char('Fornecedor 2', related='mapa.fornecedor2.name', store=True)

    fornecedor3 = fields.Char('Fornecedor 3', related='mapa.fornecedor3.name', store=True)

    def on_change_valor_fornecedor(self, cr, user, ids, quantidade, valor_fornecedor1, valor_fornecedor2,
                                   valor_fornecedor3, context=None):
        total_fornecedor1 = quantidade * valor_fornecedor1
        total_fornecedor2 = quantidade * valor_fornecedor2
        total_fornecedor3 = quantidade * valor_fornecedor3

        item_mapa_obj = self.pool.get('item_mapa').browse(cr, user, ids[0])

        menor_valor = total_fornecedor1
        fornecedor_indicado = '1'

        if total_fornecedor2 < menor_valor and total_fornecedor2 > 0:
            menor_valor = total_fornecedor2
            fornecedor_indicado = '2'

        if total_fornecedor3 < menor_valor and total_fornecedor3 > 0:
            fornecedor_indicado = '3'

        dados_item = {
                'total_fornecedor1': total_fornecedor1,
                'total_fornecedor2': total_fornecedor2,
                'total_fornecedor3': total_fornecedor3,
                'fornecedor_indicado': fornecedor_indicado
            }

        item_mapa_obj.write(dados_item)

        res = {
            'value': dados_item
        }
        return res