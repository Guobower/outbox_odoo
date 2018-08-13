# -*- coding: utf-8 -*-

from openerp import api
from openerp import fields
from openerp import models

class Remessa_bancaria(models.Model):
    _name = 'remessa_bancaria'
    _description = 'Remessa bancaria para registro de boletos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
                       string="Nome",
                       size=150,
                       required=True,
                       track_visibility='onchange')
                       
    empresa = fields.Many2one(
                              string='Empresa Emitente',
                              help='Empresa emissora dos boletos',
                              comodel_name='res.company',
                              required=True,
                              track_visibility='onchange')
    
    faturas = fields.Many2many(
                               comodel_name='account.invoice',
                               string='Faturas de Clientes',
                               help='Selecione as faturas de clientes que farão parte desse lote',
                               track_visibility='onchange')
    
    remessa_gerada = fields.Boolean(
                                    string="Remessa Gerada",
                                    help='Remessa já gerada no sistema',
                                    track_visibility='onchange')

    total_registros_lote = fields.Integer(
        string="Total de registros do lote"
    )
    
    def gerar_remessa(self, cr, user, ids, context=None):
        import base64
        from datetime import datetime
        import pytz

        remessa_bancaria = self.pool.get('remessa_bancaria').browse(cr, user, ids[0])

        if remessa_bancaria.remessa_gerada:
            remessa_bancaria.write({'total_registros_lote': 0})
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Remessa já gerada!',
                    'text': 'Verifique o anexo para baixar a remessa',
                    'sticky': True
                    }
            }
        else:
            conteudo_remessa = self.header_arquivo(remessa_bancaria)
            conteudo_remessa += self.header_lote(remessa_bancaria)
            conteudo_remessa += self.segmento_p(remessa_bancaria)
            conteudo_remessa += self.trailer_lote(remessa_bancaria)
            conteudo_remessa += self.trailer_arquivo(remessa_bancaria)

            attach_obj = self.pool.get('ir.attachment')
            context.update({'default_res_id': ids[0], 'default_res_model': 'remessa_bancaria'})

            hoje = datetime.now(pytz.timezone(context["tz"]))

            attach_obj.create(cr, user, {'name': 'Arquivo_remessa_'+hoje.strftime('%d-%m-%Y')+'.rem',
                                         'datas': base64.encodestring(conteudo_remessa),
                                         'datas_fname': 'teste.txt'}, context=context)

            remessa_bancaria.write({'remessa_gerada': True})


    def header_arquivo(self, remessa_bancaria):
        from datetime import datetime, timedelta

        header_arquivo = ""

        # Código do Banco na Compensação - 1 a 3
        header_arquivo += self.escrever_campo("001", 3, "N")

        # Lote de Serviço - 4 a 7
        header_arquivo += self.escrever_campo("0", 4, "N")

        # Tipo de Registro - 8 a 8
        header_arquivo += self.escrever_campo("0", 1, "N")

        # Uso Exclusivo FEBRABAN / CNAB - 9 a 17
        header_arquivo += self.escrever_campo("", 9, "A")

        # Tipo de Inscrição da Empresa - 18 a 18
        header_arquivo += self.escrever_campo("2", 1, "N")

        # Número de Inscrição da Empresa - 19 a 32
        header_arquivo += self.escrever_campo(self.remover_caracteres(remessa_bancaria.empresa.cnpj_cpf), 14, "N")

        # Número do convênio de cobrança BB - 33 a 41
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].codigo_da_empresa, 9, "N")

        # Cobrança Cedente BB - 42 a 45
        header_arquivo += self.escrever_campo("0014", 4, "N")

        # Número da carteira de cobrança BB - 46 a 47
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].carteira, 2, "N")

        # Número da variação da carteira de cobrança BB - 48 a 50
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].variacao_carteira, 3, "N")

        # Campo reservado BB - 51 a 52
        header_arquivo += self.escrever_campo("", 2, "A")

        # Agência Mantenedora da Conta - 53 a 57
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_number, 5, "N")

        # Dígito Verificador da Agência - 58 a 58
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_number_dig, 1, "A")

        # Número da Conta Corrente - 59 a 70
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].acc_number, 12, "N")

        # Dígito Verificador da Conta - 71 a 71
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].acc_number_dig, 1, "A")

        # Dígito Verificador da Ag/Conta - 72 a 72
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_acc_dig, 1, "A")

        # Nome da Empresa - 73 a 102
        header_arquivo += self.escrever_campo(remessa_bancaria.empresa.name, 30, "A")

        # Nome do Banco - 103 a 132
        header_arquivo += self.escrever_campo("BANCO DO BRASIL", 30, "A")

        # Uso Exclusivo FEBRABAN / CNAB - 133 a 142
        header_arquivo += self.escrever_campo("", 10, "A")

        # Código Remessa / Retorno - 143 a 143
        header_arquivo += self.escrever_campo("1", 1, "N")

        # Data de Geração do Arquivo - 144 a 151
        data_hora_geracao = datetime.strptime(remessa_bancaria.create_date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        header_arquivo += self.escrever_campo(data_hora_geracao.strftime('%d%m%Y'), 8, "N")

        # Hora de Geração do Arquivo - 152 a 157
        header_arquivo += self.escrever_campo(data_hora_geracao.strftime('%H%M%S'), 6, "N")

        # Número Seqüencial do Arquivo - 158 a 163
        header_arquivo += self.escrever_campo("0", 6, "N")

        # No da Versão do Layout do Arquivo - 164 a 166
        header_arquivo += self.escrever_campo("0", 3, "N")

        # Densidade de Gravação do Arquivo - 167 a 171
        header_arquivo += self.escrever_campo("0", 5, "N")

        # Para Uso Reservado do Banco - 172 a 191
        header_arquivo += self.escrever_campo("", 20, "A")

        # Para Uso Reservado da Empresa - 192 a 211
        header_arquivo += self.escrever_campo("", 20, "A")

        # Uso Exclusivo FEBRABAN / CNAB - 212 a 240
        header_arquivo += self.escrever_campo("", 29, "A")

        return header_arquivo

    def header_lote(self, remessa_bancaria):
        from datetime import datetime, timedelta

        #self.computar_total_lote(remessa_bancaria)
        header_lote = "\n"

        # Código do Banco na Compensação - 1 a 3
        header_lote += self.escrever_campo("001", 3, "N")

        # Lote de Serviço - 4 a 7
        header_lote += self.escrever_campo("0001", 4, "N")

        # Tipo de Registro - 8 a 8
        header_lote += self.escrever_campo("1", 1, "N")

        # Tipo de Operação - 9 a 9
        header_lote += self.escrever_campo("R", 1, "A")

        # Tipo de Serviço - 10 a 11
        header_lote += self.escrever_campo("01", 2, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 12 a 13
        header_lote += self.escrever_campo("", 2, "A")

        # No da Versão do Layout do Lote - 14 a 16
        header_lote += self.escrever_campo("042", 3, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 17 a 17
        header_lote += self.escrever_campo("", 1, "A")

        # Tipo de Inscrição da Empresa - 18 a 18
        header_lote += self.escrever_campo("2", 1, "N")

        # No de Inscrição da Empresa - 19 a 33
        header_lote += self.escrever_campo(self.remover_caracteres(remessa_bancaria.empresa.cnpj_cpf), 15, "N")

        # Nùmero do convênio de cobrança BB - 34 a 42
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].codigo_da_empresa, 9, "N")

        # Cobrança Cedente BB - 43 a 46
        header_lote += self.escrever_campo("0014", 4, "N")

        # Número da carteira de cobrança BB - 47 a 48
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].carteira, 2, "N")

        # Número da variação da carteira de cobrança BB - 49 a 51
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].variacao_carteira, 3, "N")

        # Campo que identifica remessa de testes - 52 a 53
        header_lote += self.escrever_campo("", 2, "A")

        # Agência Mantenedora da Conta - 54 a 58
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_number, 5, "N")

        # Dígito Verificador da Agência - 59 a 59
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_number_dig, 1, "A")

        # Número da Conta Corrente - 60 a 71
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].acc_number, 12, "N")

        # Dígito Verificador da Conta - 72 a 72
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].acc_number_dig, 1, "A")

        # Dígito Verificador da Ag/Conta - 73 a 73
        header_lote += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_acc_dig, 1, "A")

        # Nome da Empresa - 74 a 103
        header_lote += self.escrever_campo(remessa_bancaria.empresa.name, 30, "A")

        # Mensagem 1 - 104 a 143
        header_lote += self.escrever_campo("", 40, "A")

        # Mensagem 2 - 144 a 183
        header_lote += self.escrever_campo("", 40, "A")

        # Número Remessa/Retorno - 184 a 191
        header_lote += self.escrever_campo("0", 8, "N")

        # Data de Gravação Remessa/Retorno - 192 a 199
        data_hora_geracao = datetime.strptime(remessa_bancaria.create_date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        header_lote += self.escrever_campo(data_hora_geracao.strftime('%d%m%Y'), 8, "N")

        # Data do Crédito - 200 a 207
        header_lote += self.escrever_campo("", 8, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 208 a 240
        header_lote += self.escrever_campo("", 33, "A")

        return header_lote

    def segmento_p(self, remessa_bancaria):
        from datetime import datetime, timedelta

        segmento_p = ""

        for index, fatura in enumerate(remessa_bancaria.faturas):
            self.computar_total_lote(remessa_bancaria)
            segmento_p += "\n"

            # Código do Banco na Compensação - 1 a 3
            segmento_p += self.escrever_campo("001", 3, "N")

            # Lote Lote de Serviço - 4 a 7
            segmento_p += self.escrever_campo("0001", 4, "N")

            # Tipo de Registro - 8 a 8
            segmento_p += self.escrever_campo("3", 1, "N")

            # No Sequencial do Registro no Lote - 9 a 13
            #segmento_p += self.escrever_campo(str(index + 1), 5, "N")
            segmento_p += self.escrever_campo(str(remessa_bancaria.total_registros_lote), 5, "N")

            # Cód. Segmento do Registro Detalhe - 14 a 14
            segmento_p += self.escrever_campo("P", 1, "A")

            # Uso Exclusivo FEBRABAN/CNAB - 15 a 15
            segmento_p += self.escrever_campo("", 1, "A")

            # Código de Movimento Remessa - 16 a 17
            segmento_p += self.escrever_campo("01", 2, "N")

            # Agência Mantenedora da Conta - 18 a 22
            segmento_p += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_number, 5, "N")

            # Dígito Verificador da Agência - 23 a 23
            segmento_p += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_number_dig, 1, "A")

            # Número da Conta Corrente - 24 a 35
            segmento_p += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].acc_number, 12, "N")

            # Dígito Verificador da Conta - 36 a 36
            segmento_p += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].acc_number_dig, 1, "A")

            # Dígito Verificador da Ag/Conta - 37 a 37
            segmento_p += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].bra_acc_dig, 1, "A")

            # Identificação do Título no Banco - 38 a 57
            segmento_p += self.escrever_campo(remessa_bancaria.empresa.bank_ids[0].codigo_da_empresa, 7, "A")
            segmento_p += self.escrever_campo(str(fatura.id), 10, "N")
            segmento_p += self.escrever_campo("", 3, "A")

            # Código da Carteira - 58 a 58
            segmento_p += self.escrever_campo("1", 1, "N")

            # Forma de Cadastr. do Título no Banco - 59 a 59
            segmento_p += self.escrever_campo("1", 1, "N")

            # Tipo de Documento - 60 a 60
            segmento_p += self.escrever_campo("1", 1, "A")

            # Identificação da Emissão do Bloqueto - 61 a 61
            segmento_p += self.escrever_campo("2", 1, "N")

            # Identificação da Distribuição - 62 a 62
            segmento_p += self.escrever_campo("2", 1, "A")

            # Número do Documento de Cobrança - 63 a 77
            segmento_p += self.escrever_campo(str(fatura.id), 15, "A")

            # Data de Vencimento do Título - 78 a 85
            data_vencimento = datetime.strptime(fatura.date_due, '%Y-%m-%d')
            segmento_p += self.escrever_campo(data_vencimento.strftime('%d%m%Y'), 8, "N")

            # Valor Nominal do Título - 86 a 100
            segmento_p += self.escrever_campo(self.remover_caracteres(str('%.2f' % fatura.amount_total)), 15, "N")

            # Agência Encarregada da Cobrança - 101 a 105
            segmento_p += self.escrever_campo("0", 5, "N")

            # Dígito Verificador da Agência - 106 a 106
            segmento_p += self.escrever_campo("", 1, "A")

            # Espécie do Título - 107 a 108
            segmento_p += self.escrever_campo("02", 2, "N")

            # Identific. de Título Aceito/Não Aceito - 109 a 109
            segmento_p += self.escrever_campo("A", 1, "A")

            # Data da Emissão do Título - 110 a 117
            data_emissao = datetime.strptime(fatura.date_invoice, '%Y-%m-%d')
            segmento_p += self.escrever_campo(data_emissao.strftime('%d%m%Y'), 8, "N")

            # Código do Juros de Mora - 118 a 118
            segmento_p += self.escrever_campo("2", 1, "N")

            # Data do Juros de Mora - 119 a 126
            data_juros = data_vencimento + timedelta(days=1)
            segmento_p += self.escrever_campo(data_juros.strftime('%d%m%Y'), 8, "N")

            # Juros de Mora por Dia/Taxa - 127 a 141
            segmento_p += self.escrever_campo("100", 15, "N")

            # Código do Desconto 1 - 142 a 142
            segmento_p += self.escrever_campo("0", 1, "N")

            # Data do Desconto 1 - 143 a 150
            segmento_p += self.escrever_campo("0", 8, "N")

            # Desconto 1 Valor/Percentual a ser Concedido - 151 a 165
            segmento_p += self.escrever_campo("0", 15, "N")

            # Valor do IOF a ser Recolhido - 166 a 180
            segmento_p += self.escrever_campo("0", 15, "N")

            # Valor do Abatimento - 181 a 195
            segmento_p += self.escrever_campo("0", 15, "N")

            # Identificação do Título na Empresa - 196 a 220
            segmento_p += self.escrever_campo(str(fatura.id), 25, "A")

            # Código para Protesto - 221 a 221
            segmento_p += self.escrever_campo("3", 1, "N")

            # Número de Dias para Protesto - 222 a 223
            segmento_p += self.escrever_campo("0", 2, "N")

            # Código para Baixa/Devolução - 224 a 224
            segmento_p += self.escrever_campo("0", 1, "N")

            # Número de Dias para Baixa/Devolução - 225 a 227
            segmento_p += self.escrever_campo("0", 3, "A")

            # Código da Moeda - 228 a 229
            segmento_p += self.escrever_campo("09", 2, "N")

            # No do Contrato da Operação de Créd. - 230 a 239
            segmento_p += self.escrever_campo("0", 10, "N")

            # Uso Exclusivo FEBRABAN/CNAB - 240 a 240
            segmento_p += self.escrever_campo("", 1, "A")

            # Complementando com o segmento Q
            segmento_p += self.segmento_q(fatura, remessa_bancaria)

            # Complementando com o segmento R
            segmento_p += self.segmento_r(remessa_bancaria)

            # Confirmando saída para registro na fatura
            self.confirmar_saida_registro(fatura, remessa_bancaria)

        return segmento_p

    def segmento_q(self, fatura, remessa_bancaria):
        self.computar_total_lote(remessa_bancaria)
        segmento_q = "\n"

        # Código do Banco na Compensação - 1 a 3
        segmento_q += self.escrever_campo("001", 3, "N")

        # Lote de Serviço - 4 a 7
        segmento_q += self.escrever_campo("0001", 4, "N")

        # Tipo de Registro - 8 a 8
        segmento_q += self.escrever_campo("3", 1, "N")

        # No Sequencial do Registro no Lote - 9 a 13
        segmento_q += self.escrever_campo(str(remessa_bancaria.total_registros_lote), 5, "N")

        # Cód. Segmento do Registro Detalhe - 14 a 14
        segmento_q += self.escrever_campo("Q", 1, "A")

        # Uso Exclusivo FEBRABAN/CNAB - 15 a 15
        segmento_q += self.escrever_campo("", 1, "A")

        # Código de Movimento Remessa - 16 a 17
        segmento_q += self.escrever_campo("01", 2, "N")

        # Tipo de Inscrição - 18 a 18
        if fatura.partner_id.is_company:
            tipo_inscricao = '2'
        else:
            tipo_inscricao = '1'
        segmento_q += self.escrever_campo(tipo_inscricao, 1, "N")

        # Número de Inscrição - 19 a 33
        segmento_q += self.escrever_campo(self.remover_caracteres(fatura.partner_id.cnpj_cpf), 15, "N")

        # Nome - 34 a 73
        segmento_q += self.escrever_campo(fatura.partner_id.name, 40, "A")

        # Endereço - 74 a 113
        segmento_q += self.escrever_campo(fatura.partner_id.street, 40, "A")

        # Bairro - 114 a 128
        segmento_q += self.escrever_campo(fatura.partner_id.district, 15, "A")

        # CEP - 129 a 133
        if fatura.partner_id.zip:
            cep = fatura.partner_id.zip[0:5]
            sufixo_cep = fatura.partner_id.zip[6:9]
        segmento_q += self.escrever_campo(cep, 5, "N")

        # Sufixo do CEP - 134 a 136
        segmento_q += self.escrever_campo(sufixo_cep, 3, "N")

        # Cidade - 137 a 151
        segmento_q += self.escrever_campo(fatura.partner_id.l10n_br_city_id.name, 15, "A")

        # Unidade da Federação - 152 a 153
        segmento_q += self.escrever_campo(fatura.partner_id.state_id.code, 2, "A")

        # Tipo de Inscrição - 154 a 154
        segmento_q += self.escrever_campo("0", 1, "N")

        # Número de Inscrição - 155 a 169
        segmento_q += self.escrever_campo("0", 15, "N")

        # Nome do Sacador/Avalista - 170 a 209
        segmento_q += self.escrever_campo("", 40, "A")

        # Cód. Bco. Corresp. na Compensação - 210 a 212
        segmento_q += self.escrever_campo("0", 3, "N")

        # Nosso No no Banco Correspondente - 213 a 232
        segmento_q += self.escrever_campo("", 20, "A")

        # Uso Exclusivo FEBRABAN/CNAB - 233 a 240
        segmento_q += self.escrever_campo("", 8, "A")

        return segmento_q

    def segmento_r(self, remessa_bancaria):
        self.computar_total_lote(remessa_bancaria)
        segmento_r = "\n"

        # Código do Banco na Compensação - 1 a 3
        segmento_r += self.escrever_campo("001", 3, "N")

        # Lote de Serviço - 4 a 7
        segmento_r += self.escrever_campo("0001", 4, "N")

        # Tipo de Registro - 8 a 8
        segmento_r += self.escrever_campo("3", 1, "N")

        # No Sequencial do Registro no Lote - 9 a 13
        segmento_r += self.escrever_campo(str(remessa_bancaria.total_registros_lote), 5, "N")

        # Cód. Segmento do Registro Detalhe - 14 a 14
        segmento_r += self.escrever_campo("R", 1, "A")

        # Uso Exclusivo FEBRABAN/CNAB - 15 a 15
        segmento_r += self.escrever_campo("", 1, "A")

        # Código de Movimento Remessa - 16 a 17
        segmento_r += self.escrever_campo("01", 2, "N")

        # Código do Desconto 2 - 18 a 18
        segmento_r += self.escrever_campo("", 1, "N")

        # Data do Desconto 2 - 19 a 26
        segmento_r += self.escrever_campo("", 8, "N")

        # Desconto 2 Valor/Percentual a ser Concedido - 27 a 41
        segmento_r += self.escrever_campo("", 15, "N")

        # Código do Desconto 3 - 42 a 42
        segmento_r += self.escrever_campo("", 1, "N")

        # Data do Desconto 3 - 43 a 50
        segmento_r += self.escrever_campo("", 8, "N")

        # Desconto 3 Valor/Percentual a Ser Concedido - 51 a 65
        segmento_r += self.escrever_campo("", 15, "N")

        # Código da Multa - 66 a 66
        segmento_r += self.escrever_campo("0", 1, "A")

        # Data da Multa - 67 a 74
        segmento_r += self.escrever_campo("", 8, "N")

        # Valor/Percentual a Ser Aplicado - 75 a 89
        segmento_r += self.escrever_campo("", 15, "N")

        # Informação ao Sacado - 90 a 99
        segmento_r += self.escrever_campo("", 10, "A")

        # Mensagem 3 - 100 a 139
        segmento_r += self.escrever_campo("", 40, "A")

        # Mensagem 4 - 140 a 179
        segmento_r += self.escrever_campo("", 40, "A")

        # Uso Exclusivo FEBRABAN/CNAB - 180 a 199
        segmento_r += self.escrever_campo("", 20, "A")

        # Cód. Ocor. do Sacado - 200 a 207
        segmento_r += self.escrever_campo("", 8, "N")

        # Cód. do Banco na Conta do Débito - 208 a 210
        segmento_r += self.escrever_campo("", 3, "N")

        # Código da Agência do Débito - 211 a 215
        segmento_r += self.escrever_campo("", 5, "N")

        # Verificador da Agência - 216 a 216
        segmento_r += self.escrever_campo("", 1, "A")

        # Conta Corrente para Débito - 217 a 228
        segmento_r += self.escrever_campo("", 12, "N")

        # Dígito Verificador da Conta - 229 a 229
        segmento_r += self.escrever_campo("", 1, "A")

        # Dígito Verificador Ag/Conta - 230 a 230
        segmento_r += self.escrever_campo("", 1, "A")

        # Aviso para Débito Automático - 231 a 231
        segmento_r += self.escrever_campo("", 1, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 232 a 240
        segmento_r += self.escrever_campo("", 9, "A")


        return segmento_r

    def trailer_lote(self, remessa_bancaria):
        self.computar_total_lote(remessa_bancaria)
        trailer_lote = "\n"

        # Código do Banco na Compensação - 1 a 3
        trailer_lote += self.escrever_campo("001", 3, "N")

        # Lote de Serviço - 4 a 7
        trailer_lote += self.escrever_campo("0001", 4, "N")

        # Tipo de Registro - 8 a 8
        trailer_lote += self.escrever_campo("5", 1, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 9 a 17
        trailer_lote += self.escrever_campo("", 9, "A")

        # Quantidade de Registros do Lote - 18 a 23
        trailer_lote += self.escrever_campo(str(remessa_bancaria.total_registros_lote + 1), 6, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 24 a 240
        trailer_lote += self.escrever_campo("", 217, "A")


        return trailer_lote

    def trailer_arquivo(self, remessa_bancaria):
        self.computar_total_lote(remessa_bancaria)
        trailer_arquivo = "\n"

        # Código do Banco na Compensação - 1 a 3
        trailer_arquivo += self.escrever_campo("001", 3, "N")

        # Lote de Serviço - 4 a 7
        trailer_arquivo += self.escrever_campo("9999", 4, "N")

        # Tipo de Registro - 8 a 8
        trailer_arquivo += self.escrever_campo("9", 1, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 9 a 17
        trailer_arquivo += self.escrever_campo("", 9, "A")

        # Quantidade de Lotes do Arquivo - 18 a 23
        trailer_arquivo += self.escrever_campo("1", 6, "N")

        # Quantidade de Registros do Arquivo - 24 a 29
        trailer_arquivo += self.escrever_campo(str(remessa_bancaria.total_registros_lote + 2), 6, "N")

        # Qtde de Contas p/ Conc. (Lotes) - 30 a 35
        trailer_arquivo += self.escrever_campo("", 6, "N")

        # Uso Exclusivo FEBRABAN/CNAB - 36 a 240
        trailer_arquivo += self.escrever_campo("", 205, "A")

        trailer_arquivo += "\n"

        return trailer_arquivo

    def escrever_campo(self, conteudo, tamanho, tipo):
        from unicodedata import normalize

        if tipo == 'A':
            #conteudo = conteudo.strip().encode('ascii', 'ignore').decode('ascii')
            conteudo = normalize('NFKD', conteudo.strip().decode('utf-8')).encode('ASCII', 'ignore')
            return conteudo.ljust(tamanho)[0:tamanho]
        elif tipo == 'N':
            return conteudo.rjust(tamanho, '0')[0:tamanho]

    def remover_caracteres(self, texto):
        return texto.replace('-','').replace('.','').replace('/','').replace(':','')

    def confirmar_saida_registro(self, fatura, remessa_bancaria):
        fatura.write({'remessa_bancaria': remessa_bancaria.id})

    def gerar_remessa_php(self, cr, user, ids, context=None):
        url = 'http://cinte.com.br/CnabPHP/index.php?remessa='+str(ids[0])

        res = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }

        return res

    def computar_total_lote(self, remessa_bancaria):
        remessa_bancaria.write({'total_registros_lote': remessa_bancaria.total_registros_lote + 1})

    
    def gerar_array_faturas(self, obj_faturas):
        retorno = list()
        
        for item in obj_faturas:
            if item.partner_id.is_company:
                cpf_cnpj_tipo = 'cnpj'
            else:
                cpf_cnpj_tipo = 'cpf'
            valores = {
                'nosso_numero':item.id
            }
            retorno.append(valores)
        
        return retorno
    
    def registrar_pagamentos(self, cr, user, ids, context=None):
        invoice = self.pool.get('account.invoice').browse(cr, user, 2241) 
        
        if not invoice.state == "open":
            return 
        
        payable_amount = 1 # The amount you want to pay
        
        voucher = self.pool.get("account.voucher").create(cr, user, {
                                                          "name": "",
                                                          "amount": payable_amount,
                                                          "journal_id": self.pool.get("account.journal").search(cr, user, [("type", "=", "bank")], limit=1)[0],
                                                          "account_id": invoice.partner_id.property_account_receivable.id,
                                                          "period_id": self.pool.get("account.voucher")._get_period(cr, user),
                                                          "partner_id": invoice.partner_id.id,
                                                          "type": "receipt"
                                                          }, context)
        
        print "voucheeer " + str(invoice.partner_id.property_account_receivable.id)
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