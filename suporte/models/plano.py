# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Plano(models.Model):
    _name = 'plano'
    _description = 'Planos para clientes'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _defaults = {
        'active': True
    }
    
    name = fields.Char(
                       string="Plano",
                       size=250,
                       required=True,
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
        
    plano_cidade = fields.One2many(
                                   comodel_name='plano_cidade',
                                   inverse_name='name',
                                   string='Plano nas Cidades',
                                   help='Configuração do plano para cada cidade',
                                   track_visibility="onchange")   
                                   
    active = fields.Boolean(
                            string="Ativo",
                            help="Plano ativo ou não",
                            track_visibility='onchange'
                            )