# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Torre(models.Model):
    _name = 'torre'
    _description = 'Torre'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'torre': {
                'torre.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'torre.mt_sustentavel': lambda self, cr, uid, obj, ctx = None: obj.sustentavel,
                'torre.mt_altura': lambda self, cr, uid, obj, ctx = None: obj.altura,
                'torre.mt_latitude': lambda self, cr, uid, obj, ctx = None: obj.latitude,
                'torre.mt_longitude': lambda self, cr, uid, obj, ctx = None: obj.longitude,
                'torre.mt_cep': lambda self, cr, uid, obj, ctx = None: obj.cep,
                'torre.mt_logradouro': lambda self, cr, uid, obj, ctx = None: obj.logradouro,
                'torre.mt_numero': lambda self, cr, uid, obj, ctx = None: obj.numero,
                'torre.mt_bairro': lambda self, cr, uid, obj, ctx = None: obj.bairro,
                'torre.mt_cidade': lambda self, cr, uid, obj, ctx = None: obj.cidade,
                'torre.mt_estado': lambda self, cr, uid, obj, ctx = None: obj.estado,
                'torre.mt_complemento': lambda self, cr, uid, obj, ctx = None: obj.complemento,
                'torre.mt_ponto_referencia': lambda self, cr, uid, obj, ctx = None: obj.ponto_referencia
            }
    }
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True,
        track_visibility='onchange')
    
    sustentavel = fields.Selection(
        string="Sustentavel",
        help="Sustentável",
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        track_visibility="onchange")
    
    altura = fields.Integer(
        string="Altura (m)",
        help="Altura da torre.",
        track_visibility="onchange")
    
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
        comodel_name='l10n_br_base.city')
    
    estado = fields.Many2one(
        string='Estado',
        help='Estado',
        comodel_name='res.country.state')
    
    complemento = fields.Char(
        string="Complemento",
        size=100,
        help="Complemento",
        track_visibility="onchange")
    
    ponto_referencia = fields.Text(
        string="Ponto de Referencia",
        help="Ponto de referência",
        track_visibility="onchange")
    
    
    
