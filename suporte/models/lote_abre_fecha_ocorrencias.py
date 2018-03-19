# -*- coding: utf-8 -*-
import datetime
from openerp import api
from openerp import fields
from openerp import models

class Lote_abre_fecha_ocorrencias(models.Model):
    _name = 'lote_abre_fecha_ocorrencias'
    _description = 'Fechamento e reaberturas de ocorrencias em lote'
    
    name = fields.Selection(
                            string="Tipo",
                            selection=[('1', 'Abertura'),
                            ('2', 'Fechamento'),
                            ('3', 'Observação')],
                            required=True)
    
    descricao = fields.Text(
                            string="Descricao",
                            help="Descrição da abertura/fechamento da ocorrência")
                                                     
    ocorrencia = fields.Many2many(
                                  string="Ocorrência",
                                  comodel_name='ocorrencia',
                                  help="Ocorrência a qual a abertura/fechamento está vinculada")
         
    contrato = fields.Many2one(
                               comodel_name='account.analytic.account',
                               string='Contrato')
    
    anexo = fields.Binary(
                          string='Anexo',
                          help='Anexo.',
                          attachment=True)
    
    anexo_filename = fields.Char("Anexo")
    
    operacao = fields.Integer(string='Operacao')
    
    data_hora_resolucao = fields.Datetime(
        string='Data/Hora de resolução',
        help='Informe a data e hora de resolução para o cálculo de tempo efetivo de indisponibilidade'
    )
    
    
    @api.model
    def create(self, values):
        import datetime
        # Override the original create function for the res.partner model
        record = super(Lote_abre_fecha_ocorrencias, self).create(values)
        
        ir_model_data = self.pool.get('ir.model.data')
        anexo_lote = 0
        if record['anexo_filename']:
            attachment = {
                'name': str(record['anexo_filename'].encode('ascii', 'ignore').decode('ascii')),
                'datas': record['anexo'],
                'datas_fname': str(record['anexo_filename'].encode('ascii', 'ignore').decode('ascii')),
                'res_model': 'lote_abre_fecha_ocorrencias',
                'res_id': record['id'],
                'type': 'binary',
                'parent_id': None
            }
            arquivo_anexo = self.env['ir.attachment'].create(attachment)
            # Add Attachment
            anexo_lote = arquivo_anexo.id
        
        for item in record['ocorrencia']:
            tempo_efetivo_indisponibilidade = 0
            if record['name'] == '2':
                obj_ocorrencia = self.pool.get('ocorrencia').browse(self.env.cr, self.env.uid, item.id)
                if obj_ocorrencia.tempo_efetivo_indisponibilidade:
                    tempo_efetivo_indisponibilidade = (datetime.datetime.strptime(record['data_hora_resolucao'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(obj_ocorrencia.data_ultima_abertura, '%Y-%m-%d %H:%M:%S')).total_seconds()
                else:
                    tempo_efetivo_indisponibilidade = (datetime.datetime.strptime(record['data_hora_resolucao'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(obj_ocorrencia.create_date, '%Y-%m-%d %H:%M:%S')).total_seconds()
                    
            valores = {
                'name': record['name'],
                'descricao': record['descricao'],
                'ocorrencia': item.id,
                'tempo_efetivo_indisponibilidade': round(tempo_efetivo_indisponibilidade/60)
            }

            obj_abre_fecha_ocorrencia = self.env['abre_fecha_ocorrencia'].create(valores,anexo_lote)
        
        # Return the record so that the changes are applied and everything is stored.
	return record