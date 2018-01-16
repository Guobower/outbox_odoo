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
    
    
    #TODO
    '''
    status
    
    numero_serie
    stock.production.lot
    '''