# -*- coding: utf-8 -*-
from openerp import models, fields

class Ponto_interno(models.Model):
    _name = 'ponto.interno' 
    
    localidade = fields.Char(
        string="Localidade",
        size=150,
        required=True)
    
    endereco = fields.Char(
        string="Endereço",
        size=150,
        required=True)
    
    data_agendada_instalacao = fields.Date(
        string='Data Agendada de Instalação',
        help='Data prevista para a instalação')
    
    latitude = fields.Char(
        string="Latitude",
        size=150,
        required=True)
    
    longitude = fields.Char(
        string="Longitude",
        size=150,
        required=True)
    
    observacoes_gerais = fields.Text(
        string='Observacões',
        help='Observacões sobre o ponto do projeto')
    
    disponibilidade_minima  = fields.Float(
        string='Disponibilidade Mínima',
        help='Disponibilidade Mínima do Link')
    
    tempo_maximo_projeto_execucao_radio = fields.Integer(
        string="Tempo máximo de Projeto + Execução (dias)")
    
    modelo_radio = fields.Char(
        string="Modelo do Rádio",
        size=150)
    
    altura_necessaria_cliente = fields.Float(
        string='Altura necessária no cliente',
        help='Altura necessária no cliente')
    
    altura_necessaria_cinte = fields.Float(
        string='Altura necessária na Cinte',
        help='Altura necessária na Cinte')
    
    velocidade_maxima_radio = fields.Float(
        string='Velocidade Máxima',
        help='Velocidade Máxima')
    
    distancia_link = fields.Float(
        string='Distância do Link (km)',
        help='Distância do Link (km)')
    
    modelo_antenas = fields.Char(
        string="Modelo das Antenas",
        size=150)
    
    pop_radio = fields.Many2one(
        comodel_name='x_project.pop',
        string='POP',
        help='POP')
    
    tempo_maximo_projeto_execucao = fields.Integer(
        string="Tempo máximo de Projeto + Execução (dias)")
    
    tamanho_percurso = fields.Float(
        string='Tamanho do Percurso (m)',
        help='Tamanho do Percurso (m)')
    
    modelo_conversores = fields.Char(
        string="Modelo dos Conversores",
        size=150)
    
    pop = fields.Many2one(
        comodel_name='x_project.pop',
        string='POP',
        help='POP')
    
    velocidade_maxima = fields.Float(
        string='Velocidade Máxima',
        help='Velocidade Máxima')
    
    modelo_fibra = fields.Char(
        string="Modelo da Fibra",
        size=150)
    
    tronco = fields.Many2one(
        comodel_name='x_project.tronco',
        string='Tronco',
        help='Tronco')
    
    project_id = fields.Integer(
        string="ID do Projeto")
    
    equipe_projeto_radio = fields.One2many(
        comodel_name='x_equipe_projeto',
        inverse_name='x_ponto_interno_id_radio',
        string='Equipe do Projeto',
        help='Equipe do Projeto')
        
    equipe_projeto = fields.One2many(
        comodel_name='x_equipe_projeto',
        inverse_name='x_ponto_interno_id',
        string='Equipe do Projeto',
        help='Equipe do Projeto')
    
    lista_materiais_radio = fields.One2many(
        comodel_name='x_materiais_projeto',
        inverse_name='x_ponto_interno_id_radio',
        string='Lista de Materiais',
        help='Lista de Materiais')
    
    lista_materiais = fields.One2many(
        comodel_name='x_materiais_projeto',
        inverse_name='x_ponto_interno_id',
        string='Lista de Materiais',
        help='Lista de Materiais')
    
    aprovacao_comercial = fields.Selection(
        selection=[('0', 'Aprovado'),
                   ('1', 'Reprovado')],
        string='Aprovação Comercial',
        help='Análise e aprovação do comercial')
    
    aprovacao_comercial_observacoes = fields.Text(
        string='Observações',
        help='Observações referentes a aprovação comercial para a região/ponto.')
    
        