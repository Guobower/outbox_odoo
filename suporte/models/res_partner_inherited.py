# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Res_partner_inherited(models.Model):
    _inherit = 'res.partner' 
 
    _track = {
            'res.partner': {
                'resp.partner.mt_informacoes_tecnicas': lambda self, cr, uid, obj, ctx = None: obj.informacoes_tecnicas,
                'resp.partner.mt_textos_chamados': lambda self, cr, uid, obj, ctx = None: obj.textos_chamados,
                'resp.partner.mt_sla': lambda self, cr, uid, obj, ctx = None: obj.sla,
                'resp.partner.mt_usuario_centreon': lambda self, cr, uid, obj, ctx = None: obj.usuario_centron
            }
    }
    
    informacoes_tecnicas = fields.Text(
        string="Informações Técnicas",
        help="Informações técnicas sobre o cliente",
        track_visibility='onchange')
    
    textos_chamados = fields.Text(
        string="Textos de Chamados",
        help="Textos padrões para os chamados dos clientes",
        track_visibility='onchange')
    
    sla = fields.Selection(
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        string='SLA',
        help='Cliente possui SLA?',
        track_visibility='onchange')
    
    usuario_centreon = fields.Char(
        string="Usuário Centreon",
        size=30,
        track_visibility='onchange')
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    
    
    
    
    
