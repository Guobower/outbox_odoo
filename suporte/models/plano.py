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
        help='Valor mensal (R$)')
    
    download = fields.Integer(
        string="Download (kbps)",
        help="Taxa de download do plano")
    
    upload = fields.Integer(
        string="Upload (kbps)",
        help="Taxa de upload do plano")
    
    transferencia_mensal = fields.Integer(
        string="Transferência Mensal (Gb)",
        help="Transferência Mensal")
    
    codigo_plano = fields.Char(
        string="Plano",
        size=250,
        track_visibility='onchange')
    
    pos_pago = fields.Selection(
        string="Pós-Pago",
        help="Pós-Pago",
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        track_visibility="onchange")
    
    numero_parcelas = fields.Integer(
        string="Numero de Parcelas",
        help="Numero de Parcelas")
    
    valor_adesao = fields.Float(
        string='Valor da Instalação (R$)',
        help='Valor a ser pago no ato da instalação')
    
    adesao_desconto = fields.Float(
        string='Desconto da Instalação (R$)',
        help='Valor a ser descontado da taxa de instalação')
    
    valor_aluguel = fields.Float(
        string='Valor de Aluguel',
        help='Valor de Aluguel')
    
    comissao_mensal = fields.Float(
        string='Comissão Mensal (Em espécie)',
        help='Comissão Mensal (Em espécie)')
    
    comissao_inicial = fields.Float(
        string='Comissão Inicial (Em espécie)',
        help='Comissão Inicial (Em espécie)')
    
    traffic_table_id = fields.Integer(
        string="traffic_table_id",
        help="traffic_table_id")
    
    ont_lineprofile_id = fields.Integer(
        string="ont_lineprofile_id",
        help="ont_lineprofile_id")
    
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
        help='Pop onde valerá este plano')
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    