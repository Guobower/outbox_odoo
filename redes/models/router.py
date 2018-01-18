# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Router(models.Model):
    _name = 'router'
    _description = 'Router'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'torre': {
                'torre.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'torre.mt_login': lambda self, cr, uid, obj, ctx = None: obj.login,
                'torre.mt_nas': lambda self, cr, uid, obj, ctx = None: obj.nas,
                'torre.mt_torre': lambda self, cr, uid, obj, ctx = None: obj.torre,
                'torre.mt_pop': lambda self, cr, uid, obj, ctx = None: obj.pop,
                'torre.mt_ip': lambda self, cr, uid, obj, ctx = None: obj.ip,
                'torre.mt_mac': lambda self, cr, uid, obj, ctx = None: obj.mac,
                'torre.mt_modo_autenticacao': lambda self, cr, uid, obj, ctx = None: obj.modo_autenticacao,
                'torre.mt_tipo_nas': lambda self, cr, uid, obj, ctx = None: obj.tipo_nas,
                'torre.mt_frame': lambda self, cr, uid, obj, ctx = None: obj.frame,
                'torre.mt_slot_id': lambda self, cr, uid, obj, ctx = None: obj.slot_id,
                'torre.mt_prompt': lambda self, cr, uid, obj, ctx = None: obj.prompt,
                'torre.mt_oid': lambda self, cr, uid, obj, ctx = None: obj.oid
            }
    }
    
    name = fields.Char(
        string="Name",
        size=60,
        required=True,
        track_visibility='onchange')
    
    login = fields.Char(
        string="Login",
        size=45,
        track_visibility='onchange')
    
    senha = fields.Char(
        string="Senha",
        size=100)
    
    nas = fields.Selection(
        string="Nas",
        help="Nas",
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        track_visibility="onchange")
    
    
    torre = fields.Many2one(
        string='Torre',
        help='Torre',
        comodel_name='torre',
        track_visibility="onchange")
    
    pop = fields.Many2one(
        string='Pop',
        help='Pop',
        comodel_name='pop',
        track_visibility="onchange")
    
    ip = fields.Char(
        string="IP",
        size=25,
        track_visibility='onchange')
    
    mac = fields.Char(
        string="MAC",
        size=45,
        track_visibility='onchange')
    
    modo_autenticacao = fields.Selection(
        string="Modo Autenticacao",
        help="Modo de Autenticação",
        selection=[('1', 'Radius'),
                   ('2', 'SSH'),
                   ('3', 'SNMP'),
                   ('4', 'Telnet')],
        track_visibility="onchange")
    
    tipo_nas = fields.Selection(
        string="Tipo de NAS",
        help="Tipo de NAS",
        selection=[('mikrotic', 'mikrotic'),
                   ('cdata', 'cdata'),
                   ('huawei', 'huawei')],
        track_visibility="onchange")
    
    frame = fields.Integer(
        string="Frame",
        help="Frame.",
        track_visibility="onchange")
    
    slot_id = fields.Integer(
        string="Slot id",
        help="Slot id.",
        track_visibility="onchange")
    
    prompt = fields.Char(
        string="Prompt",
        size=130,
        track_visibility='onchange')
    
    oid = fields.Char(
        string="Oid",
        size=50,
        track_visibility='onchange')
    
    id_syncron = fields.Integer(
        string='ID do router no Syncron',
        help='ID de identificação do router no Syncron')
