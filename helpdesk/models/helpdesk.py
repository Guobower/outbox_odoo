# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

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
    
    _defaults = {
        'stage_id': 1
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
    
    horas_programadas = fields.Float(
                                     string="Horas Programadas",
                                     help='Horas programadas para o atendimento, definidas em sessões de Planning Poker',
                                     track_visibility='onchange')
        
    horas_ideais = fields.Float(
                                string="Horas Ideais",
                                help='Horas ideais para o atendimento da atividade, definidas em sessões de Planning Poker',
                                track_visibility='onchange')
        
    horas_gastas = fields.Float(
                                string="Horas Gastas",
                                help='Horas gastas na resolução da atividade',
                                track_visibility='onchange')
        
    data_base_inicio = fields.Datetime(
                                       string='Data de Inicio',
                                       help='Data de início do atendimento do suporte',
                                       track_visibility='onchange')
        
    data_base_pausa = fields.Datetime(
                                      string='Data de Pausa',
                                      help='Data de pausa do atendimento do suporte',
                                      track_visibility='onchange')
    
    status_andamento = fields.Selection(
                                        selection=[('1', 'Em curso'),
                                        ('2', 'Pausado')],
                                        string='Status do Andamento',
                                        track_visibility='onchange')
                                        
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
            
    
    def reiniciar_helpdesk(self, cr, uid, ids, context=None):
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
        import datetime
        
        helpdesk_obj = self.pool.get('helpdesk').browse(cr, uid, ids[0])
        
        helpdesk_responsavel = self.pool.get('helpdesk').search(cr, uid, [('responsavel', '=', helpdesk_obj.responsavel.id),('status_andamento', '=', '1')])  
        
        if helpdesk_responsavel:
            helpdesk_aberto = self.pool.get('helpdesk').browse(cr, uid, helpdesk_responsavel[0])
            return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': helpdesk_aberto.responsavel.name + ' esta ocupado(a)!',
                'text': 'A tarefa "'+helpdesk_aberto.name+'" esta em andamento, feche-a antes de iniciar esta atividade',
                'sticky': True
                }
            }
        else:
            helpdesk_obj.write({'data_base_inicio': datetime.datetime.today(), 'status_andamento': '1', 'data_base_pausa': False}, context=None)     
            pass
        
    def pausar_helpdesk(self, cr, uid, ids, context=None):
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
        import datetime
        
        helpdesk_obj = self.pool.get('helpdesk').browse(cr, uid, ids[0])
        
        tempo_andamento = (datetime.datetime.today() - datetime.datetime.strptime(helpdesk_obj.data_base_inicio, '%Y-%m-%d %H:%M:%S')).total_seconds()
        tempo_total = helpdesk_obj.horas_gastas + (tempo_andamento / 3600)
        helpdesk_obj.write({'status_andamento': '2', 'data_base_pausa':datetime.datetime.today(), 'horas_gastas':tempo_total}, context=None) 
        
        pass
    
    def pausar_todos_helpdesk(self, cr, uid, context=None):
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
        import datetime
        
        helpdesk_obj = self.pool.get('helpdesk').search(cr, uid, [('status_andamento', '=', '1')])   
        
        for item in helpdesk_obj:
            helpdesk = self.pool.get('helpdesk').browse(cr, uid, item)
            tempo_andamento = (datetime.datetime.today() - datetime.datetime.strptime(helpdesk.data_base_inicio, '%Y-%m-%d %H:%M:%S')).total_seconds()
            tempo_total = helpdesk.horas_gastas + (tempo_andamento / 3600)
            helpdesk.write({'status_andamento': '2', 'data_base_pausa':datetime.datetime.today(), 'horas_gastas':tempo_total}, context=None) 
        
        pass
    
    def verificar_atrasos_helpdesk(self, cr, uid, context=None):
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
        import datetime
        helpdesk_obj = self.pool.get('helpdesk').search(cr, uid, [('status_andamento', '=', '1')])   
        for item in helpdesk_obj:
            helpdesk = self.pool.get('helpdesk').browse(cr, uid, item)
            tempo_andamento = (datetime.datetime.today() - datetime.datetime.strptime(helpdesk.data_base_inicio, '%Y-%m-%d %H:%M:%S')).total_seconds()
            tempo_total = helpdesk.horas_gastas + (tempo_andamento / 3600)
            
            
            if helpdesk.horas_programadas:
                if tempo_total / helpdesk.horas_programadas > 0.9 and tempo_total / helpdesk.horas_programadas < 1:
                    helpdesk.write({'color': 3}, context=None) 
                if tempo_total / helpdesk.horas_programadas > 1:
                    helpdesk.write({'color': 2}, context=None) 
                if tempo_total / helpdesk.horas_programadas < 0.9:
                    helpdesk.write({'color': 0}, context=None) 
        
        helpdesk_obj2 = self.pool.get('helpdesk').search(cr, uid, [('stage_id', '=', 5), ('color', '!=', 1)])  
        for item in helpdesk_obj2:
            helpdesk = self.pool.get('helpdesk').browse(cr, uid, item)
            helpdesk.write({'color': 1}, context=None) 
            
        helpdesk_obj3 = self.pool.get('helpdesk').search(cr, uid, [('stage_id', '=', 4), ('color', 'not in', (5, 9))])  
        for item in helpdesk_obj3:
            helpdesk = self.pool.get('helpdesk').browse(cr, uid, item)
            
            if helpdesk.horas_programadas < helpdesk.horas_gastas:
                helpdesk.write({'color': 9}, context=None) 
            else:
                helpdesk.write({'color': 5}, context=None)     
        pass
    
    
