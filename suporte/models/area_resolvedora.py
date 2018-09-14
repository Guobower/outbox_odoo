# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Area_resolvedora(models.Model):
    _name = 'area_resolvedora'
    _description = 'Area resolvedora'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    _defaults = {
        'active': True
    }

    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')

    descricao = fields.Text(
        string="Descricao",
        help="Descrição",
        track_visibility="onchange")

    active = fields.Boolean(
        string="Ativo",
        track_visibility='onchange'
    )