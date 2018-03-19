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
                            ('2', 'Fechamento'),
                            ('3', 'Observação')],
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
         
    anexo2 = fields.Binary(
        string='Anexo',
        help='Anexo.',
        attachment=True)
    
    anexo_filename = fields.Char("Anexo")
    
    @api.model
    def create(self, values, anexo_lote=0):
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
        
        template = self.env['email.template'].browse(template_id)
        
        if record['anexo_filename']:
            attachment = {
                'name': str(record['anexo_filename'].encode('ascii', 'ignore').decode('ascii')),
                'datas': record['anexo2'],
                'datas_fname': str(record['anexo_filename'].encode('ascii', 'ignore').decode('ascii')),
                'res_model': 'abre_fecha_ocorrencia',
                'res_id': record['id'],
                'type': 'binary'
            }
            print 'Abre-fecha: '+str(values)
            arquivo_anexo = self.env['ir.attachment'].create(attachment)
            # Add Attachment
            template.attachment_ids = [(6,0,[arquivo_anexo.id])]
        
        if anexo_lote > 0:
            template.attachment_ids = [(6,0,[anexo_lote])]
            
        template.send_mail(record['ocorrencia'].id, force_send=True)
        
        # Return the record so that the changes are applied and everything is stored.
	return record