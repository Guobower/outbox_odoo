# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Adesao(models.Model):
    _name = 'adesao'
    _description = 'Adesao de Contratos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Adesao",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição da Adesão",
        track_visibility="onchange")
    
    contrato = fields.Many2one(
        string="Contrato",
        comodel_name='account.analytic.account',
        help="Contrato ao qual a adesão está vinculada")
    
    atendimento = fields.One2many(
        comodel_name='atendimento',
        inverse_name='adesao',
        string='Atendimentos',
        help='Atendimentos vinculados a adesão')
    
    protocolo = fields.One2many(
        comodel_name='protocolo',
        inverse_name='adesao',
        string='Protocolos',
        help='Protocolos vinculados a adesão')
    
    conexao = fields.One2many(
        comodel_name='conexao_cliente',
        inverse_name='adesao',
        string='Conexao',
        help='Conexões vinculadas à adesão do contrato')
    
    pop = fields.Many2one(
        comodel_name='pop',
        string='Pop',
        help='Pop ao qual a adesão está vinculada',
        track_visibility='onchange')
    
    plano = fields.Many2one(
        comodel_name='plano',
        string='Plano',
        help='Plano ao qual a adesão está vinculada',
        track_visibility='onchange')
    
    modo_aquisicao = fields.Many2one(
        comodel_name='modo_aquisicao',
        string='Modo de Aquisicao',
        help='Modo de aquisicao do material',
        track_visibility='onchange')
    
    numero_serie = fields.Many2many(
        comodel_name='stock.production.lot',
        string='Número de Serie',
        help='Material vinculado a esta instalação',
        track_visibility='onchange')
    
    status_adesao = fields.Many2one(
        comodel_name='status_adesao',
        string='Status',
        help='Status da adesão',
        track_visibility='onchange')
    
    data_adesao = fields.Date(
        string='Data da Adesão',
        help='Data da Adesão',
        track_visibility='onchange')
    
    data_cancelamento = fields.Date(
        string='Data do Cancelamento',
        help='Data do Cancelamento',
        track_visibility='onchange')
    
    data_vencimento = fields.Date(
        string='Data de Vecimento',
        help='Data de Vencimento',
        track_visibility='onchange')
    
    data_ultima_ativacao = fields.Date(
        string='Data da Última Ativação',
        help='Data da Última Ativação',
        track_visibility='onchange')
    
    data_ultima_suspensao = fields.Date(
        string='Data da Última Suspensão',
        help='Data da Última Suspensão',
        track_visibility='onchange')
    
    lacre = fields.Char(
        string='Lacre',
        help='Lacre',
        size=40,
        track_visibility='onchange')
    
    login = fields.Char(
        string='Login',
        help='Login',
        size=30,
        track_visibility='onchange')
    
    senha = fields.Char(
        string='Senha',
        help='Senha',
        size=30,
        track_visibility='onchange')
    
    latitude = fields.Char(
        string="Latitude",
        size=45,
        help="Latitude da adesão",
        track_visibility="onchange")
    
    longitude = fields.Char(
        string="Longitude",
        size=45,
        help="Longitude da adesão",
        track_visibility="onchange")
    
    cep = fields.Char(
        string="CEP",
        size=10,
        help="CEP",
        track_visibility="onchange")
    
    logradouro = fields.Char(
        string="Logradouro",
        size=300,
        help="Logradouro",
        track_visibility="onchange")
    
    numero = fields.Char(
        string="Numero",
        size=20,
        help="Número",
        track_visibility="onchange")
    
    bairro = fields.Char(
        string="Bairro",
        size=80,
        help="Bairro",
        track_visibility="onchange")
    
    cidade = fields.Many2one(
        string='Cidade',
        help='Cidade',
        comodel_name='l10n_br_base.city',
        track_visibility="onchange")
    
    estado = fields.Many2one(
        string='Estado',
        help='Estado',
        comodel_name='res.country.state',
        track_visibility="onchange")
    
    complemento = fields.Char(
        string="Complemento",
        size=100,
        help="Complemento",
        track_visibility="onchange")
    
    ponto_referencia = fields.Text(
        string="Ponto de Referencia",
        help="Ponto de referência",
        track_visibility="onchange")
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    
    
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
    
    
    def report_format_data(self,data_padrao, context=None):
        '''
            Descrição:
              Formatar valores como data em formato brasileiro para a exibição em relatórios.
        
            Utilização:
              report_format_data(param1)
        
            Parâmetros:
              fatura
                Data a ter seu texto formatado
        '''
        if data_padrao:
            return data_padrao[8:10]+"/"+data_padrao[5:7]+"/"+data_padrao[0:4]
                           
    def gerar_pdf_adesao(self, cr, user, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo imprimir um pdf da Adesão para assinatura do cliente.
        
            Utilização:
              gerar_pdf_adesao()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da adesão em questão
              context
                Contexto atual
        '''
        
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'suporte.report_adesao',
            'context': context,
        }
    
    
    def on_change_estado(self, cr, user, ids, estado, context=None):
        '''
            Descrição:
              Esta função tem como objetivo modificar o dominio das cidades para que exiba apenas as vinculados ao 
              estado selecionado.
        
            Utilização:
              on_change_estado(param1)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              estado
                Estado selecionado no formulario  
              context
                Contexto atual
        '''
        return {'domain':{'cidade':[('state_id', '=', estado)]}}
    
    def carregar_coordenadas(self, cr, user, ids, context=None):
        import simplejson, urllib
        
        adesao = self.pool.get('adesao').browse(cr, user, ids[0])
        
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + adesao.logradouro + ","
            
            if adesao.numero:
                url = url + adesao.numero + ","
            
            url = url + adesao.bairro + "," + adesao.cidade.name + "-" + adesao.estado.code + "&key=AIzaSyBRXLYF_PsJjlo-s0NIUXr_186CmZpf0hI"
            url = url.encode('utf-8')
            result = simplejson.load(urllib.urlopen(url))
    
            # distancia = (result['rows'][0]['elements'][0]['distance']['value']) / 1000
            # tempoViagem = (result['rows'][0]['elements'][0]['duration']['value']) / 60
            latitude = (result['results'][0]['geometry']['location']['lat'])
            longitude = (result['results'][0]['geometry']['location']['lng'])
            
            
            
            adesao.write({'latitude': str(latitude), 'longitude': str(longitude)}, context=context)
            # Return the values to update it in the view.
            res = {
                    'value': {
                    'latitude': str(latitude),
                    'longitude': str(longitude)
                    }
            }
            # Return the values to update it in the view.
            return res
        except IndexError:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Não encontrado!',
                    'text': 'Coordenadas não encontradas!'
                    }
            }
        

        
    def on_change_zip(self, cr, user, ids, cep, context=None):
        import pycep_correios
        from pycep_correios.excecoes import (CEPInvalido,
                                     ExcecaoPyCEPCorreios,
                                     Timeout,
                                     MultiploRedirecionamento,
                                     FalhaNaConexao)

        try:
            if cep:
                cep = cep.replace("-", "").replace(".", "")
                endereco = pycep_correios.consultar_cep(cep)
                
                estado_obj = self.pool.get('res.country.state')
                estado = estado_obj.search(cr, user, [('code', '=', endereco['uf'])])
                # estado = estado_obj.browse(cr, user, estado_obj.search(cr, user,  [('code','=',endereco['uf'])]))
                
                cidade_obj = self.pool.get('l10n_br_base.city')
                cidade = cidade_obj.search(cr, user, [('name', '=', endereco['cidade']), ('state_id', '=', estado[0])])
                
                res = {
                    'value': {
                    'logradouro': endereco['end'],
                    'bairro': endereco['bairro'],
                    'complemento': endereco['complemento'],
                    'estado': estado[0],
                    'cidade': cidade[0]
                    }
                }
                # Return the values to update it in the view.
                return res
        except Timeout as exc:
            return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Tempo excedido!',
                        'text': 'Tempo excedido na consulta de CEP!'
                        }
                }
        except FalhaNaConexao as exc:
            return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Falha de conexão!',
                        'text': 'Falha de conexão na consulta de CEP!'
                        }
                }
        except MultiploRedirecionamento as exc:
            return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Erro de redirecionamento!',
                        'text': 'Erro de redirecionamento na consulta de CEP!'
                        }
                }
        except CEPInvalido as exc:
            return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'CEP inválido!',
                        'text': 'O CEP informado é inválido!'
                        }
                }
        except ExcecaoPyCEPCorreios as exc:
            return {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Erro ao consultar!',
                        'text': 'Erro ao consultar CEP!'
                        }
                }
            
