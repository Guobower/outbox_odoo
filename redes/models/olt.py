# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Torre(models.Model):
    _name = 'torre'
    _description = 'Torre'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'torre': {
                'torre.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'torre.mt_sustentavel': lambda self, cr, uid, obj, ctx = None: obj.sistema,
                'torre.mt_altura': lambda self, cr, uid, obj, ctx = None: obj.descricao,
                'torre.mt_latitude': lambda self, cr, uid, obj, ctx = None: obj.stage_id,
                'torre.mt_longitude': lambda self, cr, uid, obj, ctx = None: obj.prioridade
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
    
    
    
