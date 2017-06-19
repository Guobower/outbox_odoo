# -*- coding: utf-8 -*-
from openerp import models, fields

class Crm_lead_inherited(models.Model):
    _inherit = 'crm.lead' 

    type = fields.Selection(
        selection=[('lead', 'Lead'),
                   ('opportunity','Opportunity'),
                   ('licitados','Licitados')],
        string='Type',
        select =True,
        help='Usados para separar prospectos, oportunidades e licitados')
    
    