# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Abre_fecha_ocorrencia(models.Model):
    _name = 'abre_fecha_ocorrencia'
    _description = 'Tipo de ocorrencia'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Selection(
                            string="Tipo",
                            selection=[('1', 'Abertura'),
                            ('2', 'Fechamento')],
                            required=True,
                            track_visibility='onchange')
    
    descricao = fields.Text(
                            string="Descricao",
                            help="Descrição da abertura/fechamento da ocorrência",
                            track_visibility="onchange")
        
    tempo_efetivo_indisponibilidade = fields.Integer(
                                                     string="Tempo Efetivo de Indisponibilidade (m)",
                                                     help="Registro de tempo efetivo de indisponibilidade",
                                                     track_visibility="onchange"
                                                     )
                                                     
    ocorrencia = fields.Many2one(
                                 string="Ocorrência",
                                 comodel_name='ocorrencia',
                                 help="Ocorrência a qual a abertura/fechamento está vinculada")
         
                                 
    @api.model
    def create(self, values):
        import datetime
        # Override the original create function for the res.partner model
        record = super(Abre_fecha_ocorrencia, self).create(values)
        
        obj_ocorrencia = self.pool.get('ocorrencia').browse(self.env.cr, self.env.uid, record['ocorrencia'].id)
        
        if record['name'] == '1':
            obj_ocorrencia.write({'status_ocorrencia': 1, 'data_ultima_abertura':datetime.datetime.today()}, context=None)
            
        if record['name'] == '2':
            obj_ocorrencia.write({'status_ocorrencia': 2, 'tempo_efetivo_indisponibilidade': obj_ocorrencia.tempo_efetivo_indisponibilidade + record['tempo_efetivo_indisponibilidade'], 'data_ultimo_fechamento':datetime.datetime.today()}, context=None)
        
        
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(self.env.cr, self.env.uid, 'suporte', 'email_template_abre_fecha_ocorrencia')[1]
        except ValueError:
            template_id = False
            
        self.pool['email.template'].send_mail(
           self.env.cr, self.env.uid, template_id, record['ocorrencia'].id, force_send=True,
           context=None)
        
        
        # Return the record so that the changes are applied and everything is stored.
	return record