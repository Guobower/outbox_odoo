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
        return {'domain':{'cidade':[('state_id','=',estado)]}}