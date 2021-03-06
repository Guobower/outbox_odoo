# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Atendimento(models.Model):
    _name = 'atendimento'
    _description = 'Atendimento'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        access_rights_uid = access_rights_uid or uid
        stage_obj = self.pool.get('status_atendimento')
        order = stage_obj._order
        
        # perform search
        stage_ids = stage_obj._search(cr, uid, "", order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        return result, None
    
    _group_by_full = {
        'status_atendimento': _read_group_stage_ids,
    }
    
    name = fields.Many2one(
        comodel_name='protocolo',
        string='Protocolo',
        help='Protocolo ao qual está vinculado o atendimento',
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição do status de adesão",
        track_visibility="onchange")
    
    manifestacao_atendimento = fields.Many2one(
        comodel_name='manifestacao_atendimento',
        string='Manifestacao',
        help='Manifestação do atendimento',
        track_visibility='onchange',
        required=True)
    
    grupo_atendimento = fields.Many2one(
        comodel_name='grupo_atendimento',
        string='Grupo',
        help='Grupo do atendimento',
        track_visibility='onchange',
        required=True)
    
    protocolo = fields.Many2one(
        comodel_name='protocolo',
        string='Protocolo',
        help='Protocolo ao qual está vinculado o atendimento',
        track_visibility='onchange',
        required=True)
    
    contrato = fields.Many2one(
        string="Contrato",
        comodel_name='account.analytic.account',
        help="Contrato ao qual o atendimento está vinculado",
        track_visibility='onchange',
        required=True)
    
    adesao = fields.Many2one(
        string="Adesao",
        comodel_name='adesao',
        help="Adesão a qual o atendimento está vinculado",
        track_visibility='onchange')
    
    
    tipo_atendimento = fields.Many2one(
        comodel_name='tipo_atendimento',
        string='Tipo',
        help='Status do contrato',
        track_visibility='onchange',
        required=True)
    
    procedimento = fields.Text('Procedimento', related='tipo_atendimento.procedimento', store=True)
    
    orientacao = fields.Text('Orientacao', related='tipo_atendimento.orientacao', store=True)
    
    tempo_resolucao = fields.Integer('Prazo (dias)', related='tipo_atendimento.tempo_resolucao', store=True)
    
    manual = fields.Binary('Manual', related='tipo_atendimento.manual', store=True)
    
    manual_filename = fields.Char('Arquivo do Manual', related='tipo_atendimento.manual_filename', store=True)
    
    previsao_resolucao = fields.Date(
        string="Previsao de Resolucao",
        help="Data prevista para a resolução do problema de acordo com o tipo de atendimento")
    
    reclamacao = fields.Text(
        string="Reclamacao",
        help="Descrição da reclamação do cliente",
        required=True)
    
    documentacao = fields.Selection(
        selection=[('0', 'Aguardando cliente enviar'),
                   ('1', 'Recebido do cliente')],
        string="Documentacao",
        help="A documentação necessária para o atendimento ao cliente foi entregue ou há alguma pendência por parte do cliente?",
        required=True)
    
    solicitacao_atendida = fields.Selection(
        selection=[('0', 'Não'),
                   ('1', 'Sim')],
        string="Solicitacao Atendida",
        help="A solicitação/reclamação do cliente foi atendida pela Cinte?",
        required=True)
    
    previsao_resolucao = fields.Date(
        string="Previsao de Resolucao",
        help="Data prevista para resolução de acordo com o tipo de atendimento")
    
    data_conclusao = fields.Date(
        string="Data de Conclusao",
        help="Data de conclusão do atendimento")
    
    status_atendimento = fields.Many2one(
        comodel_name='status_atendimento',
        string='Status',
        help='Andamento da solicitação do cliente',
        track_visibility='onchange',
        required=True)

    area_resolvedora = fields.Many2one(
        comodel_name='area_resolvedora',
        string='Área Resolvedora',
        help='Área atualmente responsável pela resolução da demanda',
        track_visibility='onchange',
        required=True)
    
    modo_contato = fields.Many2one(
        comodel_name='modo_contato',
        string='Modo de Contato',
        help='Modo de contato do cliente com a Cinte na abertura do chamado',
        track_visibility='onchange',
        required=True)
    
    color = fields.Integer(
        string="Color Index")

    def on_change_manifestacao_atendimento(self, cr, user, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo zerar os subcampos da configuracao de atendimento ao trocar a manifestacao.

            Utilização:
              on_change_manifestacao_atendimento()

            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              context
                Contexto atual
        '''
        res = {
            'value': {
                'grupo_atendimento': '',
                'tipo_atendimento': ''
            }
        }
        return res

    def on_change_grupo_atendimento(self, cr, user, ids, context=None):
        '''
            Descrição:
              Esta função tem como objetivo zerar os subcampos da configuracao de atendimento ao trocar o grupo.

            Utilização:
              on_change_grupo_atendimento()

            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              context
                Contexto atual
        '''
        res = {
            'value': {
                'tipo_atendimento': ''
            }
        }
        return res
    
    def on_change_documentacao(self, cr, user, ids, tipo_atendimento, documentacao, context=None):
        '''
            Descrição:
              Esta função tem como objetivo preencher automaticamente os dados de
              previsão de atendimento de acordo com o tipo do atendimento, adicionando
              na data atual a quantidade de dias necessárias configurada no tipo do atendimento.
        
            Utilização:
              on_change_tipo_atendimento(param1)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              tipo_atendimento
                Tipo do atendimento escolhido
              context
                Contexto atual
        '''
        from datetime import *
        import datetime
        
        obj_tipo_atendimento = self.pool.get('tipo_atendimento').browse(cr, user, tipo_atendimento)

        if documentacao == '1':
            data_prevista = datetime.date.today() + timedelta(days=obj_tipo_atendimento.tempo_resolucao)

            res = {
                     'value': {
                        # Define os valores dos campos e atualiza no formulário
                        'previsao_resolucao':  data_prevista
                    }
                }
        else:
            res = {
                'value': {
                    # Define os valores dos campos e atualiza no formulário
                    'previsao_resolucao': ''
                }
            }
        # Retorna os valores para serem atualizados na view.
        return res
