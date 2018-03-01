# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Monitoramento(models.Model):
    _name = 'monitoramento'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        access_rights_uid = access_rights_uid or uid
        stage_obj = self.pool.get('estagios_monitoramento')
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
    
    _defaults = {
        'stage_id': 1
    }
    
    
    name = fields.Char(
                       string="Name",
                       size=250,
                       required=True,
                       track_visibility='onchange')
    
    sistema = fields.Many2one(
                              comodel_name='sistemas_monitoramento',
                              string='Tipo',
                              help='Sistema monitorado',
                              required=True,
                              track_visibility='onchange')
                              
    causa_tecnica = fields.Many2one(
                              comodel_name='causa_tecnica',
                              string='Causa Tecnica',
                              help='Causa técnica que originou o problema',
                              track_visibility='onchange')
    
    descricao = fields.Text(
                            string="Descricao",
                            help="Descreva o problema",
                            required=True,
                            track_visibility='onchange')
    
    stage_id = fields.Many2one(
                               comodel_name='estagios_monitoramento',
                               string='Status',
                               help='Status do suporte',
                               required=True,
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
                                  required=True,
                                  track_visibility='onchange')
    
    data_previsao = fields.Datetime(
                                    string='Previsao de Conclusao',
                                    help='Data prevista para a conclusão do suporte',
                                    track_visibility='onchange')
    
    data_conclusao = fields.Datetime(
                                     string='Conclusao',
                                     help='Data de conclusão do suporte',
                                     track_visibility='onchange')
        
    data_contornado = fields.Datetime(
                                      string='Contornado em',
                                      help='Data em que o problema foi contornado paliativamente',
                                      track_visibility='onchange')
    
    responsavel = fields.Many2one(
                                  comodel_name='res.users',
                                  string='Responsavel',
                                  help='Responsável pela resolução do problema',
                                  track_visibility='onchange')
    
    exibir_site = fields.Selection(
                                   selection=[('0', 'Não'),
                                   ('1', 'Sim')],
                                   string='Exibir no Site',
                                   help='Exibir o monitoramento no site?',
                                   required=True,
                                   track_visibility='onchange')
    
    atrasado = fields.Selection(
                                selection=[('0', 'Não'),
                                ('1', 'Sim')],
                                string='Atrasado',
                                help='Previsão de resolução foi ultrapassada?',
                                track_visibility='onchange')
    
    pop = fields.Many2many(
                             comodel_name='pop',
                             string='Pop',
                             help='Pops atingidos pelo problema',
                             track_visibility='onchange')
    
    
    def verificar_atrasos(self, cr, uid, context=None):
        '''
            Descrição:
              Esta função tem como objetivo monitorar os prazos repassados no ticket e caso 
              ultrapasse o prazo marcar o mesmo como atrasado.
        
            Utilização:
              verificar_atrasos()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              context
                Contexto atual
        '''
        from datetime import datetime
        
        monitoramento_obj = self.pool.get('monitoramento')
        monitoramento_ids = self.pool.get('monitoramento').search(cr, uid, [])   
        
        for monitoramento_id in monitoramento_ids:
            monitoramento_line = monitoramento_obj.browse(cr, uid, monitoramento_id, context=context)
            previsao = datetime.strptime(monitoramento_line.data_previsao, '%Y-%m-%d %H:%M:%S')

            if previsao < datetime.today():
                if monitoramento_line.stage_id.id != 5:
                    monitoramento_line.write({'atrasado': '1', 'color': 2}, context=context)
        return True
    
    
    def marcar_em_tratamento(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo setar ticket como em tratamento.
        
            Utilização:
              marcar_em_tratamento()
        
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
        
        monitoramento_obj = self.pool.get('monitoramento')
        monitoramento_obj.write(cr, uid, ids[0], {'stage_id': 2}, context=context)     
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def marcar_em_testes(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo setar ticket como em testes.
        
            Utilização:
              marcar_em_testes()
        
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
        
        monitoramento_obj = self.pool.get('monitoramento')
        monitoramento_obj.write(cr, uid, ids[0], {'stage_id': 3}, context=context)     
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
    def marcar_contornado(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo setar ticket como contornado.
        
            Utilização:
              marcar_contornado()
        
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
        from datetime import datetime
        if not context:
            context = {}
        
        monitoramento_obj = self.pool.get('monitoramento')
        monitoramento_obj.write(cr, uid, ids[0], {'stage_id': 4, 'data_contornado': datetime.today()}, context=context)     
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
        
    def marcar_concluido(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo setar ticket como concluido.
        
            Utilização:
              marcar_concluido()
        
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
        from datetime import datetime
        if not context:
            context = {}
        
        monitoramento_obj = self.pool.get('monitoramento')
        monitoramento_obj.write(cr, uid, ids[0], {'stage_id': 5, 'data_conclusao': datetime.today()}, context=context)     
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
            
            
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
        
        monitoramento_obj = self.pool.get('monitoramento')
        monitoramento_obj.write(cr, uid, ids[0], {'responsavel': uid}, context=context)     
        
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
    
    
