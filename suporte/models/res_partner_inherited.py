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
        string="Informacoes Tecnicas",
        help="Informações técnicas sobre o cliente",
        track_visibility='onchange')
    
    textos_chamados = fields.Text(
        string="Textos de Chamados",
        help="Textos padrões para os chamados dos clientes",
        track_visibility='onchange')
    
    usuario_centreon = fields.Char(
        string="Usuario Centreon",
        size=30,
        track_visibility='onchange')
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    
    data_nascimento = fields.Date(
        string='Data de Nascimento',
        help='Data de Nascimento',
        track_visibility='onchange'
        )
    
    orgao_emissor_rg = fields.Char(
        string="Orgao Emissor do RG",
        size=30,
        track_visibility='onchange')
    
    profissao = fields.Many2one(
        comodel_name='l10n_br_hr.cbo',
        string='Profissao',
        help='Profissão',
        track_visibility='onchange')

    contato_cliente = fields.One2many(
        comodel_name='contato_cliente',
        inverse_name='cliente',
        string='Contatos do Cliente',
        help='Contatos do cliente',
        track_visibility="onchange")

    senha_site = fields.Char(
        string="Senha de Acesso ao Site",
        size=100,
        help="Senha de acesso a área de suporte do site.",
        track_visibility='onchange'
    )
    

    def get_contatos_notificacoes(self, cr, user, ids, context=None):
        obj_parceiro = self.pool.get('res.partner').browse(cr, user, ids)

        retorno = ''
        for contato in obj_parceiro.contato_cliente:
            if contato.name == '1':
                retorno = retorno + contato.contato + ','

        return retorno[:-1]