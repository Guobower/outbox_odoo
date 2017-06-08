# -*- coding: utf-8 -*-
import simplejson, urllib

from openerp import models, fields, api

class Convenio115(models.Model):
    _name = 'convenio115'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)
    
    mes = fields.Selection(
        selection=[('01', 'Janeiro'),
                   ('02', 'Fevereiro'),
                   ('03', 'Março'),
                   ('04', 'Abril'),
                   ('05', 'Maio'),
                   ('06', 'Junho'),
                   ('07', 'Julho'),
                   ('08', 'Agosto'),
                   ('09', 'Setembro'),
                   ('10', 'Outubro'),
                   ('11', 'Novembro'),
                   ('12', 'Dezembro')],
        string='Mês',
        help='Mês de referência para o lote enviado',
        required=True)
    
    ano = fields.Selection(
        selection=[('17', '2017')],
        string='Ano',
        help='Ano de referência para o lote enviado',
        required=True)
    
    empresa = fields.Many2one(
        string='Empresa Emitente',
        help='Empresa emissora das notas fiscais',
        comodel_name='res.company',
        required=True)
    
    volume = fields.Selection(
        selection=[('001', '001'),
                   ('002', '002'),
                   ('003', '003'),
                   ('004', '004'),
                   ('005', '005'),
                   ('006', '006'),
                   ('007', '007'),
                   ('008', '008'),
                   ('009', '009'),
                   ('010', '010')],
        string='Volume',
        help='Número sequencial do lote gerado para o mês em questão, iniciando-se de 001',
        required=True)
    
    data_emissao = fields.Date(
        string='Data de Emissão',
        help='Data de emissão do lote')
    
    status_lote = fields.Selection(
        selection=[('N', 'Normal'),
                   ('S', 'Substituto')],
        string='Status do Lote',
        help='Normal ou de substituição',
        required=True)
    
    status_sequencial = fields.Selection(
        selection=[('01', '01'),
                   ('02', '02'),
                   ('03', '03'),
                   ('04', '04'),
                   ('05', '05'),
                   ('06', '06'),
                   ('07', '07'),
                   ('08', '08'),
                   ('09', '09'),
                   ('10', '10')],
        string='Sequencial do Status',
        help='Em caso normais usar 01, caso seja substituto iniciar com 01',
        required=True)
    
    situacao_documento_fiscal = fields.Selection(
        selection=[('S', 'Documento fiscal cancelado dentro do período'),
                   ('R', 'Documento fiscal de substituição a documento do mesmo período'),
                   ('C', 'Documento fiscal complementar'),
                   ('N', 'Demais casos')],
        string='Situação do Documento Fiscal',
        help='Situação do documento fiscal',
        required=True)
    
    notas_fiscais = fields.Many2many(
        comodel_name='account.invoice',
        string='Faturas de Clientes',
        help='Selecione as faturas de clientes que farão parte desse lote fiscal')
    
    
    quantidade_registros_mestre = fields.Integer(
        string='Quantidade de Registros',
        help='Quantidade de registros no arquivo mestre')
    
    data_emissao_primeiro_documento = fields.Date(
        string='Data de Emissão - Primeiro DOC',
        help='Data de Emissão - Primeiro DOC')
    
    data_emissao_ultimo_documento = fields.Date(
        string='Data de Emissão - Último DOC',
        help='Data de Emissão - Último DOC')
    
    numero_primeiro_documento = fields.Char(
        string="Número do primeiro DOC",
        size=100,
        help='Número do primeiro DOC')
    
    numero_ultimo_documento = fields.Char(
        string="Número do último DOC",
        size=100,
        help='Número do último DOC')
    
    valor_total = fields.Float(
        string="Valor Total",
        help='Valor Total do Lote')
    
    
    base_calculo_icms = fields.Float(
        string="Base de Cálculo ICMS",
        help='Base de Cálculo ICMS')
    
    icms = fields.Float(
        string="Valor ICMS",
        help='Valor ICMS')
    
    operacoes_isentas = fields.Float(
        string="Valor Operações Isentas",
        help='Valor Operações Isentas') 
    
    nome_arquivo_mestre = fields.Char(
        string="Nome do Arquivo Mestre",
        size=100,
        help='Nome do Arquivo Mestre')
    
    codigo_autenticacao_digital_mestre = fields.Char(
        string="Autenticação do Arquivo Mestre",
        size=100,
        help='Código de Autenticação do Arquivo Mestre')
    
    quantidade_registros_itens = fields.Integer(
        string='Qtd de Registros de Itens',
        help='Quantidade de registros no arquivo de itens')
    
    nome_arquivo_itens = fields.Char(
        string="Nome do Arquivo Itens",
        size=100,
        help='Nome do Arquivo Itens')
    
    codigo_autenticacao_digital_itens = fields.Char(
        string="Autenticação do Arquivo de Itens",
        size=100,
        help='Código de Autenticação do Arquivo de Itens')
    
    quantidade_registros_destinatarios = fields.Integer(
        string='Qtd de Registros de Destinatários',
        help='Quantidade de registros no arquivo de destinatários')
    
    nome_arquivo_destinatarios = fields.Char(
        string="Nome do Arquivo de Destinatários",
        size=100,
        help='Nome do Arquivo de Destinatários')
    
    codigo_autenticacao_digital_destinatarios = fields.Char(
        string="Autenticação do Arquivo de Destinatários",
        size=100,
        help='Código de Autenticação do Arquivo de Destinatários')
    
    versao_validador = fields.Char(
        string="Versão Validador",
        size=100,
        help='Versão do Validador')
    
    chave_controle_recibo = fields.Char(
        string="Chave de Controle do Recibo",
        size=100,
        help='Chave de Controle do Recibo')
    
    quantidade_advertencias = fields.Integer(
        string='Quantidade de Advertências',
        help='Quantidade de advertências')
    
    
    
    
    
    
    def hello_world(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            # your logic will set over  hear
            
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Warning!',
                'text': 'Entered Quantity is greater than quantity on source.',
                'sticky': True
                }
         }
    
    def gerar_arquivo(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        assert len(ids) == 1, "Only one ID accepted"
        
        model_obj = self.pool.get('convenio115')  # the model of record you want file attached
        record_obj = model_obj.browse(cr, uid, ids[0])  # actual record to wich you attach file
        
        self.gerar_mestre_fiscal(cr, uid, ids, model_obj, record_obj, context)
        self.gerar_item(cr, uid, ids, model_obj, record_obj, context)
        self.gerar_dados_destinatarios(cr, uid, ids, model_obj, record_obj, context)
        # self.gerar_dados_controle_identificacao(cr, uid, ids, model_obj, record_obj, context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Arquivos Gerados!',
                'text': 'Arquivos gerados com sucesso, confira nos anexos do documento.',
                'sticky': True
                }
         }
        
    def gerar_arquivo_identificacao(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        assert len(ids) == 1, "Only one ID accepted"
        
        model_obj = self.pool.get('convenio115')  # the model of record you want file attached
        record_obj = model_obj.browse(cr, uid, ids[0])  # actual record to wich you attach file
        
        self.gerar_dados_controle_identificacao(cr, uid, ids, model_obj, record_obj, context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Arquivos Gerados!',
                'text': 'Arquivos gerados com sucesso, confira nos anexos do documento.',
                'sticky': True
                }
         }    
        
    
    # Método para gerar arquivo Mestre fiscal    
    def gerar_mestre_fiscal(self, cr, uid, ids, model_obj, record_obj, context):
        import base64
        # Geração do primeiro arquivo
        cnpj_emitente = self.formatar_caracteres_especiais(record_obj.empresa.cnpj_cpf)
        
        # Gerando nome do arquivo
        file_name = record_obj.empresa.state_id.code + '' + cnpj_emitente + '21UUU' + record_obj.ano + '' + record_obj.mes + '' + record_obj.status_lote + '' + record_obj.status_sequencial + 'M.' + record_obj.volume + ''
        
        # Gerando dados do arquivo, precisamos fazer um loop em todas as faturas
        txt_content_arquivo = ""
        
        # Número sequencial da Nota Fiscal
        numero_nota = 0
        
        # Número de itens nas Notas Fiscais
        numero_itens = 0
        
        # Data do primeiro documento
        data_primeiro = ""
        
        # Data do último documento
        data_ultimo = ""
        
        # Valor Total
        valor_total = 0
        
        # Base de cálculo do ICMS
        base_icms = 0
        
        # ICMS
        icms = 0
        
        # Operações isentas
        operacoes_isentas = 0
        
        for item in record_obj.notas_fiscais:
            # Incrementa o número sequencial da Nota Fiscal
            numero_nota = numero_nota + 1
            txt_content = ""
            
            # CNPJ Cliente, 14 caracteres, casas 1 - 14, tipo N 
            txt_content = txt_content + "" + self.formatar_numerico(
                14, self.formatar_caracteres_especiais(str(item.partner_id.cnpj_cpf))
                )
            
            # IE do Cliente, 14 caracteres, casas 15 - 28, tipo X 
            if item.partner_id.inscr_est:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    14, "" + str(item.partner_id.inscr_est)
                    )
            else:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    14, "ISENTO"
                    )
                 
            
            # Razão Social do Cliente, 35 caracteres, casas 29 - 63, tipo X 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                35, str(item.partner_id.legal_name.encode('ascii', 'ignore').decode('ascii'))
                )
            
            # UF, 2 caracteres, casas 64 - 65, tipo X 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                2, str(item.partner_id.state_id.code)
                )
            
            # Classe de consumo, 1 caracter, casa 66, tipo N 
            txt_content = txt_content + "0"
            
            # Fase ou tipo de ligação, 1 caracter, casa 67, tipo N 
            txt_content = txt_content + "4"
            
            # Grupo de tensão, 2 caracteres, casas 68 - 69, tipo N 
            txt_content = txt_content + "00"
        
            # Código de indentificação do consumidor ou assinante, 12 caracteres, casas 70 - 81, tipo X 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                12, str(item.partner_id.id)
                )
            
            # Data de emissão, 8 caracteres, casas 82 - 89, tipo N 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                8, self.formatar_caracteres_especiais(str(item.date_invoice))
                )
            
            # Descobrindo se é a primeira data
            if data_primeiro == "":
                data_primeiro = item.date_invoice
            
            # Informando a data do último documento
            data_ultimo = item.date_invoice
            
            # Modelo, 2 caracteres, casas 90 - 91, tipo N 
            txt_content = txt_content + "" + self.formatar_numerico(
                2, "21"
                )
            
            # Série, 3 caracteres, casas 92 - 94, tipo X 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                3, "UUU"
                )
            
            # Número, 9 caracteres, casas 95 - 103, tipo N 
            txt_content = txt_content + "" + self.formatar_numerico(
                9, str(numero_nota)
                )
            
            # Valor total do ICMS da nota
            nota_valor_icms = 0
            
            # Valor base do ICMS
            nota_base_icms = 0
            
            # Cálculo de ICMS base e valor
            for linha_imposto in item.tax_line:
                nota_valor_icms = linha_imposto.amount
                nota_base_icms = linha_imposto.base_amount
                    
            
            # Código de autenticação digital do documento fiscal, 32 caracteres, casas 104 - 135, tipo X 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                32, str(
                        self.gerar_autenticacao_digital(
                            self.formatar_numerico(
                                14, self.formatar_caracteres_especiais(str(item.partner_id.cnpj_cpf))
                                ),
                            self.formatar_numerico(
                                9, str(numero_nota)
                                ),
                            self.formatar_numerico(
                                12, str('%.2f' % (item.amount_total)).replace('.', '')
                                ),
                            self.formatar_numerico(
                                12, str('%.2f' % (nota_base_icms)).replace('.', '')
                                ),
                            self.formatar_numerico(
                                12, str('%.2f' % (nota_valor_icms)).replace('.', '')
                                ),
                            self.formatar_alfanumerico(
                                8, self.formatar_caracteres_especiais(str(item.date_invoice))
                                ),
                            self.formatar_numerico(
                                14, self.formatar_caracteres_especiais(str(record_obj.empresa.cnpj_cpf))
                                )
                    )
                )
             )
        
            # Valor Total, 12 caracteres, casas 136 - 147, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                12, str('%.2f' % (item.amount_total)).replace('.', '')
                )
            
            # Somando o valor total
            valor_total = valor_total + item.amount_total
            
            # BC ICMS, 12 caracteres, casas 148 - 159, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                12, str('%.2f' % (nota_base_icms)).replace('.', '')
                )
            
            # Somando o ICMS
            base_icms = base_icms + nota_base_icms
            
            # ICMS Destacado, 12 caracteres, casas 160 - 171, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                12, str('%.2f' % (nota_valor_icms)).replace('.', '')
                )
            
            # Somando o ICMS
            icms = icms + nota_valor_icms
            
            # Operações isentas ou não tributadas, 12 caracteres, casas 172 - 183, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                12, str('%.2f' % (item.amount_total - nota_base_icms)).replace('.', '')
                )
            
            # Somando as Operações isentas
            operacoes_isentas = operacoes_isentas + (item.amount_total - nota_base_icms)
            
            # Outros valores, 12 caracteres, casas 184 - 195, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                12, str("0")
                )
            
            # Situação do documento, 1 caracteres, casas 196 - 196, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                1, str(record_obj.situacao_documento_fiscal)
                )
            
            # Ano e mês de referência da apuração, 4 caracteres, casas 197 - 200, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                4, str(record_obj.ano + '' + record_obj.mes)
                )
            
            # Número do primeiro item da nota fiscal
            numero_item_documento = 0
            for linha_produto in item.invoice_line:
                numero_itens = numero_itens + 1
                if numero_item_documento == 0:
                    numero_item_documento = numero_itens
            
            
            # Referência ao item da NF, 9 caracteres, casas 201 - 209, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                9, str(numero_item_documento)
                )
            
            # Número do terminal telefônico ou da unidade consumidora, 12 caracteres, casas 210 - 221, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                12, str("")
                )
            
            # Indicação do tipo de informação contida no campo 1, 1 caracteres, casas 222 - 222, tipo N
            if item.partner_id.is_company:
                txt_content = txt_content + "" + self.formatar_numerico(
                    1, "1"
                    )
            else:
                txt_content = txt_content + "" + self.formatar_numerico(
                    1, "2"
                    )
            
            
            # Tipo de cliente, 2 caracteres, casas 223 - 224, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                    2, "05"
                    )
            
            # Subclasse de consumo, 2 caracteres, casas 225 - 226, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                    2, "00"
                    )
            
            # Número do terminal telefônico principal, 12 caracteres, casas 227 - 238, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                12, str("")
                )
            
            # CNPJ do emitente, 14 caracteres, casas 239 - 252, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                14, self.formatar_caracteres_especiais(str(record_obj.empresa.cnpj_cpf))
                )
            
            # Número ou código da fatura comercial, 20 caracteres, casas 253 - 272, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                20, self.formatar_caracteres_especiais(str(item.internal_number))
                )
            
            # Valor total da fatura comercial, 12 caracteres, casas 273 - 284, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                12, str('%.2f' % (item.amount_total)).replace('.', '')
                )
            
            # Data de leitura anterior, 8 caracteres, casas 285 - 292, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                8, str('0')
                )
            
            # Data de leitura atual, 8 caracteres, casas 293 - 300, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                8, str('0')
                )
            
            # Brancos - reservado para uso futuro, 50 caracteres, casas 301 - 350, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                50, str('')
                )
            
            # Brancos - reservado para uso futuro, 8 caracteres, casas 351 - 358, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                8, str('0')
                )
            
            # Informações adicionais, 30 caracteres, casas 359 - 388, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                30, str('')
                )
            
            # Brancos - reservado para uso futuro, 5 caracteres, casas 389 - 393, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                5, str('')
                )
            
            # Código de autenticação digital do registro, 32 caracteres, casas 394 - 425
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                32, str(self.gerar_autenticacao_digital_registro(txt_content))
                )
            
            # Encerramento da Linha
            txt_content = txt_content + "\r\n"
            txt_content_arquivo = txt_content_arquivo + txt_content
             
        
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        
        context.update({'default_res_id': ids[0], 'default_res_model': 'convenio115'})

        attach_id = attach_obj.create(cr, uid, {'name': attach_name,
                                                'datas': base64.encodestring(txt_content_arquivo),
                                                'datas_fname': file_name}, context=context)
        
        
        # Setando valores importantes para outros arquivos
        # Quantidade de registros do arquivo Mestre
        self.write(cr, uid, ids[0], {'quantidade_registros_mestre':numero_nota}, context)
        
        # Data de emissão do primeiro documento
        self.write(cr, uid, ids[0], {'data_emissao_primeiro_documento':data_primeiro}, context)
        
        # Data de emissão do último documento
        self.write(cr, uid, ids[0], {'data_emissao_ultimo_documento':data_ultimo}, context)
        
        # Número do primeiro documento
        self.write(cr, uid, ids[0], {'numero_primeiro_documento':1}, context)
        
        # Número do último documento
        self.write(cr, uid, ids[0], {'numero_ultimo_documento':numero_nota}, context)
        
        # Valor total
        self.write(cr, uid, ids[0], {'valor_total':valor_total}, context)
        
        # Base de cálculo ICMS
        self.write(cr, uid, ids[0], {'base_calculo_icms':base_icms}, context)
        
        # ICMS
        self.write(cr, uid, ids[0], {'icms':icms}, context)
        
        # Operações Isentas
        self.write(cr, uid, ids[0], {'operacoes_isentas':operacoes_isentas}, context)
        
        # Nome do arquivo Mestre
        self.write(cr, uid, ids[0], {'nome_arquivo_mestre':file_name}, context)
        
        # Código de autenticação digital do Mestre
        self.write(cr, uid, ids[0], {'codigo_autenticacao_digital_mestre':self.gerar_autenticacao_digital_registro(txt_content)}, context)
        
        
        return attach_id
    
    
    
    # Método para gerar arquivo Itens Fiscais
    def gerar_item(self, cr, uid, ids, model_obj, record_obj, context):
        import base64
        # Geração do primeiro arquivo
        cnpj_emitente = self.formatar_caracteres_especiais(record_obj.empresa.cnpj_cpf)
        
        # Gerando nome do arquivo
        file_name = record_obj.empresa.state_id.code + '' + cnpj_emitente + '21UUU' + record_obj.ano + '' + record_obj.mes + '' + record_obj.status_lote + '' + record_obj.status_sequencial + 'I.' + record_obj.volume + ''
        
        # Gerando dados do arquivo, precisamos fazer um loop em todas as faturas
        txt_content_arquivo = ""
        
        # Número sequencial da Nota Fiscal
        numero_nota = 0
        
        # Totalizador de itens
        total_itens = 0
        for item in record_obj.notas_fiscais:
            # Incrementa o número sequencial da Nota Fiscal
            numero_nota = numero_nota + 1
            numero_item = 0
            
            for linha_produto in item.invoice_line:
                txt_content = ""
                numero_item = numero_item + 1
                total_itens = total_itens + 1
            
                # CNPJ Cliente, 14 caracteres, casas 1 - 14, tipo N 
                txt_content = txt_content + "" + self.formatar_numerico(
                    14, self.formatar_caracteres_especiais(str(item.partner_id.cnpj_cpf))
                    )
                
                # UF, 2 caracteres, casas 15 - 16, tipo X 
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    2, str(item.partner_id.state_id.code)
                    )
                
                # Classe do Consumo, 1 casa, 17 - 17 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    1, str('0')
                    )
                
                # Fase ou Tipo de Utilização, 1 casa, 18 - 18 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    1, str('4')
                    )
                
                # Grupo de Tensão, 2 casas, 19 - 20 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    2, str('00')
                    )
                
                # Data de Emissão, 8 casas, 21 - 28 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    8, self.formatar_caracteres_especiais(str(item.date_invoice))
                    )
                
                # Modelo, 2 casas, 29 - 30 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    2, str("21")
                    )
                
                # Série, 3 casas, 31 - 33 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    3, str("UUU")
                    )
                
                # Número, 9 casas, 34 - 42 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    9, str(numero_nota)
                    )
                
                # CFOP, 4 casas, 43 - 46 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    4, str("5307")
                    )
                
                # Nº de ordem do item, 3 casas, 47 - 49 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    3, str(numero_item)
                    )
                
                # Código do item, 10 casas, 50 - 59 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    10, str(linha_produto.product_id.id)
                    )
                
                # Descrição do item, 40 casas, 60 - 99 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    40, str(linha_produto.product_id.name.encode('ascii', 'ignore').decode('ascii'))
                    )
                
                # Código de classificação do item, 4 casas, 100 - 103 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    4, str("0104")
                    )
                
                # Unidade, 6 casas, 104 - 109 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    6, str(linha_produto.uos_id.name)
                    )
                
                # Quantidade contratada (com 3 decimais), 12 casas, 110 - 121 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    12, str("0")
                    )
                
                # Quantidade medida (com 3 decimais), 12 casas, 122 - 133 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    12, str("0")
                    )
                
                # Total (com 2 decimais), 11 casas, 134 - 144 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('%.2f' % (linha_produto.quantity * linha_produto.price_unit)).replace('.', '')
                    )
    
                # Desconto/Redutores (com 2 decimais), 11 casas, 134 - 144 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('0')
                    )
    
                # Acréscimos e Despesas Acessórias (com 2 decimais), 11 casas, 156 - 166 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('0')
                    )
                
                # Valores isentos
                valores_isentos = 0
                
                # BC ICMS (com 2 decimais), 11 casas, 167 - 177 tipo N
                if linha_produto.price_subtotal > linha_produto.price_tax_discount:
                    txt_content = txt_content + "" + self.formatar_numerico(
                        11, str('%.2f' % (linha_produto.price_subtotal)).replace('.', '')
                        )
                else:
                    txt_content = txt_content + "" + self.formatar_numerico(
                        11, str('%.2f' % (0.00)).replace('.', '')
                        )
                    valores_isentos = linha_produto.price_subtotal
                    
                    
                # ICMS (com 2 decimais), 11 casas, 178 - 188 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('%.2f' % ((linha_produto.price_subtotal - linha_produto.price_tax_discount))).replace('.', '')
                    )
                
                # Operações isentas ou não tributadas (com 2 decimais), 11 casas, 189 - 199 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('%.2f' % (valores_isentos)).replace('.', '')
                    )
                
                # Outros valores (com 2 decimais), 11 casas, 200 - 210 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('0')
                    )
                
                # Alíquota do ICMS (com 2 decimais), 4 casas, 211 - 214 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    4, str('%.2f' % (30.00)).replace('.', '')
                    )
                
                # Situação, 1 casas, 215 - 215 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    1, str(record_obj.situacao_documento_fiscal)
                    )
                
                # Ano e Mês de referência da apuração, 4 casas, 216 - 219 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    4, str(record_obj.ano + '' + record_obj.mes)
                    )
                
                # Número do Contrato, 15 casas, 220 - 234 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    15, str("")
                    )
                
                # Quantidade faturada (com 3 decimais), 12 casas, 235 - 246 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    12, str('%.3f' % (linha_produto.quantity)).replace('.', '')
                    )
                
                # Tarifa Aplicada / Preço Médio Efetivo (com 6 decimais), 11 casas, 247 - 257 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('0')
                    )
                
                # Alíquota PIS/PASEP (com 4 decimais), 6 casas, 258 - 263 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    6, str('%.4f' % (linha_produto.pis_base)).replace('.', '')
                    )
                
                # PIS/PASEP (com 2 decimais), 11 casas, 264 - 274 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('%.2f' % (linha_produto.pis_value)).replace('.', '')
                    )
                
                # Alíquota COFINS (com 4 decimais), 6 casas, 275 - 280 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    6, str('%.4f' % (linha_produto.cofins_base)).replace('.', '')
                    )
                
                # COFINS (com 2 decimais), 11 casas, 281 - 291 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    11, str('%.2f' % (linha_produto.cofins_value)).replace('.', '')
                    )
                
                # Indicador de Desconto Judicial, 1 casas, 292 - 292 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    1, str('')
                    )
                
                # Tipo de Insenção/Redução de base de cálculo, 2 casas, 293 - 294 tipo N
                txt_content = txt_content + "" + self.formatar_numerico(
                    2, str('99')
                    )
                
                # Brancos - reservados para uso futuro, 5 casas, 295 - 299 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    5, str('')
                    )
                
                # Código de autenticação digital do registro, 32 casas, 300 - 331 tipo X
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    32, str(self.gerar_autenticacao_digital_registro(txt_content))
                )
                
                # Encerramento da Linha
                txt_content = txt_content + "\r\n"
                txt_content_arquivo = txt_content_arquivo + txt_content
        
        # Quantidade de registros do arquivo Itens
        self.write(cr, uid, ids[0], {'quantidade_registros_itens':total_itens}, context)
        
        # Nome do arquivo Itens
        self.write(cr, uid, ids[0], {'nome_arquivo_itens':file_name}, context)
        
        # Código de autenticação digital do arquivo de Itens
        self.write(cr, uid, ids[0], {'codigo_autenticacao_digital_itens':self.gerar_autenticacao_digital_registro(txt_content)}, context)
        
        
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        
        context.update({'default_res_id': ids[0], 'default_res_model': 'convenio115'})

        attach_id = attach_obj.create(cr, uid, {'name': attach_name,
                                                'datas': base64.encodestring(txt_content_arquivo),
                                                'datas_fname': file_name}, context=context)
        
        return attach_id
    
    
    
    # Método para gerar arquivo com dados dos destinatários   
    def gerar_dados_destinatarios(self, cr, uid, ids, model_obj, record_obj, context):
        import base64
        # Geração do primeiro arquivo
        cnpj_emitente = self.formatar_caracteres_especiais(record_obj.empresa.cnpj_cpf)
        
        # Gerando nome do arquivo
        file_name = record_obj.empresa.state_id.code + '' + cnpj_emitente + '21UUU' + record_obj.ano + '' + record_obj.mes + '' + record_obj.status_lote + '' + record_obj.status_sequencial + 'D.' + record_obj.volume + ''
        
        # Gerando dados do arquivo, precisamos fazer um loop em todas as faturas
        txt_content_arquivo = ""
        
        # Número sequencial da Nota Fiscal
        numero_nota = 0
        for item in record_obj.notas_fiscais:
            # Incrementa o número sequencial da Nota Fiscal
            numero_nota = numero_nota + 1
            txt_content = ""
            
            # CNPJ Cliente, 14 caracteres, casas 1 - 14, tipo N 
            txt_content = txt_content + "" + self.formatar_numerico(
                14, self.formatar_caracteres_especiais(str(item.partner_id.cnpj_cpf))
                )
            
            # IE do Cliente, 14 caracteres, casas 15 - 28, tipo X 
            if item.partner_id.inscr_est:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    14, "" + str(item.partner_id.inscr_est)
                    )
            else:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    14, "ISENTO"
                    )
                 
                
            # Razão Social, 35 caracteres, casas 29 - 63, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                35, str(item.partner_id.legal_name.encode('ascii', 'ignore').decode('ascii'))
                )
            
            # Logradouro, 45 caracteres, casas 64 - 108, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                45, str(item.partner_id.street.encode('ascii', 'ignore').decode('ascii'))
                )
            
            # Número, 5 caracteres, casas 109 - 113, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                5, str(item.partner_id.number)
                )
            
            # Complemento, 15 caracteres, casas 114 - 128, tipo X
            if item.partner_id.street2:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    15, str(item.partner_id.street2)
                )
            else:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    15, str("")
                )
            
            # CEP, 8 caracteres, casas 129 - 136, tipo N
            if item.partner_id.zip:
                txt_content = txt_content + "" + self.formatar_numerico(
                    8, str(self.formatar_caracteres_especiais(item.partner_id.zip))
                    )
            else:
                txt_content = txt_content + "" + self.formatar_numerico(
                    8, str("0")
                    )

            # Bairro, 15 caracteres, casas 137 - 151, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                15, str(item.partner_id.district.encode('ascii', 'ignore').decode('ascii'))
                )
            
            # Municipio, 30 caracteres, casas 152 - 181, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                30, str(item.partner_id.l10n_br_city_id.name)
                )
            
            # UF, 2 caracteres, casas 64 - 65, tipo X 
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                2, str(item.partner_id.state_id.code)
                )
            
            # Telefone de contato, 12 caracteres, casas 184 - 195, tipo X
            if item.partner_id.phone:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    12, str(self.formatar_caracteres_especiais(item.partner_id.phone))
                )
            else:
                txt_content = txt_content + "" + self.formatar_alfanumerico(
                    12, str("")
                )
            
            
            # Código de indentificação do consumidor ou assinante, 12 caracteres, casas 196 - 207, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                12, str(item.partner_id.id)
                )
            
            # Número do terminal telefônico ou da unidade consumidora, 12 caracteres, casas 208 - 219, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                12, str("")
                )
            
            # UF de habilitação do terminal telefônico, 2 caracteres, casas 220 - 221, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                2, str(item.partner_id.state_id.code)
                )
            
            # Data de emissão, 8 caracteres, casas 222 - 229, tipo N
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                8, self.formatar_caracteres_especiais(str(item.date_invoice))
                )
            
            # Modelo, 2 caracteres, casas 230 - 231, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                2, str("21")
                )
            
            # Série, 3 caracteres, casas 232 - 234, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                3, str("UUU")
                )
            
            # Número, 9 caracteres, casas 235 - 243, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                9, str(numero_nota)
                )
            
            # Código do Município, 7 caracteres, casas 244 - 250, tipo N
            txt_content = txt_content + "" + self.formatar_numerico(
                7, str(item.partner_id.l10n_br_city_id.state_id.ibge_code + "" + item.partner_id.l10n_br_city_id.ibge_code)
                )
            
            # Brancos - reservado para uso futuro, 5 caracteres, casas 251 - 255, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                5, str("")
                )
            
            # Código de autenticação digital do registro, 32 caracteres, casas 256 - 287, tipo X
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                    32, str(self.gerar_autenticacao_digital_registro(txt_content))
                )
            
            
            # Encerramento da Linha
            txt_content = txt_content + "\r\n"
            txt_content_arquivo = txt_content_arquivo + txt_content
        
        # Quantidade de registro do arquivo de Destinatários
        self.write(cr, uid, ids[0], {'quantidade_registros_destinatarios':numero_nota}, context)
        
        # Nome do arquivo de Destinatários
        self.write(cr, uid, ids[0], {'nome_arquivo_destinatarios':file_name}, context)
        
        # Código de autenticação digital do arquivo de Destinatários
        self.write(cr, uid, ids[0], {'codigo_autenticacao_digital_destinatarios':self.gerar_autenticacao_digital_registro(txt_content)}, context)
         
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        
        context.update({'default_res_id': ids[0], 'default_res_model': 'convenio115'})

        attach_id = attach_obj.create(cr, uid, {'name': attach_name,
                                                'datas': base64.encodestring(txt_content_arquivo),
                                                'datas_fname': file_name}, context=context)
        
        return attach_id
    
    
    
    # Método para gerar arquivo de Controle e Identificação
    def gerar_dados_controle_identificacao(self, cr, uid, ids, model_obj, record_obj, context):
        import base64
        # Geração do primeiro arquivo
        cnpj_emitente = self.formatar_caracteres_especiais(record_obj.empresa.cnpj_cpf)
        
        # Gerando nome do arquivo
        file_name = record_obj.empresa.state_id.code + '' + cnpj_emitente + '21UUU' + record_obj.ano + '' + record_obj.mes + '' + record_obj.status_lote + '' + record_obj.status_sequencial + 'C.' + record_obj.volume + ''
        
        # Gerando dados do arquivo, precisamos fazer um loop em todas as faturas
        txt_content = ""
        
        # CNPJ, 18 caracteres, casas 1 - 18, tipo X 
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            18, str(record_obj.empresa.cnpj_cpf)
            )
        
        # IE, 15 caracteres, casas 19 - 33, tipo X 
        if record_obj.empresa.inscr_est:
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                15, "" + str(record_obj.empresa.inscr_est)
                )
        else:
            txt_content = txt_content + "" + self.formatar_alfanumerico(
                15, "ISENTO"
                )
             
        # Razão Social, 50 caracteres, casas 34 - 83, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            50, str(record_obj.empresa.legal_name)
            )
        
        # Logradouro, 50 caracteres, casas 84 - 133, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            50, str(record_obj.empresa.street)
            )
        
        # CEP, 9 caracteres, casas 134 - 142, tipo X
        txt_content = txt_content + "" + self.formatar_numerico(
            9, str(record_obj.empresa.zip)
            )
        
        # Bairro, 30 caracteres, casas 143 - 172, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            30, str(record_obj.empresa.district.encode('ascii', 'ignore').decode('ascii'))
            )
        
        # Municipio, 30 caracteres, casas 173 - 202, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            30, str(record_obj.empresa.l10n_br_city_id.name.encode('ascii', 'ignore').decode('ascii'))
            )
        
        # UF, 2 caracteres, casas 203 - 204, tipo X 
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            2, str(record_obj.empresa.state_id.code)
            )
        
        # Responsável pela apresentação, 30 caracteres, casas 205 - 234, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            30, str("BRUNO ALEXANDRE AZEVEDO BEZERRA DE SOUSA")
            )
        
        # Cargo, 20 caracteres, casas 235 - 254, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            20, str("CONTADOR")
            )
        
        # Telefone, 12 caracteres, casas 255 - 266, tipo N
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            12, str(self.formatar_caracteres_especiais(record_obj.empresa.phone))
            )
        
        # Email, 40 caracteres, casas 267 - 306, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
            40, str("BRUNOBEZERRA@CINTE.COM.BR")
            )
        
        # Quantidade de registro do arquivo Mestre, 7 caracteres, casas 307 - 313, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                7, str(record_obj.quantidade_registros_mestre)
            )
        
        # Quantidade de notas fiscais canceladas, 7 caracteres, casas 314 - 320, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                7, str("0")
            )
        
        # Data de emissão do primeiro documento fiscal, 8 caracteres, casas 321 - 328, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                8, self.formatar_caracteres_especiais(str(record_obj.data_emissao_primeiro_documento))
            )
        
        # Data de emissão do último documento fiscal, 8 caracteres, casas 329 - 336, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                8, self.formatar_caracteres_especiais(str(record_obj.data_emissao_ultimo_documento))
            )
       
        # Número do primeiro documento fiscal, 9 caracteres, casas 337 - 345, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                9, str(record_obj.numero_primeiro_documento)
            )
        
        # Número do último documento fiscal, 9 caracteres, casas 346 - 354, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                9, str(record_obj.numero_ultimo_documento)
            )
       
        # Valor Total (com 2 decimais), 14 caracteres, casas 355 - 368, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.valor_total)).replace('.', '')
            )
       
        # BC ICMS (com 2 decimais), 14 caracteres, casas 369 - 382, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.base_calculo_icms)).replace('.', '')
            )
       
        # ICMS (com 2 decimais), 14 caracteres, casas 383 - 396, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.icms)).replace('.', '')
            )
       
        # Operações isentas ou não tributadas (com 2 decimais), 14 caracteres, casas 397 - 410, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.operacoes_isentas)).replace('.', '')
            )
        
        # Outros valores que não compõe a BC do ICMS (com 2 decimais), 14 caracteres, casas 411 - 424, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('0')
            )
        
        # Nome do arquivo mestre do documento fiscal, 15 caracteres, casas 425 - 439, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                15, str(record_obj.nome_arquivo_mestre)
            )
        
        # Status de retificação ou substituição do arquivo, 1 caracteres, casas 440 - 440, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                1, str(record_obj.status_lote)
            )
        
        # Código de autenticação digital do arquivo mestre do documento fiscal, 32 caracteres, casas 441 - 472, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                32, str(record_obj.codigo_autenticacao_digital_mestre)
            )
        
        # Quantidade de registros do arquivo Item de Documento Fiscal, 9 caracteres, casas 473 - 481, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                9, str(record_obj.quantidade_registros_itens)
            )
        
        # Quantidade de itens cancelados, 7 caracteres, casas 482 - 488, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                7, str("0")
            )
        
        # Data de emissão do primeiro documento fiscal, 8 caracteres, casas 489 - 496, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                8, self.formatar_caracteres_especiais(str(record_obj.data_emissao_primeiro_documento))
            )
        
        # Data de emissão do ultimo documento fiscal, 8 caracteres, casas 497 - 504, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                8, self.formatar_caracteres_especiais(str(record_obj.data_emissao_ultimo_documento))
            )
        
        # Número do primeiro documento fiscal, 9 caracteres, casas 505 - 513, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                9, str(record_obj.numero_primeiro_documento)
            )
        
        # Número do último documento fiscal, 9 caracteres, casas 514 - 522, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                9, str(record_obj.numero_ultimo_documento)
            )
        
        # Valor Total (com 2 decimais), 14 caracteres, casas 523 - 536, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.valor_total)).replace('.', '')
            )
        
        # Descontos (com 2 decimais), 14 caracteres, casas 537 - 550, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('0')
            )
        
        # Acréscimos e despesas acessórias (com 2 decimais), 14 caracteres, casas 551 - 564, tipo N       
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('0')
            )
               
        # BC ICMS (com 2 decimais), 14 caracteres, casas 565 - 578, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.base_calculo_icms)).replace('.', '')
            )
       
        # ICMS (com 2 decimais), 14 caracteres, casas 579 - 592, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.icms)).replace('.', '')
            )
        
        # Operações isentas ou não tributadas (com 2 decimais), 14 caracteres, casas 593 - 606, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('%.2f' % (record_obj.operacoes_isentas)).replace('.', '')
            )
        
        # Outros valores que não compõe a BC do ICMS (com 2 decimais), 14 caracteres, casas 607 - 620, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                14, str('0')
            )
        
        # Nome do arquivo item do documento fiscal, 15 caracteres, casas 621 - 635, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                15, str(record_obj.nome_arquivo_mestre)
            )
        
        # Status de retificação ou substituição do arquivo, 1 caracteres, casas 636 - 636, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                1, str(record_obj.status_lote)
            )
        
        # Código de autenticação digital do arquivo Item de Documento Fiscal, 32 caracteres, casas 637 - 668, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                32, str(record_obj.codigo_autenticacao_digital_itens)
            )
        
        # Quantidade de registros do arquivo Dados Cadastrais do Destinatário do documento fiscal, 7 caracteres, casas 669 - 675, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                7, str(record_obj.quantidade_registros_itens)
            )
        
        # Nome do arquivo Dados Cadastrais do Destinatário do documento fiscal, 15 caracteres, casas 676 - 690, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                15, str(record_obj.nome_arquivo_mestre)
            )
        
        # Status de retificação ou substituição do arquivo, 1 caracteres, casas 691 - 691, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                1, str(record_obj.status_lote)
            )
        
        # Código de autenticação digital do arquivo Dados Cadastrais do Destinatário do documento fiscal, 32 caracteres, casas 692 - 723, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                32, str(record_obj.codigo_autenticacao_digital_destinatarios)
            )
        
        # Versão do programa Validador utilizado na validação, 3 caracteres, casas 724 - 726, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                3, str(record_obj.versao_validador)
            )
        
        # Chave de controle do recibo de entrega, 9 caracteres, casas 727 - 732, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                3, str(record_obj.chave_controle_recibo)
            )
        
        # Quantidade de Advertências encontradas, 9 caracteres, casas 733 - 741, tipo N
        txt_content = txt_content + "" + self.formatar_numerico(
                9, str(record_obj.quantidade_advertencias)
            )
        
        # Brancos - reservado para uso futuro, 24 caracteres, casas 742 - 765, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                24, str("")
            )
        
        # Código de autenticação digital do registro, 32 caracteres, casas 766 - 797, tipo X
        txt_content = txt_content + "" + self.formatar_alfanumerico(
                32, str(self.gerar_autenticacao_digital_registro(txt_content))
            )
        
        
        # Encerramento da Linha
        txt_content = txt_content + "\r\n"
    
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        
        context.update({'default_res_id': ids[0], 'default_res_model': 'convenio115'})

        attach_id = attach_obj.create(cr, uid, {'name': attach_name,
                                                'datas': base64.encodestring(txt_content),
                                                'datas_fname': file_name}, context=context)
        
        return attach_id
    
    
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
        
    # Função para gerar a autenticação digital da nota fiscal
    # Recebe os campos necessários para a geração do código
    def gerar_autenticacao_digital(self, cnpj_destinatario, numero_nota, valor_total,
                                   base_calculo_icms, valor_icms, data_emissao, cnpj_emitente):
        # importa classe python com implementação do algoritmo MD5
        import md5
        
        # gera a autenticação com a aplicação do MD5 nos campos repassados
        autenticacao_digital = md5.new(cnpj_destinatario + "" + numero_nota + "" + valor_total + "" + 
                                   base_calculo_icms + "" + valor_icms + "" + data_emissao + "" + cnpj_emitente)
        
        # retornando a autenticação  
        return autenticacao_digital.hexdigest()
    
    # Função para gerar a autenticação digital do registro
    def gerar_autenticacao_digital_registro(self, string_registro):
        # importa classe python com implementação do algoritmo MD5
        import md5
        
        # gera a autenticação com a aplicação do MD5 nos campos repassados
        autenticacao_digital = md5.new(string_registro)
        
        # retornando a autenticação  
        return autenticacao_digital.hexdigest()

    
    def on_change_mes_ano(self, cr, user, ids, mes, ano, context=None):
        import calendar
        if mes:
            if ano:
                res = {}

                res['domain'] = {'notas_fiscais': [('date_invoice', '>=', '01-'+mes+'-'+ano),
                                                   ('date_invoice', '<=', ''+str(calendar.monthrange(int(ano), int(mes))[1])+'-'+mes+'-'+ano)]}
                
                return res