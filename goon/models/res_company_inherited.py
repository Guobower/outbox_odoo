# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Res_company_inherited(models.Model):
    _inherit = 'res.company' 
 
    url = fields.Char(
                      string="URL",
                      size=200
                      )
                           
    auth_code = fields.Char(
                            string="Auth Code",
                            size=40
                            )
    
    client_code = fields.Char(
                              string="Client Code",
                              size=20
                              )
    
    
    
