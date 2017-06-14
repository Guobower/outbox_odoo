# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Atividades_cinte(models.Model):
    _name = 'atividades_cinte'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)
    
    atividade = fields.Text(
        string='Atividade/Pendência',
        help='Atividade/Pendência a ser desenvolvida')
    
    status = fields.Selection(
        selection=[('resolvida', 'Resolvida'),
                   ('pendente', 'Pendente'),
                   ('cancelada', 'Cancelada')],
        string='Status',
        help='Status da atividade')
    
    prioridade = fields.Selection(
        selection=[('0', 'Nenhuma'),
                   ('1', 'Muito Baixa'),
                   ('2', 'Baixa'),
                   ('3', 'Media'),
                   ('4', 'Alta'),
                   ('5', 'Muito Alta')],
        string='Prioridade',
        help='Prioridade da atividade')
    
    observacoes = fields.Text(
        string='Observacões',
        help='Observacões sobre a atividade')

    dataPrevisao = fields.Date(
        string='Previsão de Conclusão',
        help='Data prevista para a conclusão da atividades')
    
    dataConclusao = fields.Date(
        string='Conclusão',
        help='Data de conclusão da atividade')
    
    observacoesGestao = fields.Text(
        string='Observacões do Gestor/Avaliador',
        help='Observacões do gestor/avaliador')
    
    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável pela atividade')
    
    equipe = fields.Many2many(
        comodel_name='res.users',
        string='Equipe',
        help='Equipe envolvida na atividade')