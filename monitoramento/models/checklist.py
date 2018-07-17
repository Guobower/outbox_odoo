# -*- coding: utf-8 -*-
"""
Módulo de checklist para troca de informações na mudança de turno no suporte da Cinte.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2017, Edson Junior"
__credits__ = ["equipe de desenvolvimento Cinte"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"

from openerp import fields
from openerp import models
from datetime import datetime


class Checklist(models.Model):
    """
    Classe Checklist define os atributos e métodos necessários para o registro do checklist de mudança de turno no suporte.

    Define o formulário de checklist a ser preenchido pelo atendente do suporte durante a mudança de turno, onde deverá
    ser informado o status do serviço nos clientes chaves e na infraestrutura da empresa.
    """

    _name = 'checklist'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Datetime(
        string="Retorno",
        required=True,
        track_visibility='onchange')

    item_cliente = fields.One2many(
        comodel_name="checklist_item_cliente",
        inverse_name='checklist',
        string="Incidentes Clientes",
        help="Todos os registros de ocorrências com clientes chaves",
        track_visibility="onchange"
    )

    item_backbone = fields.One2many(
        comodel_name="checklist_item_backbone",
        inverse_name='checklist',
        string="Incidentes Backbone",
        help="Todos os registros de ocorrências com a infraestrutura",
        track_visibility="onchange"
    )


class Checklist_item_cliente(models.Model):
    """
    Classe item do checklist para definição de problemas relativos a clientes.
    """

    _name = 'checklist_item_cliente'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Selection(
        selection=[('caern', 'Caern'),
                   ('crea', 'CREA-RN'),
                   ('dprf', 'DPRF'),
                   ('sesi', 'SESI (FIERN)'),
                   ('ifrn', 'IFRN'),
                   ('jfrn', 'JFRN'),
                   ('mprn', 'MPRN'),
                   ('pmja', 'PMJA'),
                   ('pml', 'PML'),
                   ('pmm', 'PMM'),
                   ('pmsn', 'PMSN'),
                   ('sebrae', 'SEBRAE'),
                   ('sesc', 'SESC'),
                   ('tjrn', 'TJRN'),
                   ('tre', 'TRE'),
                   ('tce', 'TCE'),
                   ('uern', 'UERN'),
                   ('ufrn', 'UFRN'),
                   ('ebserh', 'EBSERH')],
        string='Cliente',
        required=True,
        track_visibility='onchange')

    status = fields.Selection(
        selection=[('1', 'Ocorrências registradas corretamente'),
                   ('2', 'Havia ocorrência não registrada. Retificado'),
                   ('3', 'Havia ocorrência em aberto. Retificado'),
                   ('4', 'Inoperância de Rádio "A" não reportada. Retificado'),
                   ('5', 'Inoperância de Conversor de mídia não reportada. Retificado'),
                   ('6', 'Outro')],
        string='Status',
        required=True,
        track_visibility='onchange')

    observacoes = fields.Text(
        string="Observações",
        track_visibility='onchange'
    )

    verificado = fields.Selection(
        selection=[('1', 'Não'),
                   ('2', 'Sim')],
        string="Verificado"
    )

    checklist = fields.Many2one(
        string="Checklist",
        comodel_name='checklist')


class Checklist_item_backbone(models.Model):
    """
    Classe item do checklist para definição de problemas relativos a infraestrutura própria.
    """

    _name = 'checklist_item_backbone'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Selection(
        selection=[('1', 'Falha Repetidora'),
                   ('2', 'UPS Modo Bateria'),
                   ('3', 'Operadoras'),
                   ('4', 'Mikrotiks/OLTs'),
                   ('5', 'Elastix'),
                   ('6', 'Switchs')],
        string="Backbone",
        required=True,
        track_visibility='onchange'
    )

    status = fields.Many2one(
        comodel_name="status_checklist_item_backbone",
        string='Status',
        required=True,
        track_visibility='onchange')

    observacoes = fields.Text(
        string="Observações",
        track_visibility='onchange'
    )

    verificado = fields.Selection(
        selection=[('1', 'Não'),
                   ('2', 'Sim')],
        string="Verificado"
    )

    checklist = fields.Many2one(
        string="Checklist",
        comodel_name='checklist')

    def on_change_name(self, cr, user, ids, name, context=None):
        """
        Função onchange para os itens do checklist do backbone.

        Recebe qual item foi selecionado e devolve os status possíveis de utilização para este item.

        :param cr: Cursor da base de dados.
        :param user: Usuário logado.
        :param ids: IDs das instâncias da classe.
        :param name: Item selecionado no formulário.
        :param context: Contexto da aplicação. Default None
        :return: Retorna o domínio de status possíveis para o item selecionado
        """

        if name == "1":
            return {'domain': {'status': [('id', 'in', (1, 2, 3, 4, 5, 6))]}}
        elif name == "2":
            return {'domain': {'status': [('id', 'in', (7, 8, 9, 10))]}}
        elif name == "3":
            return {'domain': {'status': [('id', 'in', (11, 12, 13, 14, 15, 16))]}}
        elif name == "4":
            return {'domain': {'status': [('id', 'in', (17, 18, 19))]}}
        elif name == "5":
            return {'domain': {'status': [('id', 'in', (20, 21, 22))]}}
        elif name == "6":
            return {'domain': {'status': [('id', 'in', (23, 24, 25))]}}


class Status_checklist_item_backbone(models.Model):
    """
    Classe status dos itens do checklist de backbone.
    """

    _name = 'status_checklist_item_backbone'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(
        string="Status",
        size=150,
        required=True
    )

