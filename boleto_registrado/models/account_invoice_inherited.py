# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models
import datetime

class Account_invoice_inherited(models.Model):
    _inherit = 'account.invoice' 

    remessa_bancaria = fields.Many2one(
                                       string='Remessa de Saída',
                                       help='Remessa de saída para o banco',
                                       comodel_name='remessa_bancaria',
                                       track_visibility='onchange')
                              
    status_banco = fields.Selection(
                                    selection=[('02', 'Entrada Confirmada'),
                                    ('03', 'Entrada Rejeitada'),
                                    ('04', 'Transferência de Carteira/Entrada'),
                                    ('05', 'Transferência de Carteira/Baixa'),
                                    ('06', 'Liquidação'),
                                    ('07', 'Confirmação do Recebimento da Instrução de Desconto'),
                                    ('08', 'Confirmação do recebimento do Cancelamento do Desconto'),
                                    ('09', 'Baixa'),
                                    ('11', 'Títulos em Carteira (Em Ser)'),
                                    ('12', 'Confirmação Recebimento Instrução de Abatimento'),
                                    ('13', 'Confirmação Recebimento Instrução de Cancelamento Abatimento'),
                                    ('14', 'Confirmação Recebimento Instrução Alteração de Vencimento'),
                                    ('15', 'Franco de Pagamento'),
                                    ('17', 'Liquidação Após Baixa ou Título Não Registrado'),
                                    ('19', 'Confirmação Recebimento Instrução de Protesto'),
                                    ('20', 'Confirmação Recebimento Instrução de Sustação/Cancelamento de Protesto'),
                                    ('23', 'Remessa a Cartório (Aponte em Cartório)'),
                                    ('24', 'Retirada de Cartório e Manutenção em Carteira'),
                                    ('25', 'Protestado e Baixado (Baixa por ter sido Protestado)'),
                                    ('26', 'Instrução Rejeitada'),
                                    ('27', 'Confirmação do Pedido de Alteração de Outros Dados'),
                                    ('28', 'Débito de Tarifas/Custas'),
                                    ('29', 'Ocorrência do Pagador'),
                                    ('30', 'Alteração de Dados Rejeitada'),
                                    ('33', 'Confirmação de Alteração dos Dados do Rateio de Crédito'),
                                    ('34', 'Confirmação do Cancelamento dos Dados do Rateio de Crédito'),
                                    ('35', 'Confirmação do Desagendamento do Débito Automático'),
                                    ('36', 'Confirmação de envio de e-mail/SMS'),
                                    ('37', 'Envio de e-mail/SMS rejeitado'),
                                    ('38', 'Confirmação de alteração do Prazo Limite de Recebimento'),
                                    ('39', 'Confirmação de Dispensa de Prazo Limite de Recebimento'),
                                    ('40', 'Confirmação da alteração do número do título dado pelo Beneficiário'),
                                    ('41', 'Confirmação da alteração do número controle do Participante'),
                                    ('42', 'Confirmação de alteração dos dados do Pagador'),
                                    ('43', 'Confirmação de alteração dos dados do Sacador/Avalista'),
                                    ('44', 'Título pago com cheque devolvido'),
                                    ('45', 'Título pago com cheque compensado'),
                                    ('46', 'Instrução para cancelar protesto confirmada'),
                                    ('47', 'Instrução para protesto para fins falimentares confirmada'),
                                    ('48', 'Confirmação de instrução de transferência de carteira/modalidade de cobrança'),
                                    ('49', 'Alteração de contrato de cobrança'),
                                    ('50', 'Título pago com cheque pendente de liquidação'),
                                    ('51', 'Título DDA reconhecido pelo Pagador'),
                                    ('52', 'Título DDA não reconhecido pelo Pagador'),
                                    ('53', 'Título DDA recusado pela CIP'),
                                    ('54', 'Confirmação da instrução de Baixa de Título Negativado sem Protesto'),
                                    ('55', 'Confirmação de Pedido de Dispensa de Multa'),
                                    ('56', 'Confirmação de Pedido de Cobrança de Multa'),
                                    ('57', 'Confirmação de Pedido de Alteração de Cobrança de Juros'),
                                    ('58', 'Confirmação de Pedido do Valor/Data de Desconto'),
                                    ('59', 'Confirmação de Pedido de Alteração do beneficiário do Título'),
                                    ('60', 'Confirmação de Pedido de Dispensa do Juros de Mora'),
                                    ('61', 'Confirmação de Alteração do Valor Nominal do Título'),
                                    ('63', 'Título Sustado Judicialmente')],
                                    string="Status no banco",
                                    help="Status atual do boleto no banco",
                                    track_visibility='onchange'
                                    )

    metodo_pagamento = fields.Selection(
        selection=[('1', 'Boleto'),
                   ('2', 'Fatura')],
        string='Método de Pagamento',
        help='Método de pagamento do cliente',
        track_visibility='onchange')

    def validar_faturas(self, cr, user, context=None):
        hoje = datetime.date.today()
        # Buscar contratos que pagam por boleto
        itens_contratos = self.pool.get('account.analytic.account').search(cr, user, [('metodo_pagamento','=','1')])
        print(str(itens_contratos))
        for item_contrato in itens_contratos:
            contrato = self.pool.get('account.analytic.account').browse(cr, user, item_contrato)
            print(str(contrato))
            itens_faturas = self.pool.get('account.invoice').search(cr, user, [('origin', '=', contrato.code), ('date_invoice', '<=', hoje.strftime('%Y-%m-%d')), ('state', '=', 'draft')])
            print(str(itens_faturas))
            for item_fatura in itens_faturas:
                fatura = self.pool.get('account.invoice').browse(cr, user, item_fatura)
                print(str(fatura))
                self.confirmar_fatura(cr, user, fatura, contrato)

    def confirmar_fatura(self, cr, user, fatura, contrato):
        print(str(fatura))
        self.gerar_acrescimos_descontos(cr, user, fatura, contrato)
        fatura.write({'payment_term': contrato.condicao_pagamento.id, 'metodo_pagamento': contrato.metodo_pagamento})
        fatura.action_date_assign()
        fatura.action_move_create()
        fatura.action_number()
        fatura.invoice_validate()

    def gerar_acrescimos_descontos(self, cr, user, fatura, contrato):
        for acrescimo_desconto in contrato.acrescimo_desconto:
            if acrescimo_desconto.repeticoes > acrescimo_desconto.repeticoes_executadas:
                if acrescimo_desconto.name == 'acres':
                    valores = {
                        'product_id': 846,
                        'name': 'ACRESCIMO AGENDADO',
                        'quantity': 1,
                        'price_unit': acrescimo_desconto.valor,
                        'invoice_id': fatura.id
                    }

                    self.pool.get('account.invoice.line').create(cr, user, valores)
                    acrescimo_desconto.write({'repeticoes_executadas': acrescimo_desconto.repeticoes_executadas + 1})
                elif acrescimo_desconto.name == 'desc':
                    valores = {
                        'product_id': 845,
                        'name': 'DESCONTO AGENDADO',
                        'quantity': 1,
                        'price_unit': acrescimo_desconto.valor * -1,
                        'invoice_id': fatura.id
                    }

                    self.pool.get('account.invoice.line').create(cr, user, valores)
                    acrescimo_desconto.write({'repeticoes_executadas': acrescimo_desconto.repeticoes_executadas + 1})

    def imprimir_boleto(self, cr, user, ids, context=None):
        from datetime import datetime, timedelta

        fatura = self.pool.get('account.invoice').browse(cr, user, ids[0])

        hoje = datetime.now()
        data_vencimento = datetime.strptime(fatura.date_due, '%Y-%m-%d')

        disponivel = hoje < data_vencimento + timedelta(days=1)

        if disponivel:
            url = 'http://www.cinte.com.br/2016/boletos/imprimirOdoo.php?id=' + str(ids[0])
            res = {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url,
            }
        else:
            url = 'https://www63.bb.com.br/portalbb/boleto/boletos/hc21e,802,3322,10343.bbx?_ga=2.163848380.2023037881.1506687534-274924826.1502129516&&pk_vid=5ee6db42c6a667aa15066875613fff07'
            res = {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': url,
            }

        return res