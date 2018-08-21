# -*- coding: utf-8 -*-
"""
Módulo de Tarefas Recorrentes para as Tarefas padrões do módulo de Projetos.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2018, Edson Junior"
__credits__ = ["Outbox Sistemas"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"

from odoo import models, fields, api


class RecurringTask(models.Model):
    """
        Classe Recurring Tasks define os atributos e métodos necessários para a geração de tarefas recorrentes no módulo de projetos.

        Define os dados da tarefa a ser replicada, sua frequência e os métodos necessários para a geração das atividades.
    """
    _name = 'recurring_task'
    _inherit = ['mail.thread']

    _defaults = {
        'active': True
    }

    name = fields.Char(
        string="Nome",
        size=150,
        required=True,
        track_visibility="onchange")

    project_id = fields.Many2one(
        string="Projeto",
        comodel_name="project.project",
        required=True,
        track_visibility="onchange"
    )

    active = fields.Boolean(
        string="Ativo",
        track_visibility="onchange"
    )

    user_id = fields.Many2one(
        string="Atribuido a",
        comodel_name="res.users",
        required=True,
        track_visibility="onchange"
    )

    description = fields.Text(
        string="Descrição",
        track_visibility="onchange"
    )

    '''
    def on_change_cidade(self, cr, user, ids, cidade_origem, cidade_destino, context=None):
        """
        Função onchange para as cidades no formulário.
        Recebe a cidade de origem e destino adicionadas ao formulário, caso ambas estejam preenchidas utiliza a API do
        Google Maps para buscar a distância e o tempo de percurso entre as cidades e atualiza no formulário os dados
        calculados na consulta.
        :param cr: Cursor da base de dados.
        :param user: Usuário logado.
        :param ids: IDs das instâncias da classe.
        :param cidade_origem: Cidade de origem definida no formulário.
        :param cidade_destino: Cidade de destino definida no formulário.
        :param context: Contexto da aplicação. Default None
        :return: Retorna o par distância/tempo de viagem e atualiza os campos do formulário
        """
        if cidade_origem and cidade_destino:
            origem = self.pool.get('l10n_br_base.city').browse(cr, user, cidade_origem)
            destino = self.pool.get('l10n_br_base.city').browse(cr, user, cidade_destino)

            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origem.name + "," + origem.state_id.name + "&destinations=" + destino.name + "," + destino.state_id.name + "&key=AIzaSyDYRUAfCeT3uwCqZzvVoGv1QqRIAL0h5dk"
            url = url.encode('utf-8')
            result = simplejson.load(urllib.urlopen(url))

            distancia = (result['rows'][0]['elements'][0]['distance']['value']) / 1000
            tempo_viagem = (result['rows'][0]['elements'][0]['duration']['value']) / 60

            res = {
                'value': {
                    'distancia': distancia,
                    'tempo_viagem': tempo_viagem
                }
            }
            return res
    '''