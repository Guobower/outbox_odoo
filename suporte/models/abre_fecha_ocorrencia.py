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
                            required=True,
                            track_visibility="onchange")
        
    tempo_efetivo_indisponibilidade = fields.Integer(
                                                     string="Tempo Efetivo de Indisponibilidade (m)",
                                                     help="Registro de tempo efetivo de indisponibilidade",
                                                     track_visibility="onchange"
                                                     )

    desligamento = fields.Boolean(
        string="É desligamento?",
        help="Marque se for desligamento e quiser realizar o cálculo de uptime do ativo",
        track_visibility="onchange"
    )

    uptime = fields.Char(
        string="Uptime do ativo",
        size=5,
        help="Informe o uptime do ativo para que o Odoo preencha o texto do fechamento automaticamente",
        track_visibility="onchange"
    )
                                                     
    ocorrencia = fields.Many2one(
                                 string="Ocorrência",
                                 comodel_name='ocorrencia',
                                 required=True,
                                 help="Ocorrência a qual a abertura/fechamento está vinculada")
         
    anexo2 = fields.Binary(
        string='Anexo',
        help='Anexo.',
        attachment=True)
    
    anexo_filename = fields.Char("Anexo")

    
    def on_change_descricao(self, cr, user, ids, descricao, ocorrencia, context=None):
        '''
            Descrição:
              Esta função tem como objetivo modificar o titulo e o texto do chamado trocando 
              #cidade# pelo nome da localidade.
        
            Utilização:
              on_change_tipo(param1)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              titulo
                Titulo da ocorrência
              descricao
                Descricao da ocorrência
              localidade
                Localidade da ocorrência
              context
                Contexto atual
        '''
        if ocorrencia:
            if descricao:
                obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, user, ocorrencia)
                res = {
                    'value': {
                        # Define a distancia entre as cidades e o tempo médio do percurso.
                        'descricao': str(descricao).replace('#cidade#', '' + obj_ocorrencia.localidade.name)
                    }
                }
                # Return the values to update it in the view.
                return res

    def on_change_uptime(self, cr, user, ids, desligamento, uptime, context=None):
        if desligamento:
            hora_uptime = self.calcular_hora_uptime(uptime, context)
            if hora_uptime:
                texto_fechamento = "O circuito de dados da localidade #cidade# consta em nossos sistemas como havendo " \
                                   "retornado a funcionar normalmente sem intervenção corretiva da CINTE, e por este motivo" \
                                   " estamos encerrando a ocorrência. Após análise, verificamos que o link foi " \
                                   "restabelecido às " + hora_uptime + " e o uptime do equipamento é de " + self.formatar_uptime(uptime) + ", por este motivo " \
                                   "estamos encerrando a ocorrência. Em caso de anormalidades em sua operação, " \
                                   "por gentileza contatem novamente o suporte técnico da CINTE, através do e-mail " \
                                   "suporte@cinte.com.br ou pelo telefone (84)3231-2922."
                res = {
                    'value': {
                        # Define a distancia entre as cidades e o tempo médio do percurso.
                        'descricao': texto_fechamento
                    }
                }

                return res

    def calcular_hora_uptime(self, uptime, context):
        from datetime import datetime, timedelta
        import pytz

        uptime = uptime.split(":")

        if len(uptime) > 1:
            hora_atual = datetime.now(pytz.timezone(context["tz"]))

            hora_uptime = hora_atual - timedelta(hours=float(uptime[0])) - timedelta(minutes=float(uptime[1]))

            return hora_uptime.strftime('%Hh%M')

    def formatar_uptime(self, uptime):
        uptime = uptime.split(":")

        if len(uptime) > 1:
            return uptime[0] + " horas e " + uptime[1] + " minutos"

    @api.model
    def create(self, values, anexo_lote=0):
        import datetime
        from datetime import timedelta
        # Override the original create function for the res.partner model
        obj_ocorrencia = self.pool.get('ocorrencia').browse(self.env.cr, self.env.uid, values['ocorrencia'])
        
        values['descricao'] = str(values['descricao']).replace('#cidade#', '' + obj_ocorrencia.localidade.name)
        
        record = super(Abre_fecha_ocorrencia, self).create(values)
        
        
        if record['name'] == '1':
            obj_ocorrencia.write({'status_ocorrencia': 1, 'data_ultima_abertura':datetime.datetime.today() - timedelta(hours=3)}, context=None)
            
        if record['name'] == '2':
            obj_ocorrencia.write({'status_ocorrencia': 2, 'tempo_efetivo_indisponibilidade': obj_ocorrencia.tempo_efetivo_indisponibilidade + record['tempo_efetivo_indisponibilidade'], 'data_ultimo_fechamento':datetime.datetime.today() - timedelta(hours=3)}, context=None)
        
        
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
            arquivo_anexo = self.env['ir.attachment'].create(attachment)
            # Add Attachment
            template.attachment_ids = [(6,0,[arquivo_anexo.id])]
        else:
            # Remove Attachment
            template.attachment_ids = [(6,0,[])]
            if anexo_lote > 0:
                template.attachment_ids = [(6,0,[anexo_lote])]
        
        
        template.send_mail(record['ocorrencia'].id, force_send=True)
        
        # Return the record so that the changes are applied and everything is stored.
        return record