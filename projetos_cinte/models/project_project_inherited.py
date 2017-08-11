# -*- coding: utf-8 -*-
from openerp import models, fields

class Project_task_inherited(models.Model):
    _inherit = 'project.project' 
    
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
              setar_proxima_tarefa(param1, param2)
        
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
        