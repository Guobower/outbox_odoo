# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Trabalhe_conosco(models.Model):
    _name = 'trabalhe_conosco'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True,
        track_visibility='onchange')
    
    email = fields.Char(
        string="E-mail",
        size=100,
        track_visibility='onchange')
    
    curriculo = fields.Char(
        string="Curriculo",
        size=100,
        track_visibility='onchange')
    
    mensagem = fields.Text(
        string="Mensagem",
        track_visibility='onchange')
    
    
    def download_curriculo(self, cr, user, ids, context=None):
        trabalhe_conosco = self.pool.get('trabalhe_conosco').browse(cr, user, ids[0])
        url = 'http://www.cinte.com.br/2016/trabalheConosco/'+str(trabalhe_conosco.curriculo) 
        res = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url,
        }
        
        return res