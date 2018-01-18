# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Torre(models.Model):
    _name = 'torre'
    _description = 'Torre'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'torre': {
                'torre.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'torre.mt_sustentavel': lambda self, cr, uid, obj, ctx = None: obj.sustentavel,
                'torre.mt_altura': lambda self, cr, uid, obj, ctx = None: obj.altura,
                'torre.mt_latitude': lambda self, cr, uid, obj, ctx = None: obj.latitude,
                'torre.mt_longitude': lambda self, cr, uid, obj, ctx = None: obj.longitude,
                'torre.mt_cep': lambda self, cr, uid, obj, ctx = None: obj.cep,
                'torre.mt_logradouro': lambda self, cr, uid, obj, ctx = None: obj.logradouro,
                'torre.mt_numero': lambda self, cr, uid, obj, ctx = None: obj.numero,
                'torre.mt_bairro': lambda self, cr, uid, obj, ctx = None: obj.bairro,
                'torre.mt_cidade': lambda self, cr, uid, obj, ctx = None: obj.cidade,
                'torre.mt_estado': lambda self, cr, uid, obj, ctx = None: obj.estado,
                'torre.mt_complemento': lambda self, cr, uid, obj, ctx = None: obj.complemento,
                'torre.mt_ponto_referencia': lambda self, cr, uid, obj, ctx = None: obj.ponto_referencia
            }
    }
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True,
        track_visibility='onchange')
    
    sustentavel = fields.Selection(
        string="Sustentavel",
        help="Sustentável",
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        track_visibility="onchange")
    
    altura = fields.Integer(
        string="Altura (m)",
        help="Altura da torre.",
        track_visibility="onchange")
    
    latitude = fields.Char(
        string="Latitude",
        size=45,
        help="Latitude da torre",
        track_visibility="onchange")
    
    longitude = fields.Char(
        string="Longitude",
        size=45,
        help="Longitude da torre",
        track_visibility="onchange")
    
    cep = fields.Char(
        string="CEP",
        size=10,
        help="CEP",
        track_visibility="onchange")
    
    logradouro = fields.Char(
        string="Logradouro",
        size=300,
        required=True,
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
        required=True,
        help="Bairro",
        track_visibility="onchange")
    
    cidade = fields.Many2one(
        string='Cidade',
        help='Cidade',
        required=True,
        comodel_name='l10n_br_base.city',
        track_visibility="onchange")
    
    estado = fields.Many2one(
        string='Estado',
        help='Estado',
        required=True,
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
        string='ID do torre no Syncron',
        help='ID de identificação da torre no Syncron')
    
    
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
        
        torre = self.pool.get('torre').browse(cr, user, ids[0])
        
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json?address="+torre.logradouro+","
            
            if torre.numero:
                url = url + torre.numero+","
            
            url = url + torre.bairro+","+torre.cidade.name+"-"+torre.estado.code+"&key=AIzaSyBRXLYF_PsJjlo-s0NIUXr_186CmZpf0hI"
            url = url.encode('utf-8')
            result = simplejson.load(urllib.urlopen(url))
    
            # distancia = (result['rows'][0]['elements'][0]['distance']['value']) / 1000
            # tempoViagem = (result['rows'][0]['elements'][0]['duration']['value']) / 60
            latitude = (result['results'][0]['geometry']['location']['lat'])
            longitude = (result['results'][0]['geometry']['location']['lng'])
            
            
            
            torre.write({'latitude': str(latitude),'longitude': str(longitude)}, context=context)
            # Return the values to update it in the view.
            return {
                'type': 'ir.actions.client',
                'tag': 'reload'
            }
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
            
            
        
