# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Tipo_servico(models.Model):
    _name = 'tipo_servico'
    _description = 'Tipo de servico'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
                       string="Nome",
                       size=150,
                       required=True,
                       track_visibility='onchange')
                       
    descricao = fields.Text(
                            string="Descricao",
                            track_visibility='onchange'
                            )
        
    grupo_servico = fields.Many2one(
                                    comodel_name='grupo_servico',
                                    string='Grupo de Servico',
                                    help='Grupo de servico ao qual o tipo esta vinculado',
                                    required=True,
                                    track_visibility='onchange')
                              
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    
     