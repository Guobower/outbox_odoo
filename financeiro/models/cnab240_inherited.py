# -*- coding: utf-8 -*-
from openerp import models, fields, api, workflow
from datetime import datetime
import unicodedata
import time
import base64

class Cnab240_inherited(models.Model):
    _inherit = 'payment.cnab' 
    
    @api.multi
    def export(self):
        for order_id in self.env.context.get('active_ids', []):

            order = self.env['payment.order'].browse(order_id)
            
            remessa = self.remessa(order)
            suf_arquivo = order.get_next_sufixo()

            if order.mode.type.code == '240':
                self.name = 'CB%s%s.REM' % (
                    time.strftime('%d%m'), str(order.file_number))
            elif order.mode.type.code == '400':
                self.name = 'CB%s%s.REM' % (
                    time.strftime('%d%m'), str(suf_arquivo))
            elif order.mode.type.code == '500':
                self.name = 'PG%s%s.REM' % (
                    time.strftime('%d%m'), str(order.file_number))
            self.state = 'done'
            self.cnab_file = base64.b64encode(remessa)

            self.env['ir.attachment'].create({
                'name': self.name,
                'datas': self.cnab_file,
                'datas_fname': self.name,
                'description': 'Arquivo CNAB 240',
                'res_model': 'payment.order',
                'res_id': order_id
            })
            workflow.trg_validate(self.env.uid, 'payment.order',
                                  order_id, 'done', self.env.cr)

            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'target': 'new',
            }
          
          
            
    def remessa(self, order):
        """

        :param order:
        :return:
        """
        conteudo = ""
        conteudo = conteudo + self.header_arquivo(order)
        conteudo = conteudo + self.header_lote("1")
        conteudo = conteudo + self.detalhes_segmentoA("1")
        conteudo = conteudo + self.trailer_lote("1")
        conteudo = conteudo + self.trailer_arquivo()
        
        remessa = unicode(conteudo)
        return unicodedata.normalize(
            'NFKD', remessa).encode('ascii', 'ignore')
            
    def header_arquivo(self, order):
        
        conteudo = ""
        # Código do Banco na Compensação, 1-3, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Lote de Serviço, 4-7, 4, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                4, "0000"
            )
        
        # Tipo de Registro, 8-8, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "0"
            )
        
        # Uso Exclusivo FEBRABAN/CNAB, 9-17, 9, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                9, ""
            )
        
        # Tipo de Inscrição da Empresa, 18-18, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "2"
            )
        
        # Número de Inscrição da Empresa, 19-32, 14, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                14, "08378641000196"
            )
        
        # Código do Convênio no Banco, 33-52, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, "141006"
            )
        
        # Agência Mantenedora da Conta, 53-57, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "02870"
            )
        
        # Dígito Verificador da Agência, 58-58, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "3"
            )
        
        # Número da Conta Corrente, 59-70, 12, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                12, "000000301432"
            )
        
        # Dígito Verificador da Conta, 71-71, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "0"
            )
        
        # Dígito Verificador da Ag/Conta, 72-72, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "0"
            )
        
        # Nome da Empresa, 73-102, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "CINTE TELECOM COMERCIO E SERVICOS LTDA-EPP"
            )
        
        # Nome do Banco, 103-132, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "BANCO DO BRASIL"
            )
        
        # Uso Exclusivo FEBRABAN/CNAB, 133-142, 10, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                10, ""
            )
        
        # Código Remessa/Retorno, 143-143, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "1"
            )
        
        now = datetime.now()
        dataGeracao = str(self.formatar_numerico(2,now.day))+""+str(self.formatar_numerico(2,now.month))+""+str(self.formatar_numerico(4,now.year))+""

        # Data de Geração do Arquivo, 144-151, 8, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                8, dataGeracao
            )
        
        horaGeracao = str(self.formatar_numerico(2,(now.hour-3)))+""+str(self.formatar_numerico(2,now.minute))+""+str(self.formatar_numerico(2,now.second))+""
        # Hora de Geração do Arquivo, 152-157, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, horaGeracao
            )
        
        # Número Sequencial do Arquivo, 158-163, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, self.formatar_numerico(3,order.reference)
            )
        
        # Nº da Versão do Layout do Arquivo, 164-166, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "087"
            )
        
        # Densidade de Gravação do Arquivo, 167-171, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "00000"
            )
        
        # Para Uso Reservado do Banco, 172-191, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, ""
            )
        
        # Para Uso Reservado da Empresa, 192-211, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, ""
            )
        
        # Uso Exclusivo FEBRABAN/CNAB, 212-240, 29, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                29, ""
            )
        
        return conteudo
    
    def header_lote(self, numero_lote):
        conteudo = ""
        # Código do Banco na Compensação, 1-3, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Lote de Serviço, 4-7, 4, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                4, numero_lote
            )
        
        # Tipo de Registro, 8-8, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "1"
            )
        
        # Tipo da Operação, 9-9, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "R"
            )
        
        # Tipo do Serviço, 10-11, 2, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "98"
            )
        
        # Forma de Lançamento, 12-13, 2, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "30"
            )
        
        # Número da Versão do Layout do Lote, 14-16, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "045"
            )
        
        # Uso Exclusivo FEBRABAN/CNAB, 17-17, 9, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, ""
            )
        
        # Tipo de Inscrição da Empresa, 18-18, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "2"
            )
        
        # Número de Inscrição da Empresa, 19-32, 14, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                14, "08378641000196"
            )
        
        # Código do Convênio no Banco, 33-52, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, "141006"
            )
        
        # Agência Mantenedora da Conta, 53-57, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "02870"
            )
        
        # Dígito Verificador da Agência, 58-58, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "3"
            )
        
        # Número da Conta Corrente, 59-70, 12, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                12, "000000301432"
            )
        
        # Dígito Verificador da Conta, 71-71, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "0"
            )
        
        # Dígito Verificador da Ag/Conta, 72-72, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "0"
            )
        
        # Nome da Empresa, 73-102, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "CINTE TELECOM COMERCIO E SERVICOS LTDA-EPP"
            )
        
        # Mensagem, 103-142, 40, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, ""
            )
        
        # Logradouro, 143-172, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "Rua Doutor Lauro Pinto"
            )
        
        # Número do Local, 173-177, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "610"
            )
        
        # Complemento, 178-192, 15, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                15, "Casa"
            )
        
        # Cidade, 193-212, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, "Natal"
            )
        
        # CEP, 213-217, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "59064"
            )
        
        # Complemento CEP, 218-220, 3, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                3, "250"
            )
        
        # Estado, 221-222, 2, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                2, "RN"
            )
        
        # Indicativo da Forma de Pagamento do Servico, 223-224, 2, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "01"
            )
        
        # Uso Exclusivo Febraban/Cnab, 225-230, 6, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                6, ""
            )
        
        # Códigos das Ocorrências p/Retorno, 231-240, 10, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                10, ""
            )
        
        return conteudo
    
    def detalhes_segmentoA(self, numero_lote):
        conteudo = ""
        # Código do Banco na Compensação, 1-3, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Lote de Serviço, 4-7, 4, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                4, numero_lote
            )
        
        # Tipo de Registro, 8-8, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "3"
            )
        
        # Nº Sequencial do Registro no Lote, 9-13, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, numero_lote
            )
        
        # Código de Segmento do Reg. Detalhe, 14-14, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "A"
            )
        
        # Tipo de Movimento, 15-15, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "0"
            )
        
        # Código da Instrução p/ Movimento, 16-17, 2, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "00"
            )
        
        # Código da Câmara Centralizadora, 18-20, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "018"
            )
        
        # Código do Banco do Favorecido, 21-23, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Ag. Mantenedora da Cta do Favor., 24-28, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "00214"
            )
        
        # Dígito Verificador da Agência, 29-29, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "3"
            )
        
        # Número da Conta Corrente, 30-41, 12, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                12, "000000028437"
            )
        
        # Dígito Verificador da Conta, 42-42, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "8"
            )
        
        # Dígito Verificador da AG/Conta, 43-43, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "8"
            )
        
        # Nome do Favorecido, 44-73, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "Edson Lima Cosme Junior"
            )
        
        # Nº do Documento Atribuído pela Empresa, 74-93, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, "P001"
            )
        
        now = datetime.now()
        dataGeracao = str(self.formatar_numerico(2,now.day))+""+str(self.formatar_numerico(2,now.month))+""+str(self.formatar_numerico(4,now.year))+""
        
        # Data do Pagamento, 94-101, 8, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                8, dataGeracao
            )
        
        # Tipo da Moeda, 102-104, 3, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                3, "BRL"
            )
        
        # Quantidade da Moeda, 105-119, 10, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                10, "0000100000"
            )
        
        # Valor do Pagamento, 120-134, 13, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                13, "0000000000100"
            )
        
        # Nº do Documento Atribuído pelo Banco, 135-154, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, ""
            )
        
        # Data Real da Efetivação Pagto, 155-162, 8, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                8, ""
            )
        
        # Valor Real da Efetivação do Pagto, 163-177, 13, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                13, ""
            )
        
        # Outras Informações, 178-217, 40, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                40, ""
            )
        
        # Compl. Tipo Serviço, 218-219, 2, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                2, "07"
            )
        
        # Código Finalidade da TED, 220-224, 5, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                5, ""
            )
        
        # Complemento de finalidade pagto., 225-226, 2, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                2, ""
            )
        
        # Uso Exclusivo FEBRABAN/CNAB, 227-229, 3, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                3, ""
            )
        
        # Aviso ao Favorecido, 230-230, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "0"
            )
        
        # Códigos das Ocorrências p/ Retorno, 231-240, 10, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                10, ""
            )
        
        return conteudo
    
    def trailer_lote(self, numero_lote):

        conteudo = ""
        # Código do Banco na Compensação, 1-3, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Lote de Serviço, 4-7, 4, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                4, numero_lote
            )
        
        # Tipo de Registro, 8-8, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "5"
            )
        
        # Uso Exclusivo Febraban/Cnab, 9-17, 9, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                9, ""
            )
        
        # Quantidade de Registros do Lote, 18-23, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, "1"
            )
        
        # Somatório dos Valores, 24-41, 16, NUM
        conteudo = conteudo + "0000000000000100" + self.formatar_numerico(
                16, ""
            )
        
        # Somatório de Quantidade de Moedas, 42-59, 13, NUM
        conteudo = conteudo + "0000000100000" + self.formatar_numerico(
                13, ""
            )
        
        # Número Aviso de Débito, 60-65, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, ""
            )
        
        # Uso Exclusivo Febraban/Cnab, 66-230, 165, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                165, ""
            )
        
        # Códigos das Ocorrências para Retorno, 231-240, 10, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                10, ""
            )
        
        return conteudo
    
    
    def header_lote_titulos_cobranca(self, numero_lote):
        conteudo = ""
        # Código do Banco na Compensação, 1-3, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Lote de Serviço, 4-7, 4, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                4, numero_lote
            )
        
        # Tipo de Registro, 8-8, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "1"
            )
        
        # Tipo da Operação, 9-9, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "C"
            )
        
        # Tipo do Serviço, 10-11, 2, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "98"
            )
        
        # Forma de Lançamento, 12-13, 2, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "30"
            )
        
        # Número da Versão do Layout do Lote, 14-16, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                2, "040"
            )
        
        # Uso Exclusivo FEBRABAN/CNAB, 17-17, 9, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, ""
            )
        
        # Tipo de Inscrição da Empresa, 18-18, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "2"
            )
        
        # Número de Inscrição da Empresa, 19-32, 14, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                14, "08378641000196"
            )
        
        # Código do Convênio no Banco, 33-52, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, "141006"
            )
        
        # Agência Mantenedora da Conta, 53-57, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "02870"
            )
        
        # Dígito Verificador da Agência, 58-58, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "3"
            )
        
        # Número da Conta Corrente, 59-70, 12, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                12, "000000301432"
            )
        
        # Dígito Verificador da Conta, 71-71, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "0"
            )
        
        # Dígito Verificador da Ag/Conta, 72-72, 1, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                1, "0"
            )
        
        # Nome da Empresa, 73-102, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "CINTE TELECOM COMERCIO E SERVICOS LTDA-EPP"
            )
        
        # Mensagem, 103-142, 40, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, ""
            )
        
        # Logradouro, 143-172, 30, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                30, "Rua Doutor Lauro Pinto"
            )
        
        # Número do Local, 173-177, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "610"
            )
        
        # Complemento, 178-192, 15, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                15, "Casa"
            )
        
        # Cidade, 193-212, 20, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                20, "Natal"
            )
        
        # CEP, 213-217, 5, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                5, "59064"
            )
        
        # Complemento CEP, 218-220, 3, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                3, "250"
            )
        
        # Estado, 221-222, 2, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                2, "RN"
            )
        
        # Uso Exclusivo Febraban/Cnab, 225-230, 6, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                8, ""
            )
        
        # Códigos das Ocorrências p/Retorno, 231-240, 10, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                10, ""
            )
        
        return conteudo
    
    def trailer_arquivo(self):
        conteudo = ""
        
        # Código do Banco na Compensação, 1-3, 3, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                3, "001"
            )
        
        # Lote de Serviço, 4-7, 4, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                4, "9999"
            )
        
        # Tipo de Registro, 8-8, 1, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                1, "9"
            )
        
        # Uso Exclusivo Febraban/Cnab, 9-17, 9, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                9, ""
            )
        
        # Quantidade de Lotes do Arquivo, 18-23, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, "1"
            )
        
        # Quantidade de Registros do Arquivo, 24-29, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, "1"
            )
        
        # Qtde de Contas p/Conc. (Lotes), 30-35, 6, NUM
        conteudo = conteudo + "" + self.formatar_numerico(
                6, "1"
            )
        
        # Uso Exclusivo Febraban/Cnab, 36-240, 205, ALFA
        conteudo = conteudo + "" + self.formatar_alfanumerico(
                205, ""
            )
        
        return conteudo
    
    # Função para formatar elementos numéricos para o arquivo da nota fiscal
    # Recebe o tamanho padrão do documento e o valor para formatação
    def formatar_numerico(self, tamanho, valor):
        # Declaração de string que será utilizada para formatação e retorno
        string_tratada = ""
        valor = str(valor)
        # For preenchendo com 0 a esquerda do tamanho solicitado
        for x in range(0, tamanho):
            string_tratada = string_tratada + "0"
        
        # Concatenando a string de 0 com o valor desejado à direita
        string_tratada = string_tratada + valor
        
        # retornando a string formatada com o tamanho solicitado, contando da direita para esquerda   
        return string_tratada[-tamanho::]
    
    
    # Função para formatar elementos alfanuméricos para o arquivo da nota fiscal
    # Recebe o tamanho padrão do documento e a string para formatação
    def formatar_alfanumerico(self, tamanho, string_pura):
        # Declaração de string que será utilizada para formatação e retorno recebendo a string passada
        string_tratada = "" + string_pura
        
        # For preenchendo com espaços à direita do tamanho solicitado
        for x in range(0, tamanho):
            string_tratada = string_tratada + " "
        
        
        # retornando a string formatada com o tamanho solicitado, contando da esquerda para direita   
        return string_tratada[:tamanho]