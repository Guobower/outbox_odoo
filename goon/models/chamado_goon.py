# -*- coding: utf-8 -*-
import json
from openerp import api
from openerp import fields
from openerp import models
from suds.client import Client

class Chamado_goon(models.Model):
    _name = 'chamado_goon'
    _description = 'Chamado no Goon'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    name = fields.Char(
                       string='ID Goon',
                       help='Id do chamado no Goon',
                       size=200,
                       required=True)
    
    tecnico = fields.Many2one(
                              string='Tecnico',
                              help='Tecnico responsavel',
                              comodel_name='tecnico',
                              required=True)
    
    data = fields.Datetime(
                           string='Data',
                           help='Data do Chamado')
                       
    observacao = fields.Text(
                             string='Observacao')
                       
    localidade = fields.Many2one(
                                 string='Localidade',
                                 help='Localidade de atendimento do cliente',
                                 comodel_name='localidade')
        
    tipo_servico = fields.Many2one(
                                   string='Tipo de Servico',
                                   help='Tipo de Serviço no Goon',
                                   comodel_name='tipo_servico')
        
    ocorrencia = fields.Many2one(
                                 comodel_name='ocorrencia',
                                 string='Ocorrencia',
                                 help='Ocorrencia vinculada ao chamado no Goon',
                                 track_visibility='onchange')
                                 
    agenda_tecnicos = fields.Many2one(
                                      comodel_name='agenda_tecnicos',
                                      string='Agenda dos Tecnicos',
                                      help='Agenda dos tecnicos vinculada ao chamado no Goon',
                                      track_visibility='onchange')
                              
    
    status = fields.Selection(
                              string="Status",
                              selection=[('DESP', 'Despachado'),
                              ('ACTE', 'Recebido pelo Agente'),
                              ('INIC', 'Iniciado'),
                              ('CTEC', 'Cancelado pelo Agente'),
                              ('COPE', 'Cancelado pelo Atendente'),
                              ('CCLI', 'Cancelado pelo cliente'),
                              ('FIOK', 'Finalizado OK'),
                              ('AGEN', 'Agendado')],
                              track_visibility='onchange'
                              )
                              
    erro = fields.Text(
                       string='Erro')
    '''      
    TODO
    chamado
    '''
        
    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(Chamado_goon, self).create(values)
        
        self.pool.get('chamado_goon').sincronizar_dados(self.env.cr, self.env.uid, record['id'])
        
        # Return the record so that the changes are applied and everything is stored.
	return record
    
    
    
    def sincronizar_dados(self, cr, user, ids, context=None):
        from suds.client import Client
        import json
        
        obj_companhia = self.pool.get('res.company').browse(cr, user, 1)
        obj_chamado_goon = self.pool.get('chamado_goon').browse(cr, user, ids)
        obj_agenda_tecnicos = self.pool.get('agenda_tecnicos').browse(cr, user, obj_chamado_goon.agenda_tecnicos.id)
        
        client = Client(obj_companhia.url)
        
        if obj_chamado_goon.name:
            if obj_chamado_goon.tecnico.id == obj_agenda_tecnicos.name.id and obj_chamado_goon.data == obj_agenda_tecnicos.data:
                return self.acompanharOrdemServico(obj_companhia, obj_chamado_goon, obj_agenda_tecnicos)
            else:
                self.acompanharOrdemServico(obj_companhia, obj_chamado_goon, obj_agenda_tecnicos)
                return self.editarOrdemServico(obj_companhia, obj_chamado_goon, obj_agenda_tecnicos)
        else:
            return self.abrirOrdemServico(obj_companhia, obj_chamado_goon)
    
    
    def abrirOrdemServico(self, obj_companhia, obj_chamado_goon):
        client = Client(obj_companhia.url)
        retorno = json.loads(client.service.OpenOrdemServico(
                             '88E9F98B63F15D7F635B0D6027DC4443EE44B50F', 
                             obj_companhia.client_code, 
                             obj_chamado_goon.id, 
                             obj_chamado_goon.ocorrencia.contrato.partner_id.id_syncron, 
                             obj_chamado_goon.tipo_servico.id, 
                             '0',
                             str(obj_chamado_goon.data).replace(" ", "T"), 
                             'N', 
                             'Desconhecido', 
                             obj_chamado_goon.ocorrencia.contrato.partner_id.phone, 
                             obj_chamado_goon.localidade.logradouro, 
                             obj_chamado_goon.localidade.numero, 
                             obj_chamado_goon.localidade.complemento, 
                             obj_chamado_goon.localidade.bairro, 
                             obj_chamado_goon.localidade.cidade.name, 
                             obj_chamado_goon.localidade.estado.code, 
                             obj_chamado_goon.localidade.cep, 
                             obj_chamado_goon.observacao, 
                             obj_chamado_goon.localidade.latitude, 
                             obj_chamado_goon.localidade.longitude, 
                             str(obj_chamado_goon.create_date).replace(" ", "T"), 
                             '',
                             0,
                             '0',
                             obj_chamado_goon.tecnico.codigo_usuario,
                             str(obj_chamado_goon.data).replace(" ", "T"),
                             '',
                             'Internal'))

        if retorno['success']:
            obj_chamado_goon.write({'name': retorno['numeroOS'], 'status': 'DESP'})
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Sincronização Concluída!',
                    'text': 'Dados enviados para o Goon.',
                    'sticky': True
                    }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Erro ao sincronizar!',
                    'text': 'Houve um erro ao sincronizar, contate o administrador do sistema.',
                    'sticky': False
                    }
            }
            
    def editarOrdemServico(self, obj_companhia, obj_chamado_goon, obj_agenda_tecnicos):
        client = Client(obj_companhia.url)
        retorno = json.loads(client.service.SetAcompanhamentoOrdemServico(
                             'A7E43A2C4974A8282B6E6754AF5F06DCA0DE988B', 
                             obj_companhia.client_code, 
                             obj_chamado_goon.id,
                             2,
                             obj_agenda_tecnicos.name.codigo_usuario,
                             str(obj_agenda_tecnicos.data).replace(" ", "T"),
                             obj_chamado_goon.status,
                             'true',
                             'Internal',
                             0))

        if retorno['success']:
            obj_chamado_goon.write({'data': obj_agenda_tecnicos.data, 'tecnico': obj_agenda_tecnicos.name.id})
            return obj_chamado_goon.status
        
    def acompanharOrdemServico(self, obj_companhia, obj_chamado_goon, obj_agenda_tecnicos):
        client = Client(obj_companhia.url)
        retorno = json.loads(client.service.GetAcompanhamentoOrdemServico(
                             'B2754231E374B8DAB17B09DA83E40AF1354D3EFD', 
                             obj_companhia.client_code, 
                             obj_chamado_goon.id))

        if retorno['success']:
            obj_chamado_goon.write({'status': retorno['status']})
            obj_agenda_tecnicos.write({'status_goon': retorno['status']})
            return retorno['status']