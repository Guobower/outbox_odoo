# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Plano_cidade(models.Model):
    _name = 'plano_cidade'
    _description = 'Planos associados nas cidades'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _defaults = {
        'active': True
    }
    
    name = fields.Many2one(
                           string='Plano',
                           help='Plano do cliente',
                           comodel_name='plano',
                           required=True,
                           track_visibility="onchange")
    
    cidade = fields.Many2one(
                             string='Cidade',
                             help='Cidade',
                             comodel_name='l10n_br_base.city',
                             required=True,
                             track_visibility="onchange")
    
    estado = fields.Many2one(
                             string='Estado',
                             help='Estado',
                             comodel_name='res.country.state',
                             required=True,
                             track_visibility="onchange")
                             
    nome_exibicao = fields.Char(
                                string="Nome de Exibicao",
                                size=250,
                                help='Nome para exibição do plano no site',
                                required=True,
                                track_visibility='onchange')
                                
    valor = fields.Float(
                         string="Mensalidade (R$)",
                         help='Valor da mensalidade',
                         required=True,
                         track_visibility='onchange')
    
    pop = fields.Many2one(
                             string='Pop',
                             help='Pop de conexão',
                             comodel_name='pop',
                             required=True,
                             track_visibility="onchange")
                             
    active = fields.Boolean(
                            string="Ativo",
                            help="Pacote ativo ou não",
                            track_visibility='onchange'
                            )
                         
    descricao = fields.Text(
                            string="Descricao",
                            help="Descrição do Plano para a cidade",
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