# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Atendimento(models.Model):
    _name = 'atendimento'
    _description = 'Atendimento'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Many2one(
        comodel_name='protocolo',
        string='Protocolo',
        help='Protocolo ao qual está vinculado o atendimento',
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do status de adesão",
        track_visibility="onchange")
    
    manifestacao_atendimento = fields.Many2one(
        comodel_name='manifestacao_atendimento',
        string='Manifestacao',
        help='Manifestação do atendimento',
        track_visibility='onchange')
    
    grupo_atendimento = fields.Many2one(
        comodel_name='grupo_atendimento',
        string='Grupo',
        help='Grupo do atendimento',
        track_visibility='onchange')
    
    protocolo = fields.Many2one(
        comodel_name='protocolo',
        string='Protocolo',
        help='Protocolo ao qual está vinculado o atendimento',
        track_visibility='onchange')
    
    
    tipo_atendimento = fields.Many2one(
        comodel_name='tipo_atendimento',
        string='Tipo',
        help='Status do contrato',
        track_visibility='onchange')
    
    procedimento = fields.Text('Procedimento', related='tipo_atendimento.procedimento', store=True)
    
    orientacao = fields.Text('Orientacao', related='tipo_atendimento.orientacao', store=True)
    
    manual = fields.Binary('Manual', related='tipo_atendimento.manual', store=True)
    
    manual_filename = fields.Char('Arquivo do Manual', related='tipo_atendimento.manual_filename', store=True)
    
    previsao_resolucao = fields.Date(
        string="Previsao de Resolucao",
        help="Data prevista para a resolução do problema de acordo com o tipo de atendimento")
    
    reclamacao = fields.Text(
        string="Reclamacao",
        help="Descrição da reclamação do cliente")
    
    documentacao = fields.Selection(
        selection=[('0', 'Documentos Pendentes'),
                   ('1', 'Documentos Recebidos')],
        string="Documentacao",
        help="A documentação necessária para o atendimento ao cliente foi entregue ou há alguma pendência por parte do cliente?")
    
    solicitacao_atendida = fields.Selection(
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        string="Solicitacao Atendida",
        help="A solicitação/reclamação do cliente foi atendida pela Cinte?")
    
    previsao_resolucao = fields.Date(
        string="Previsao de Resolucao",
        help="Data prevista para resolução de acordo com o tipo de atendimento")
    
    data_conclusao = fields.Date(
        string="Data de Conclusao",
        help="Data de conclusão do atendimento")
    
    status_atendimento = fields.Many2one(
        comodel_name='status_atendimento',
        string='Status',
        help='Andamento da solicitação do cliente',
        track_visibility='onchange')
    