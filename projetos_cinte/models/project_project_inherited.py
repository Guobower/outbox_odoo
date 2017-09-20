# -*- coding: utf-8 -*-
from openerp import models, fields

class Project_task_inherited(models.Model):
    _inherit = 'project.project' 
    
    type_project = fields.Selection(
        selection=[('corporativos', 'Corporativos'),
                   ('licitados', 'Licitados'),
                   ('internos', 'Internos')],
        string='Type',
        select=True,
        help='Usados para separar projetos coporativos, licitados e internos')
    
    pontos_clientes = fields.One2many(
        comodel_name='ponto.cliente_licitado',
        inverse_name='project_id',
        string='Pontos do Cliente',
        help='Pontos do Cliente')
    
    pontos_internos = fields.One2many(
        comodel_name='ponto.interno',
        inverse_name='project_id',
        string='Pontos Internos',
        help='Pontos Internos')
    
    invoice_line = fields.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    
    proxima_tarefa = fields.Many2one(
        comodel_name='project.task',
        string='Próxima Tarefa',
        help='Próxima tarefa a ser realizada no projeto')
    
    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável pela atividade')
    
    def setar_proxima_tarefa(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo setar no cadastro
              do projeto a próxima tarefa a ser executada e 
              exibida na visualização Kanban dos projetos.
        
            Utilização:
              setar_proxima_tarefa()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs dos projetos em questão
              context
                Contexto atual
        '''
        if context is None:
            context = {}
            
        model_obj = self.pool.get('project.project')
        projeto = model_obj.browse(cr, uid, ids[0].project_id.id)
        
        atividade = 0
        responsavel = 0
        for atividades in ids[0].project_id.tasks:
            if atividades.stage_id.id != 7:
                atividade = atividades.id
                responsavel = atividades.user_id.id
                break
        
        return projeto.write({'proxima_tarefa':atividade,'responsavel':responsavel})
    
    
    def gerar_oportunidade(self, cr, uid, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo gerar uma oportunidade no CRM
              ao criar um projeto.
        
            Utilização:
              gerar_oportunidade()
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs dos projetos em questão
              context
                Contexto atual
        '''
        if context is None:
            context = {}
            
        lead_obj = self.pool.get('crm.lead')
        
        lead_obj.create(cr, uid, {'name': 'Teste', 'trunk':'Teste', 'callerid':'Teste', 'id_queue_call_entry': 1}, context=context)     
       
        
        