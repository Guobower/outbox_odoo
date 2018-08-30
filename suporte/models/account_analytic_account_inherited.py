# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Account_analytic_account_inherited(models.Model):
    _inherit = 'account.analytic.account' 
 
    _track = {
        'account.analytic.account': {
            'account.analytic.account.mt_stage_id': lambda self, cr, uid, obj, ctx = None: obj.status_contrato
        }
    }
    
    _defaults = {
        'stage_id': 1,
        'type': 'contract'
    }
    
    condicao_pagamento = fields.Many2one(
                                        comodel_name='account.payment.term',
                                        string='Condição de Pagamento',
                                        help='Condição padrão de pagamento do cliente',
                                        required=True,
                                        track_visibility='onchange')

    
    tipo_contrato = fields.Selection(
                                     selection=[('1', 'Banda Larga'),
                                     ('2', 'Corporativo'),
                                     ('3', 'Licitado'),
                                     ('4', 'Provedor')],
                                     string='Tipo de Contrato',
                                     help='Tipo de contrato com o cliente',
                                     required=True,
                                     track_visibility='onchange')

    metodo_pagamento = fields.Selection(
                                    selection=[('1', 'Boleto'),
                                               ('2', 'Fatura')],
                                    string='Método de Pagamento',
                                    help='Método de pagamento do cliente',
                                    required=True,
                                    track_visibility='onchange')
    
    grupo_servico = fields.Many2one(
                                    comodel_name='grupo_servico',
                                    string='Grupo de Servico',
                                    help='Grupo de serviço do plano',
                                    required=True,
                                    track_visibility='onchange')
        
    adesao = fields.One2many(
                             comodel_name='adesao',
                             inverse_name='contrato',
                             string='Adesoes',
                             help='Adesões vinculadas ao contrato')
        
    localidade = fields.One2many(
                                 comodel_name='localidade',
                                 inverse_name='contrato',
                                 string='Localidades',
                                 help='Localidades vinculadas ao contrato')
    
    atendimento = fields.One2many(
                                  comodel_name='atendimento',
                                  inverse_name='contrato',
                                  string='Atendimentos',
                                  help='Atendimentos vinculados ao contrato')
    
    protocolo = fields.One2many(
                                comodel_name='protocolo',
                                inverse_name='contrato',
                                string='Protocolos',
                                help='Protocolos vinculados ao contrato')
                                
    ocorrencia = fields.One2many(
                                 comodel_name='ocorrencia',
                                 inverse_name='contrato',
                                 string='Ocorrencias',
                                 help='Ocorrencias vinculados ao contrato')
    
    contrato_pdf = fields.Binary(
                                 string='Contrato Assinado',
                                 help='Contrato assinado pelo cliente.')
    
    contrato_pdf_filename = fields.Char("Contrato Assinado", 
                                        track_visibility='onchange')
    
    id_syncron = fields.Integer(
                                string='ID no Syncron',
                                help='ID de identificação no Syncron')
    
    date_start = fields.Date(
                             track_visibility='onchange'
                             )
    
    recurring_invoices = fields.Boolean(
                                        track_visibility='onchange'
                                        )
    
    recurring_interval = fields.Integer(
                                        track_visibility='onchange'
                                        )
    
    recurring_next_date = fields.Date(
                                      track_visibility='onchange'
                                      )
    
    recurring_rule_type = fields.Selection(
                                           track_visibility='onchange'
                                           )
    
    host = fields.One2many(
                           comodel_name='host',
                           inverse_name='contrato',
                           string='Hosts',
                           help='Hosts vinculados ao contrato')
        
    sla = fields.Selection(
                           selection=[(2, 'Não'),
                           (1, 'Sim')],
                           string='SLA',
                           help='Cliente possui SLA?',
                           required=True,
                           track_visibility='onchange')
    
    '''
    def ativar_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 13}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def inativar_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 12}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def suspender_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 14}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def cancelar_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 15}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def free_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 16}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def nunca_bloquear_contrato(self, cr, user, ids, context=None):
        contrato = self.pool.get('account.analytic.account').browse(cr, user, ids[0])
        contrato.write({'status_contrato': 17}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    '''
    def abrir_varias_ocorrencias(self, cr, user, ids, context=None):
        
        return {
            'name':'lote_ocorrencias.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'lote_ocorrencias',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_contrato': ids[0]
            }
        }
        
    def reabrir_varias_ocorrencias(self, cr, user, ids, context=None):
        return {
            'name':'lote_abre_fecha_ocorrencias.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'lote_abre_fecha_ocorrencias',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_contrato': ids[0],
                'default_name': '1',
                'default_operacao': '1'
            }
        }
        
    def fechar_varias_ocorrencias(self, cr, user, ids, context=None):
        
        return {
            'name':'lote_abre_fecha_ocorrencias.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'lote_abre_fecha_ocorrencias',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_contrato': ids[0],
                'default_name': '2',
                'default_operacao': '2'
            }
        }
        
    def obs_varias_ocorrencias(self, cr, user, ids, context=None):
        
        return {
            'name':'lote_abre_fecha_ocorrencias.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'lote_abre_fecha_ocorrencias',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_contrato': ids[0],
                'default_name': '3',
                'default_operacao': '2'
            }
        }

    def gerar_protocolo(self, cr, user, ids, context=None):
        valores = {
            'contrato': ids[0]
        }
        protocolo = self.pool.get('protocolo').create(cr, user, valores, context)
        pass
