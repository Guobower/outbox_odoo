# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Plano(models.Model):
    _name = 'plano'
    _description = 'Planos para clientes'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Plano",
        size=250,
        required=True,
        track_visibility='onchange')
    
    tarifa_basica = fields.Float(
        string='Valor Mensal (R$)',
        help='Valor mensal (R$)',
        track_visibility='onchange')
    
    download = fields.Integer(
        string="Download (kbps)",
        help="Taxa de download do plano",
        track_visibility='onchange')
    
    upload = fields.Integer(
        string="Upload (kbps)",
        help="Taxa de upload do plano",
        track_visibility='onchange')
    
    transferencia_mensal = fields.Integer(
        string="Transferencia Mensal (Gb)",
        help="Transferência Mensal",
        track_visibility='onchange')
    
    codigo_plano = fields.Char(
        string="Plano",
        size=250,
        track_visibility='onchange')
    
    pos_pago = fields.Selection(
        string="Pos-Pago",
        help="Pós-Pago",
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        track_visibility="onchange")
    
    numero_parcelas = fields.Integer(
        string="Numero de Parcelas",
        help="Numero de Parcelas",
        track_visibility='onchange')
    
    valor_adesao = fields.Float(
        string='Valor da Instalacao (R$)',
        help='Valor a ser pago no ato da instalação',
        track_visibility='onchange')
    
    adesao_desconto = fields.Float(
        string='Desconto da Instalacao (R$)',
        help='Valor a ser descontado da taxa de instalação',
        track_visibility='onchange')
    
    valor_aluguel = fields.Float(
        string='Valor de Aluguel',
        help='Valor de Aluguel',
        track_visibility='onchange')
    
    comissao_mensal = fields.Float(
        string='Comissao Mensal (Em espécie)',
        help='Comissão Mensal (Em espécie)',
        track_visibility='onchange')
    
    comissao_inicial = fields.Float(
        string='Comissao Inicial (Em espécie)',
        help='Comissão Inicial (Em espécie)',
        track_visibility='onchange')
    
    traffic_table_id = fields.Integer(
        string="traffic_table_id",
        help="traffic_table_id",
        track_visibility='onchange')
    
    ont_lineprofile_id = fields.Integer(
        string="ont_lineprofile_id",
        help="ont_lineprofile_id",
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição da Adesão",
        track_visibility="onchange")
    
    grupo_servico = fields.Many2one(
        comodel_name='grupo_servico',
        string='Grupo de Servico',
        help='Grupo de serviço do plano',
        track_visibility='onchange')
    
    pop = fields.Many2many(
        comodel_name='pop',
        string='Pops',
        help='Pop onde valerá este plano',
        track_visibility='onchange')
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron',
        track_visibility='onchange')
    