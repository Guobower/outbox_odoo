# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Pop(models.Model):
    _name = 'pop'
    _description = 'Pop'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'pop': {
                'pop.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'pop.mt_cidade': lambda self, cr, uid, obj, ctx = None: obj.cidade,
                'pop.mt_populacao': lambda self, cr, uid, obj, ctx = None: obj.populacao,
                'pop.mt_central': lambda self, cr, uid, obj, ctx = None: obj.central
            }
    }
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True,
        track_visibility='onchange')
    
    populacao = fields.Char(
        string="Populacao",
        size=10,
        help="População",
        track_visibility="onchange")
    
    central = fields.Selection(
        string="Central",
        help="Central",
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        track_visibility="onchange")
    
    cidade = fields.Many2one(
        string='Cidade',
        help='Cidade',
        comodel_name='l10n_br_base.city',
        track_visibility="onchange",
        domain=[('state_id', '=', 70)])
    
    id_syncron = fields.Integer(
        string='ID do pop no Syncron',
        help='ID de identificação do pop no Syncron')
    
    
