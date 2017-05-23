# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Ponto_cliente_mudanca(models.Model):
    _name = 'ponto_cliente_mudanca'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    
    localidade = fields.Char(
        string='Localidade', 
        help='Localidade do ponto do cliente')
    
    endereco = fields.Char(
        string='Endereço', 
        help='Endereço do ponto do cliente', 
        required=True)
    
    latitude = fields.Char(
        string='Latitude', 
        help='Latitude do ponto do cliente')
    
    longitude = fields.Char(
        string='Longitude', 
        help='Longitude do ponto do cliente')
    
    valor = fields.Float(
        string='Valor', 
        help='Valor negociado com o cliente')
    
    despesas_instalacao = fields.Selection(
        [('cinte', 'Cinte'),('cliente', 'Cliente'),('dividida', 'Dividida')],
        string='Despesas da Instalação', 
        help='Despesas da instalação serão da Cinte, cliente ou dividida?')
    
    data_agendada_instalacao = fields.Date(
        string='Data de instalação agendada', 
        help='Data de instalação agendada pelo operacional')
    
    observacoes = fields.Text(
        string='Observações', 
        help='Observações gerais quanto ao ponto')
