# -*- coding: utf-8 -*-

from openerp import api
from openerp import fields
from openerp import models

class Item_retorno_bancario(models.Model):
    _name = 'item_retorno_bancario'
    _description = 'Item lido no retorno do banco'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
        
    name = fields.Char(
                       string="Nosso Numero",
                       size=20,
                       required=True,
                       track_visibility='onchange')
    
    numero_documento = fields.Char(
                                   string="Numero do Documento",
                                   size=20,
                                   track_visibility='onchange'
                                   )
    
    valor_recebido = fields.Float(
                                  string="Valor Recebido",
                                  track_visibility='onchange'
                                  )
    
    data_ocorrencia = fields.Date(
                                  string="Data da Ocorrencia",
                                  track_visibility='onchange'
                                  )
    
    retorno_bancario = fields.Many2one(
                                       string="Retorno Bancario",
                                       comodel_name='retorno_bancario',
                                       help="Retorno Bancario ao qual o item está associado")
                                
    retorno = fields.Selection(
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