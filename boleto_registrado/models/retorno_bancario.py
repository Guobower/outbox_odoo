# -*- coding: utf-8 -*-

from openerp import api
from openerp import fields
from openerp import models
import datetime

class Retorno_bancario(models.Model):
    _name = 'retorno_bancario'
    _description = 'Retorno do banco dos status dos boletos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _defaults = {
        'name': datetime.date.today()
        }
        
    name = fields.Date(
                       string="Retorno",
                       required=True,
                       track_visibility='onchange')

    arquivo_retorno = fields.Binary(
        string='Arquivo de Retorno',
        help='Arquivo de retorno enviado pelo banco.')

    arquivo_retorno_filename = fields.Char("Arquivo de Retorno",
                                  track_visibility='onchange')
    
    item_retorno_bancario = fields.One2many(
                               comodel_name='item_retorno_bancario',
                               string='Itens do Retorno',
                               inverse_name='retorno_bancario',
                               track_visibility='onchange')
                               
    retorno_lido = fields.Boolean(
                                    string="Retorno Lido",
                                    help='Retorno já lido pelo sistema',
                                    track_visibility='onchange')

    def ler_arquivo_retorno(self, cr, user, ids, context=None):
        retorno_bancario = self.pool.get('retorno_bancario').browse(cr, user, ids[0])

        linhas = retorno_bancario.arquivo_retorno.decode('base64').split('\n')

        for linha in linhas:
            try:
                if linha[13] == 'T':
                    nosso_numero = self.ler_nosso_numero(linha).strip()
                    numero_documento = self.ler_numero_documento(linha).strip()
                elif linha[13] == 'U':
                    valor_recebido = self.ler_valor_recebido(linha)
                    retorno = self.ler_retorno(linha)
                    data_ocorrencia = self.ler_data_ocorrencia(linha)

                    self.pool.get('item_retorno_bancario').create(cr, user, {'retorno_bancario': retorno_bancario.id, 'name': nosso_numero, 'numero_documento': numero_documento, 'valor_recebido': valor_recebido, 'retorno': retorno, 'data_ocorrencia': data_ocorrencia})
                    if numero_documento:
                            invoices = self.pool.get('account.invoice').search(cr, user, [('id', '=', int(numero_documento))])
                            if len(invoices) > 0:
                                if retorno in ("06", "17"):
                                    self.registrar_pagamentos(cr, user, self.pool.get('account.invoice').browse(cr, user, invoices[0]))

                                fatura = self.pool.get('account.invoice').browse(cr, user, invoices[0])
                                fatura.write({'status_banco': retorno})

            except IndexError:
                break

    def ler_nosso_numero(self, linha):
        return linha[37:57]

    def ler_numero_documento(self, linha):
        return linha[58:73]

    def ler_valor_recebido(self, linha):
        return linha[92:105]+"."+linha[105:107]

    def ler_retorno(self, linha):
        return linha[15:17]

    def ler_data_ocorrencia(self, linha):
        return linha[141:145] + "-" + linha[139:141] + "-" + linha[137:139]

    def registrar_pagamentos(self, cr, user, invoice, context=None):
        if not invoice.state == "open":
            return 
        
        payable_amount = invoice.amount_total # The amount you want to pay
        
        voucher = self.pool.get("account.voucher").create(cr, user, {
                                                          "name": "",
                                                          "amount": payable_amount,
                                                          "journal_id": self.pool.get("account.journal").search(cr, user, [("type", "=", "bank")], limit=1)[0],
                                                          "account_id": invoice.partner_id.property_account_receivable.id,
                                                          "period_id": self.pool.get("account.voucher")._get_period(cr, user),
                                                          "partner_id": invoice.partner_id.id,
                                                          "type": "receipt"
                                                          }, context)
        
        voucher_obj = self.pool.get('account.voucher').browse(cr, user, voucher)
        voucher_line = self.pool.get("account.voucher.line").create(cr, user, {
                                                                    "name": "",
                                                                    "payment_option": "without_writeoff",
                                                                    "amount": payable_amount,
                                                                    "voucher_id": voucher,
                                                                    "partner_id": invoice.partner_id.id,
                                                                    "account_id": invoice.partner_id.property_account_receivable.id,
                                                                    "type": "cr",
                                                                    "move_line_id": invoice.move_id.line_id[0].id,
                                                                    }, context)
        voucher_obj.signal_workflow("proforma_voucher")
        
        pass