# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Localidade(models.Model):
    _name = 'localidade'
    _description = 'Localidades de clientes licitados'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
                       string="Nome",
                       size=250,
                       required=True,
                       track_visibility='onchange')
    
    contrato = fields.Many2one(
                               string="Contrato",
                               comodel_name='account.analytic.account',
                               help="Contrato ao qual a localidade está vinculada")
                               
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
                                   
    torre = fields.Many2one(
                            string='Torre',
                            help='Torre ao qual a localidade está vinculada',
                            comodel_name='torre',
                            track_visibility="onchange")         
                                   
    pop = fields.Many2one(
                          string='Pop',
                          help='Pop ao qual a localidade está vinculada',
                          comodel_name='pop',
                          track_visibility="onchange")         
                                   
    contato_localidade = fields.One2many(
                                         comodel_name='contato_localidade',
                                         inverse_name='localidade',
                                         string='Contatos das Localidades',
                                         help='Contatos das localidades vinculadas ao contrato',
                                         track_visibility="onchange")   
                                   
    informacoes_tecnicas = fields.Text(
                                       string='Informacoes Tecnicas',
                                       help='Informações e dados técnicos extras sobre esta localidade',
                                       track_visibility="onchange")
                            
                            
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
        
        localidade = self.pool.get('localidade').browse(cr, user, ids[0])
        
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + localidade.logradouro + ","
            
            if localidade.numero:
                url = url + localidade.numero + ","
            
            url = url + localidade.bairro + "," + localidade.cidade.name + "-" + localidade.estado.code + "&key=AIzaSyBRXLYF_PsJjlo-s0NIUXr_186CmZpf0hI"
            url = url.encode('utf-8')
            result = simplejson.load(urllib.urlopen(url))
    
            # distancia = (result['rows'][0]['elements'][0]['distance']['value']) / 1000
            # tempoViagem = (result['rows'][0]['elements'][0]['duration']['value']) / 60
            latitude = (result['results'][0]['geometry']['location']['lat'])
            longitude = (result['results'][0]['geometry']['location']['lng'])
            
            
            
            localidade.write({'latitude': str(latitude), 'longitude': str(longitude)}, context=context)
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
                                    