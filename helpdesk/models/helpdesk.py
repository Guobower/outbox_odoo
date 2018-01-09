# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Helpdesk(models.Model):
    _name = 'helpdesk'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        access_rights_uid = access_rights_uid or uid
        stage_obj = self.pool.get('estagios_helpdesk')
        order = stage_obj._order
        
        # perform search
        stage_ids = stage_obj._search(cr, uid, "", order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        return result, None
    
    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }
    
    _defaults={
        'stage_id' : 1
    }
    
    _track = {
            'helpdesk': {
                'helpdesk.mt_name': lambda self, cr, uid, obj, ctx = None: obj.name,
                'helpdesk.mt_sistema': lambda self, cr, uid, obj, ctx = None: obj.sistema,
                'helpdesk.mt_descricao': lambda self, cr, uid, obj, ctx = None: obj.descricao,
                'helpdesk.mt_stage_id': lambda self, cr, uid, obj, ctx = None: obj.stage_id,
                'helpdesk.mt_prioridade': lambda self, cr, uid, obj, ctx = None: obj.prioridade,
                'helpdesk.mt_data_previsao': lambda self, cr, uid, obj, ctx = None: obj.data_previsao,
                'helpdesk.mt_data_conclusao': lambda self, cr, uid, obj, ctx = None: obj.data_conclusao,
                'helpdesk.mt_responsavel': lambda self, cr, uid, obj, ctx = None: obj.responsavel
            }
    }
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True,
        track_visibility='onchange')
    
    sistema = fields.Many2one(
        comodel_name='sistemas_helpdesk',
        string='Sistema',
        help='Sistema para o suporte',
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descreva o suporte desejado",
        track_visibility='onchange')
    
    stage_id = fields.Many2one(
        comodel_name='estagios_helpdesk',
        string='Status',
        help='Status do suporte',
        track_visibility='onchange')
    
    color = fields.Integer(
        string="Color Index")
    
    prioridade = fields.Selection(
        selection=[('0', 'Nenhuma'),
                   ('1', 'Muito Baixa'),
                   ('2', 'Baixa'),
                   ('3', 'Media'),
                   ('4', 'Alta'),
                   ('5', 'Muito Alta')],
        string='Prioridade',
        help='Prioridade do suporte',
        track_visibility='onchange')
    
    data_previsao = fields.Date(
        string='Previsao de Conclusao',
        help='Data prevista para a conclusão do suporte',
        track_visibility='onchange')
    
    data_conclusao = fields.Date(
        string='Conclusao',
        help='Data de conclusão do suporte',
        track_visibility='onchange')
    
    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsavel',
        help='Responsável pelo suporte',
        track_visibility='onchange')
    
    equipe = fields.Many2many(
        comodel_name='res.users',
        string='Equipe',
        help='Equipe envolvida na atividade')
    
    
    def pegar_ticket(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo setar o usuario logado como responsavel pelo ticket.
        
            Utilização:
              pegar_ticket()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs do ticket em questão
              context
                Contexto atual
        '''
        if not context:
            context = {}
        
        helpdesk_obj = self.pool.get('helpdesk')
        helpdesk_obj.write(cr, uid, ids[0], {'responsavel': uid}, context=context)     
        
        return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Operação concluída com sucesso!',
                    'text': 'Você foi selecionado como responsável pelo atendimento deste ticket.',
                    'sticky': False
                    }
            }
    
    
