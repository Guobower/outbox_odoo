# -*- coding: utf-8 -*-
from openerp import models, fields

class Account_invoice_inherited(models.Model):
    _inherit = 'account.invoice' 

    mes_competencia = fields.Selection(
        selection=[(1, 'Janeiro'),
                   (2, 'Fevereiro'),
                   (3, 'Março'),
                   (4, 'Abril'),
                   (5, 'Maio'),
                   (6, 'Junho'),
                   (7, 'Julho'),
                   (8, 'Agosto'),
                   (9, 'Setembro'),
                   (10, 'Outubro'),
                   (11, 'Novembro'),
                   (12, 'Dezembro')],
        string='Mês de Competência',
        help='Mês da competência de prestação do serviço.')
    
    ano_competencia = fields.Selection(
        selection=[(2017, '2017'),
                   (2016, '2016')],
        string='Ano de Competência',
        help='Ano da competência de prestação do serviço.')
    
    periodo_prestacao_servico = fields.Char(
        string="Período de Prestação do Serviço",
        size=150)
    
    numero_nota_fiscal = fields.Integer(
        string='Nota Fiscal',
        help='Número da Nota Fiscal')
    
    data_emissao = fields.Date(
        string='Data de Emissão',
        help='Data de Emissão')
    
    chave_autenticacao_digital = fields.Char(
        string="Chave Digital",
        size=250)
    
    lote_convenio = fields.Many2one(
        string='Lote de Notas Fiscais',
        help='Lote de notas fiscais do convênio 115 ao qual pertence a fatura',
        comodel_name='convenio115')
    
    
    def on_change_data_emissao(self, cr, user, ids, data_emissao, contrato, context=None):
        '''
            Descrição:
              Esta função tem como objetivo preencher automaticamente os dados de
              mês e ano de competência, além do período de prestação de serviço na medida
              em que for selecionada uma data de emissão da nota fiscal.
        
            Utilização:
              on_change_data_emissao(param1, param2)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              context
                Contexto atual
        '''
        from datetime import *
        
        if data_emissao:
            ano, mes, dia = data_emissao.split('-')
            
            if int(mes) > 1:
                mes = int(mes)-1
                ano = int(ano)
            else:
                mes = 12
                ano = int(ano)-1
            
            if ids:
                fatura = self.pool.get('account.invoice').browse(cr, user, ids[0])
                data_fatura = fatura.create_date.split(" ")
                
                data_base = datetime.strptime(data_fatura[0], '%Y-%m-%d')
                inicio_periodo = data_base - timedelta(days=31)
                final_periodo = data_base - timedelta(days=1)
                
                res = {
                     'value': {
                        # Define os valores dos campos e atualiza no formulário
                        'mes_competencia': mes,
                        'ano_competencia': ano,
                        'periodo_prestacao_servico': "De " + str(inicio_periodo.strftime('%d/%m/%Y')) + " à " + str(final_periodo.strftime('%d/%m/%Y'))
                    }
                }
                # Retorna os valores para serem atualizados na view.
                return res
    
    def gerar_nota_fiscal(self, cr, user, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo preencher os dados da chave digital para esta nota e imprimir
              o seu recibo.
        
            Utilização:
              gerar_nota_fiscal()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              context
                Contexto atual
        '''
        fatura = self.pool.get('account.invoice').browse(cr, user, ids[0])
        
        if fatura.numero_nota_fiscal == 0:
            if fatura.lote_convenio:
                lote_nota_fiscal = self.pool.get('convenio115').browse(cr, user, fatura.lote_convenio.id)
                fatura.write({'numero_nota_fiscal': lote_nota_fiscal.ultima_nota + 1}, context=context)
                lote_nota_fiscal.write({'ultima_nota': lote_nota_fiscal.ultima_nota + 1})
                
        if fatura.state != "draft":
            if fatura.numero_nota_fiscal > 0:
                if fatura.data_emissao:
                    # Valor total do ICMS da nota
                    nota_valor_icms = 0
                    # Valor base do ICMS
                    nota_base_icms = 0
                    
                    # Cálculo de ICMS base e valor
                    for linha_imposto in fatura.tax_line:
                        nota_valor_icms = linha_imposto.amount
                        nota_base_icms = linha_imposto.base_amount
                            
                    
                    # Código de autenticação digital do documento fiscal, 32 caracteres, casas 104 - 135, tipo X 
                    autenticacao_digital = self.gerar_autenticacao_digital(
                        self.formatar_numerico(
                            14, self.formatar_caracteres_especiais(str(fatura.partner_id.cnpj_cpf))
                            ),
                        self.formatar_numerico(
                            9, str(fatura.numero_nota_fiscal)
                            ),
                        self.formatar_numerico(
                            12, str('%.2f' % (fatura.amount_total)).replace('.', '')
                            ),
                        self.formatar_numerico(
                            12, str('%.2f' % (nota_base_icms)).replace('.', '')
                            ),
                        self.formatar_numerico(
                            12, str('%.2f' % (nota_valor_icms)).replace('.', '')
                            ),
                        self.formatar_alfanumerico(
                            8, self.formatar_caracteres_especiais(str(fatura.data_emissao))
                            ),
                        self.formatar_numerico(
                            14, self.formatar_caracteres_especiais(str(fatura.company_id.cnpj_cpf))
                            )
                    )
                    
                    fatura.write({'chave_autenticacao_digital': autenticacao_digital}, context=context)
                    
                    return {
                        'type': 'ir.actions.report.xml',
                        'report_name': 'financeiro.report_recibo_nota_fiscal',
                        'context': context,
                    }
                else:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'action_warn',
                        'name': 'Warning',
                        'params': {
                            'title': 'Data de Emissão não informada!',
                            'text': 'Informe a data de emissão da fatura.',
                            'sticky': True
                            }
                    }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Fatura não possui um número de nota fiscal!',
                        'text': 'A fatura ainda não possui um número de nota fiscal, é necessário adicioná-la a um lote de notas fiscais.',
                        'sticky': True
                        }
                }        
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Fatura não confirmada!',
                    'text': 'Confirme a fatura antes de gerar a nota fiscal.',
                    'sticky': True
                    }
             }    
        # Retorna uma mensagem de confirmação.
        return True
    
    
    def gerar_autenticacao_digital(self, cnpj_destinatario, numero_nota, valor_total,
                                   base_calculo_icms, valor_icms, data_emissao, cnpj_emitente):
        # importa classe python com implementação do algoritmo MD5
        import md5
        
        # gera a autenticação com a aplicação do MD5 nos campos repassados
        autenticacao_digital = md5.new(cnpj_destinatario + "" + numero_nota + "" + valor_total + "" + 
                                   base_calculo_icms + "" + valor_icms + "" + data_emissao + "" + cnpj_emitente)
        
        # retornando a autenticação  
        return autenticacao_digital.hexdigest()
    
    # Função para formatar strings para retirar caracteres especiais
    def formatar_caracteres_especiais(self, string_pura):
        if string_pura:
            # Retirando caracteres especiais e substituindo por nada
            string_pura = string_pura.replace(".", "")
            string_pura = string_pura.replace("/", "")
            string_pura = string_pura.replace("-", "")
            string_pura = string_pura.replace("(", "")
            string_pura = string_pura.replace(")", "")
            
            # retornando a string formatada   
            return string_pura
        else:
            return ""
        
    # Função para formatar elementos numéricos para o arquivo da nota fiscal
    # Recebe o tamanho padrão do documento e o valor para formatação
    def formatar_numerico(self, tamanho, valor):
        # Declaração de string que será utilizada para formatação e retorno
        string_tratada = ""
        
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
    
    
    def report_format_moeda(self, cr, user, ids, valor, context=None):
        '''
            Descrição:
              Formatar valores como moeda em real para a exibição em relatórios.
        
            Utilização:
              report_format_moeda(param1)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              valor
                Valor a ser formatado
              context
                Contexto atual
        '''
        import locale
        
        return locale.currency(valor, grouping=True, symbol=None)
    
    