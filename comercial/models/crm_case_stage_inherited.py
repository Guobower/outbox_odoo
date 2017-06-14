# -*- coding: utf-8 -*-
from openerp import models, fields

class Crm_case_stage_inherited(models.Model):
    _inherit = 'crm.case.stage' 

    type = fields.Selection(
        selection=[('lead', 'Lead'),
                   ('opportunity','Opportunity'),
                   ('licitados','Licitados'),
                   ('both','Todos')],
        string='Type',
        select =True,
        help='Usados para separar prospectos, oportunidades e licitados')