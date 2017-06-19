# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Atividades_cinte(models.Model):
    def _read_group_stage_ids(self, cr, uid, ids, domain, read_group_order=None, access_rights_uid=None, context=None):
        access_rights_uid = access_rights_uid or uid
        stage_obj = self.pool.get('estagios_atividades_cinte')
        order = stage_obj._order
        
        # perform search
        stage_ids = stage_obj._search(cr, uid, "", order=order, access_rights_uid=access_rights_uid, context=context)
        result = stage_obj.name_get(cr, access_rights_uid, stage_ids, context=context)
        # restore order of the search
        result.sort(lambda x, y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))

        return result, None
    
    _name = 'atividades_cinte'
    _group_by_full = {
        'stage_id': _read_group_stage_ids,
    }
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)
    
    stage_id = fields.Many2one(
        comodel_name='estagios_atividades_cinte',
        string='Estágio',
        help='Estágio da atividade')
    
    color = fields.Integer(
        string="Color Index")
    
    atividade = fields.Text(
        string='Atividade/Pendência',
        help='Atividade/Pendência a ser desenvolvida')
    
    prioridade = fields.Selection(
        selection=[('0', 'Nenhuma'),
                   ('1', 'Muito Baixa'),
                   ('2', 'Baixa'),
                   ('3', 'Media'),
                   ('4', 'Alta'),
                   ('5', 'Muito Alta')],
        string='Prioridade',
        help='Prioridade da atividade')
    
    observacoes = fields.Text(
        string='Observacões',
        help='Observacões sobre a atividade')

    dataPrevisao = fields.Date(
        string='Previsão de Conclusão',
        help='Data prevista para a conclusão da atividades')
    
    dataConclusao = fields.Date(
        string='Conclusão',
        help='Data de conclusão da atividade')
    
    observacoesGestao = fields.Text(
        string='Observacões do Gestor/Avaliador',
        help='Observacões do gestor/avaliador')
    
    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável pela atividade')
    
    equipe = fields.Many2many(
        comodel_name='res.users',
        string='Equipe',
        help='Equipe envolvida na atividade')