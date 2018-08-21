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

    stage_id = fields.Many2one(
        string="Estágio",
        comodel_name="project.task.type",
        track_visibility="onchange"
    )

    frequencia = fields.Integer(
        string="Repetir a cada",
        required=True,
        track_visibility="onchange"
    )

    recorrencia = fields.Selection(
        string="Recorrência",
        selection=[
            ('dia','Dia(s)'),
            ('semana','Semana(s)'),
            ('mes','Mês(es)'),
            ('ano','Ano(s)')
        ],
        required=True,
        track_visibility="onchange"
    )

    proxima_data = fields.Date(
        string="Data da próxima tarefa",
        required=True,
        track_visibility="onchange"
    )

    active = fields.Boolean(
        string="Ativo",
        default=True,
        track_visibility="onchange"
    )

    user_id = fields.Many2one(
        string="Atribuido a",
        comodel_name="res.users",
        required=True,
        track_visibility="onchange"
    )

    description = fields.Html(
        string="Descrição",
        track_visibility="onchange"
    )

    @api.multi
    def executar_cron(self, context=None):
        """
        Função para gerar tarefas agendadas.
        Função a ser executada diariamente com o intuido de verificar quais tarefas recorrentes devem ser geradas na data
        atual e realizar a criação, após isso também seta a data da próxima geração de acordo com a frequência definida.
        :param context: Contexto da aplicação. Default None
        :return: Null
        """
        import datetime
        hoje = datetime.datetime.now().strftime("%Y-%m-%d")
        recurring_tasks_obj = self.env['recurring_task'].search([('proxima_data', '<=', hoje)])

        for recurring_task in recurring_tasks_obj:
            valores = {
                'name': recurring_task["name"],
                'project_id': recurring_task["project_id"].id,
                'stage_id': recurring_task["stage_id"].id,
                'user_id': recurring_task["user_id"].id,
                'description': recurring_task["description"]
            }
            recurring_task.recalcular_proxima_data()
            self.env['project.task'].create(valores)

    def recalcular_proxima_data(self):
        """
        Função para recalcular a data da próxima tarefa agendada.
        Função responsável por recalcular a data da geração da próxima atividade de acordo com a definição de frequência
        e recorrência.
        :param context: Contexto da aplicação. Default None
        :return: Null
        """
        from datetime import timedelta, datetime
        from dateutil.relativedelta import relativedelta

        if self.recorrencia == "dia":
            self.proxima_data = (datetime.strptime(self.proxima_data, '%Y-%m-%d') + timedelta(days=self.frequencia)).strftime("%Y-%m-%d")
        elif self.recorrencia == "semana":
            self.proxima_data = (datetime.strptime(self.proxima_data, '%Y-%m-%d') + timedelta(weeks=self.frequencia)).strftime("%Y-%m-%d")
        elif self.recorrencia == "mes":
            self.proxima_data = (datetime.strptime(self.proxima_data, '%Y-%m-%d') + relativedelta(months=self.frequencia)).strftime("%Y-%m-%d")
        elif self.recorrencia == "ano":
            self.proxima_data = (datetime.strptime(self.proxima_data, '%Y-%m-%d') + relativedelta(years=self.frequencia)).strftime("%Y-%m-%d")