# -*- coding: utf-8 -*-
import datetime
from openerp import api
from openerp import fields
from openerp import models

class Ocorrencia(models.Model):
    _name = 'ocorrencia'
    _description = 'Ocorrencia'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    _defaults = {
        'name': lambda self, cr, uid, context = {}: self.pool.get('ir.sequence').get(cr, uid, 'ocorrencia.ocorrencia_sequence'),
        'status_ocorrencia': 1,
        'data_ultima_abertura': datetime.date.today()
        }
    
    name = fields.Char(
                       string="Protocolo",
                       size=250,
                       required=True,
                       track_visibility='onchange')
                       
    contrato = fields.Many2one(
                               string="Contrato",
                               comodel_name='account.analytic.account',
                               help="Contrato ao qual a ocorrência está vinculada")
        
    titulo = fields.Char(
                         string="Titulo",
                         size=250,
                         required=True,
                         track_visibility='onchange')
    
    descricao = fields.Text(
                            string="Descricao",
                            help="Descrição da ocorrência",
                            track_visibility="onchange")
    
    tipo_ocorrencia = fields.Many2one(
                                      comodel_name='tipo_ocorrencia',
                                      string='Tipo',
                                      help='Tipo da ocorrêmcia',
                                      track_visibility='onchange')
                                      
    status_ocorrencia = fields.Many2one(
                                        comodel_name='status_ocorrencia',
                                        string='Status',
                                        help='Status da ocorrêmcia',
                                        required=True,
                                        track_visibility='onchange')
        
    localidade = fields.Many2one(
                                 comodel_name='localidade',
                                 string='Localidade',
                                 help='Localidade',
                                 track_visibility='onchange')
    
    imputavel = fields.Selection(
                                 string="Imputavel",
                                 help="Ocorrência deve ser imputada?",
                                 selection=[(1, 'Não'),
                                 (2, 'Sim')],
                                 track_visibility="onchange")
    
    color = fields.Integer(
                           string="Color Index")
                           
    tempo_efetivo_indisponibilidade = fields.Integer(
                                                     string="Tempo Efetivo de Indisponibilidade (m)",
                                                     help="Registro de tempo efetivo de indisponibilidade",
                                                     track_visibility="onchange"
                                                     )
    
    data_ultimo_fechamento = fields.Datetime(
                                             string="Data do Ultimo Fechamento",
                                             help="Data do último fechamento da ocorrência",
                                             track_visibility="onchange"
                                             )
    
    data_ultima_abertura = fields.Datetime(
                                           string="Data da Ultima Abertura",
                                           help="Data da última abertura da ocorrência",
                                           track_visibility="onchange"
                                           )
                                             
    abre_fecha_ocorrencia = fields.One2many(
                                            comodel_name='abre_fecha_ocorrencia',
                                            inverse_name='ocorrencia',
                                            string='Aberturas e Fechamentos',
                                            help='Aberturas e fechamentos da ocorrência')
                                
    informacoes_tecnicas = fields.Text('Informacoes Tecnicas', related='contrato.partner_id.informacoes_tecnicas', store=True)
     
    textos_chamados = fields.Text('Textos de chamados', related='contrato.partner_id.textos_chamados', store=True) 
    
    #contato_localidade = fields.One2many('Contatos de Localidades', related='contrato.contato_localidade', store=True) 
    
    
    
    def on_change_tipo(self, cr, user, ids, tipo_ocorrencia, context=None):
        '''
            Descrição:
              Esta função tem como objetivo modificar o titulo e o texto padrao do chamado
              de acordo com o tipo.
        
            Utilização:
              on_change_tipo(param1)
        
            Parâmetros:
              cr
                Cursor do banco de dados
              uid
                Usuário do sistema
              ids
                IDs da fatura em questão
              tipo_ocorrencia
                Tipo da ocorrência selecionado no formulario  
              context
                Contexto atual
        '''
        if tipo_ocorrencia:
            tipo = self.pool.get('tipo_ocorrencia').browse(cr, user, tipo_ocorrencia)
            res = {
                'value': {
                    # Define a distancia entre as cidades e o tempo médio do percurso.
                    'titulo': tipo.titulo_padrao,
                    'descricao': tipo.texto_padrao
                }
            }
            # Return the values to update it in the view.
            return res
        
        
    def on_change_titulo_descricao(self, cr, user, ids, titulo, descricao, localidade, context=None):
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
        if localidade:
            if titulo:
                if descricao:
                    obj_localidade = self.pool.get('localidade').browse(cr, user, localidade)
                    res = {
                        'value': {
                            # Define a distancia entre as cidades e o tempo médio do percurso.
                            'titulo': str(titulo).replace('#cidade#', '' + obj_localidade.name),
                            'descricao': str(descricao).replace('#cidade#', '' + obj_localidade.name)
                        }
                    }
                    # Return the values to update it in the view.
                    return res
    
    
    def reabrir_ocorrencia(self, cr, user, ids, context=None):
        '''
        import datetime
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, user, ids[0])
        
        obj_ocorrencia.write({'status_ocorrencia': 1, 'data_ultima_abertura':datetime.datetime.today()}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        '''
        return {
            'name':'abre_fecha_ocorrencia.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'abre_fecha_ocorrencia',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_ocorrencia': ids[0],
                'default_name': '1',
            }
        }
    
    
    def fechar_ocorrencia(self, cr, user, ids, context=None):
        '''
        import datetime
        
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, user, ids[0])
        
        tempo_efetivo_indisponibilidade = (datetime.datetime.today() - datetime.datetime.strptime(obj_ocorrencia.data_ultima_abertura, '%Y-%m-%d %H:%M:%S')).total_seconds()
        
        obj_ocorrencia.write({'status_ocorrencia': 2, 'data_ultimo_fechamento':datetime.datetime.today(), 'tempo_efetivo_indisponibilidade': round(tempo_efetivo_indisponibilidade/60)}, context=context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        '''
        import datetime
        
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, user, ids[0])
        
        tempo_efetivo_indisponibilidade = (datetime.datetime.today() - datetime.datetime.strptime(obj_ocorrencia.data_ultima_abertura, '%Y-%m-%d %H:%M:%S')).total_seconds()
        
        return {
            'name':'abre_fecha_ocorrencia.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'abre_fecha_ocorrencia',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_ocorrencia': ids[0],
                'default_name': '2',
                'default_tempo_efetivo_indisponibilidade': round(tempo_efetivo_indisponibilidade / 60),
            }
        }
    
    def adicionar_observacao(self, cr, user, ids, context=None):
        
        return {
            'name':'abre_fecha_ocorrencia.form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'abre_fecha_ocorrencia',
            'type':'ir.actions.act_window',
            'target':'new',
            'context': {
                'default_ocorrencia': ids[0],
                'default_name': '3',
            }
        }
        
        
    def report_format_data(self, cr, uid, data, context=None):
        import datetime
        
        return datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
    
    def report_format_operacao(self, cr, uid, operacao, context=None):
        retorno = ""
        
        if operacao:
            if operacao == '1':
                retorno = "Reabertura"
            if operacao == '2':
                retorno = "Fechamento"
            if operacao == '3':
                retorno = "Observacao"
        
        return retorno
    
    def report_format_imputavel(self, cr, uid, imputavel, context=None):
        retorno = ""
        
        if imputavel:
            if imputavel == 1:
                retorno = "Nao Imputavel"
            if imputavel == 2:
                retorno = "Imputavel"

        return retorno
    
    def report_format_aberto_fechado(self, cr, uid, status, context=None):
        retorno = ""
        
        if status:
            if status == 1:
                retorno = "Aberto a"
            if status == 2:
                retorno = "Tempo Efetivo de Indisponibilidade"

        return retorno
    
    def report_format_tempo_efetivo_indisponibilidade(self, cr, uid, ocorrencia, context=None):
        import datetime
        retorno = ""
        
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, uid, ocorrencia)
        
        if obj_ocorrencia.status_ocorrencia:
            if obj_ocorrencia.status_ocorrencia.id == 1:
                tempo_efetivo_indisponibilidade = (datetime.datetime.today() - datetime.datetime.strptime(obj_ocorrencia.create_date, '%Y-%m-%d %H:%M:%S')).total_seconds()
                
                retorno = self.formatar_hora_extenso(tempo_efetivo_indisponibilidade)
            if obj_ocorrencia.status_ocorrencia.id == 2:
                retorno = self.formatar_hora_extenso(obj_ocorrencia.tempo_efetivo_indisponibilidade * 60)

        return retorno
    
    def formatar_hora_extenso(self, segundos):
        #dias = segundos // 86400
        #segundos_rest = segundos % 86400
        horas = segundos // 3600
        segundos_rest = segundos % 3600
        minutos = segundos_rest // 60
        minutos_totais = segundos // 60
        
        return str(int(round(horas))) + ' horas e ' + str(int(round(minutos))) + ' minutos (' + str(int(round(minutos_totais))) + ' minutos)'
    
    def houve_nova_informacao(self, cr, uid, ocorrencia, context=None):
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, uid, ocorrencia)
        
        retorno = ""
        if len(obj_ocorrencia.abre_fecha_ocorrencia) > 0:
            retorno = "A seguinte informacao foi adicionada a ordem de servico:"
        
        return retorno
    
    def ultima_informacao(self, cr, uid, ocorrencia, context=None):
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, uid, ocorrencia)
        
        retorno = ""
        cont_iteracoes = len(obj_ocorrencia.abre_fecha_ocorrencia)
        if cont_iteracoes > 0:
            retorno = obj_ocorrencia.abre_fecha_ocorrencia[cont_iteracoes-1].descricao
        return retorno
    
    def solicitar_visita(self, cr, uid, ids, context=None):
        obj_ocorrencia = self.pool.get('ocorrencia').browse(cr, uid, ids[0])
        
        valores = {
            'ocorrencia': obj_ocorrencia.id,
            'cliente': obj_ocorrencia.contrato.partner_id.id,
            'contrato': obj_ocorrencia.contrato.id,
            'localidade': obj_ocorrencia.localidade.id,
            'atividade': obj_ocorrencia.titulo,
            'observacoes': obj_ocorrencia.descricao
        }

        obj_agenda_tecnicos = self.pool.get('agenda_tecnicos').create(cr, uid, valores, context)
        
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'agenda_tecnicos', 'email_template_solicitacao_visita_tecnica')[1]
        except ValueError:
            template_id = False
        
        self.pool['email.template'].send_mail(
                                              cr, uid, template_id, obj_agenda_tecnicos, force_send=True,
                                              context=None)
           
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Solicitação Concluída!',
                'text': 'Foi solicitada a visita técnica ao setor responsável, aguarde retorno!',
                'sticky': False
                }
        }