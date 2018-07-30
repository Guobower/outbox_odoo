# -*- coding: utf-8 -*-
import datetime
from openerp import api
from openerp import fields
from openerp import models

class Lote_ocorrencias(models.Model):
    _name = 'lote_ocorrencias'
    _description = 'Lote de Ocorrencias'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _defaults = {
        'data_ultima_abertura': datetime.date.today()
        }
    
    name = fields.Char(
                       string="Titulo",
                       size=250,
                       required=True,
                       track_visibility='onchange')
                       
    contrato = fields.Many2one(
                               string="Contrato",
                               comodel_name='account.analytic.account',
                               required=True,
                               help="Contrato ao qual a ocorrência está vinculada")
    
    descricao = fields.Text(
                            string="Descricao",
                            help="Descrição da ocorrência",
                            required=True,
                            track_visibility="onchange")
    
    tipo_ocorrencia = fields.Many2one(
                                      comodel_name='tipo_ocorrencia',
                                      string='Tipo',
                                      help='Tipo da ocorrêmcia',
                                      required=True,
                                      track_visibility='onchange')
                                      
        
    localidade = fields.Many2many(
                                 comodel_name='localidade',
                                 string='Localidade',
                                 help='Localidade',
                                 required=True,
                                 track_visibility='onchange')
    
    imputavel = fields.Selection(
                                 string="Imputavel",
                                 help="Ocorrência deve ser imputada?",
                                 selection=[(1, 'Não'),
                                 (2, 'Sim')],
                                 track_visibility="onchange")
                                
    informacoes_tecnicas = fields.Text('Informacoes Tecnicas', related='contrato.partner_id.informacoes_tecnicas', store=True)
     
    textos_chamados = fields.Text('Textos de chamados', related='contrato.partner_id.textos_chamados', store=True) 
    
    #contato_localidade = fields.One2many('Contatos de Localidades', related='contrato.contato_localidade', store=True) 
    
    
    
    def on_change_tipo(self, cr, user, ids, tipo_ocorrencia, context=None):
        '''
            Descrição:
              Esta função tem como objetivo modificar o titulo e o texto padrao do chamado
              de acordo com o tipo.
        
            Utilização:
              on_change_tipo(param1)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              tipo_ocorrencia
                Tipo da ocorrência selecionado no formulario  
              context
                Contexto atual
        '''
        if tipo_ocorrencia:
            tipo = self.pool.get('tipo_ocorrencia').browse(cr, user, tipo_ocorrencia)
            res = {
                'value': {
                    # Define a distancia entre as cidades e o tempo médio do percurso.
                    'name': tipo.titulo_padrao,
                    'descricao': tipo.texto_padrao
                }
            }
            # Return the values to update it in the view.
            return res
        
        
    @api.model
    def create(self, values):
        import datetime
        # Override the original create function for the res.partner model
        record = super(Lote_ocorrencias, self).create(values)
        
        for item in record['localidade']:
            valores = {
                'contrato': record['contrato'].id,
                'titulo': str(record['name']).replace('#cidade#', '' + item.name),
                'descricao': str(record['descricao']).replace('#cidade#', '' + item.name),
                'tipo_ocorrencia': record['tipo_ocorrencia'].id,
                'status_ocorrencia': 1,
                'localidade': item.id,
                'imputavel': record['imputavel']
            }

            obj_ocorrencia = self.env['ocorrencia'].create(valores)
        
        # Return the record so that the changes are applied and everything is stored.
	return record