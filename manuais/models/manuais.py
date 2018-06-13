# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Manuais(models.Model):
    _name = 'manuais'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _track = {
            'manuais': {
                'manuais.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'manuais.mt_descricao': lambda self, cr, uid, obj, ctx = None: obj.descricao,
                'manuais.mt_pdf_filename': lambda self, cr, uid, obj, ctx = None: obj.pdf_filename,
                'manuais.mt_video': lambda self, cr, uid, obj, ctx = None: obj.video,
                'manuais.mt_status': lambda self, cr, uid, obj, ctx = None: obj.status
            }
    }
    
    _defaults = {
        'status': 'ativo'
    }
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True, 
        track_visibility='onchange')
    
    modulo = fields.Selection(
        string="Modulo",
        selection=[('comunicacoes','Comunicações'),
                   ('crm','CRM'),
                   ('projetos','Projetos'),
                   ('fiscal','Fiscal'),
                   ('contabilidade','Contabilidade'),
                   ('compras','Compras'),
                   ('almoxarifado','Almoxarifado'),
                   ('recursos_humanos','Recursos Humanos'),
                   ('frota','Frota'),
                   ('conhecimento','Conhecimento'),
                   ('relatorios','Relatórios'),
                   ('site','Site'),
                   ('configuracoes','Configurações'),
                   ('suporte','Suporte')],
        help="Módulo ao qual o manual se refere", 
        track_visibility='onchange')
    
    pdf = fields.Binary(
        string='PDF',
        help='PDF do Manual.')
    
    pdf_filename = fields.Char("PDF do Manual", 
        track_visibility='onchange')
    
    video = fields.Char(
        string="Video",
        size=250, 
        track_visibility='onchange')
    
    status = fields.Selection(
        string="Status",
        selection=[('ativo','Ativo'),('obsoleto','Obsoleto')],
        help="Status do manual", 
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Observações e descrições referentes a este manual", 
        track_visibility='onchange')
    
    