# -*- coding: utf-8 -*-
from openerp import models, fields

class Crm_lead_inherited(models.Model):
    _inherit = 'crm.lead' 

    type = fields.Selection(
        selection=[('lead', 'Lead'),
                   ('opportunity', 'Opportunity'),
                   ('licitados', 'Licitados')],
        string='Type',
        select=True,
        help='Usados para separar prospectos, oportunidades e licitados')
    
    
    referred = fields.Many2one(
        comodel_name='res.users',
        string='Indicado por:',
        help='Quem realizou a indicação do prospecto?')
    
    tipo_servico = fields.Selection(
        selection=[('fibra', 'Fibra'),
                   ('radio', 'Rádio'),
                   ('ambos', 'Ambos')],
        string='Tipo do Serviço',
        select=True,
        help='Tipo de serviço oferecido ao cliente')
    
    motivo_desistencia = fields.Selection([
                   ('instalacao', 'Dificuldade de Instalação'),
                   ('prazo', 'Prazo de Entrega da Proposta Elevado'),
                   ('prazo_instalacao', 'Prazo de Instalação Elevado'),
                   ('viabilidade', 'Sem Viabilidade Técnica'),
                   ('taxa', 'Taxa de Instalação'),
                   ('valor', 'Valor do Mega'),
                   ('outros', 'Outros')],
        string='Motivo da Perda',
        select=True,
        help='Motivo da perda/desistência do Prospecto/Cliente')
    
    
    
    # Campos necessários para as Licitações
    tipo_licitacao = fields.Selection(
        selection=[('eletronica', 'Eletrônica'),
                   ('presencial', 'Presencial')],
        string='Tipo da Licitação',
        select=True,
        help='Tipo da licitação')
    
    data_abertura_edital = fields.Date(
        string='Abertura do Edital',
        help='Data da Abertura do Edital')
    
    data_licitacao = fields.Datetime(
        string='Data da Licitação',
        help='Data da Licitação')
    
    edital = fields.Binary(
        string='Edital',
        help='PDF do Edital.')
    
    edital_filename = fields.Char("Arquivo do Edital")
    
    anexo_edital = fields.Binary(
        string='Termo de Referência',
        help='PDF do termo de referência do Edital.')
    
    anexo_edital_filename = fields.Char("Arquivo do Anexo Edital")
    
    numero_edital = fields.Char(
        string='Número/Identificação do Edital',
        size=200,
        help='Número ou Identificação do Edital do Orgão')
    
    objeto_contrato = fields.Text(
        string='Objeto',
        help='Objeto do Edital')
    
    objeto_atende = fields.Selection(
        selection=[(1, 'Sim'), (2, 'Não')],
        string='Objeto atende?',
        help='O objeto do edital atende os serviços da Cinte?')
    
    objeto_atende_observacoes = fields.Text(
        string='Observações',
        help='Observações sobre o objeto do edital.')
    
    objeto_atende_ultima_lembranca = fields.Datetime(
        string='Lembrado em',
        help='Data da última solicitação de lembrança.')
    
    objeto_atende_responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável')
    
    restricao_participacao = fields.Selection(
        selection=[(1, 'Sim'), (2, 'Não')],
        string='Há restrição para nossa participação?',
        help='Há algo que restrinja a nossa participação na licitação?')
    
    restricao_participacao_observacoes = fields.Text(
        string='Observações',
        help='Observações sobre restrição de participação.')
    
    restricao_participacao_ultima_lembranca = fields.Datetime(
        string='Lembrado em',
        help='Data da última solicitação de lembrança.')
    
    restricao_participacao_responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável')
    
    financeiramente_viavel = fields.Selection(
        selection=[(1, 'Sim'), (2, 'Não')],
        string='É financeiramente viável?',
        help='A licitação é financeiramente viável para os preços praticados pela Cinte?')
    
    financeiramente_viavel_observacoes = fields.Text(
        string='Observações',
        help='Observações sobre a viabilidade financeira da licitação.')
    
    financeiramente_viavel_ultima_lembranca = fields.Datetime(
        string='Lembrado em',
        help='Data da última solicitação de lembrança.')
    
    financeiramente_viavel_responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável')
    
    orgao_interesse = fields.Selection(
        selection=[(1, 'Sim'), (2, 'Não')],
        string='É um orgão de interesse?',
        help='O orgão da licitação é de interesse da Cinte?')
    
    orgao_interesse_observacoes = fields.Text(
        string='Observações',
        help='Observações sobre o orgão da licitação.')
    
    orgao_interesse_ultima_lembranca = fields.Datetime(
        string='Lembrado em',
        help='Data da última solicitação de lembrança.')
    
    orgao_interesse_responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável')
    
    data_fim_esclarecimentos = fields.Date(
        string='Prazo para Esclarecimentos',
        help='Data final para solicitação de esclarecimentos.')
    
    data_fim_impugnacao = fields.Date(
        string='Prazo para Impugnação',
        help='Data final para entrada em processo de impugnação.')
    
    ata_pregao = fields.Binary(
        string='Ata do Pregão',
        help='Anexo da ata do pregão.')
    
    ata_pregao_filename = fields.Char("Arquivo da Ata do Pregão")
    
    vencemos_perdemos = fields.Selection(
        selection=[(1, 'Vencemos'), (2, 'Perdemos')],
        string='Resultado',
        help='Resultado da Licitação')
    
    vencedor = fields.Char(
        string='Vencedor',
        size=200,
        help='Vencedor da Licitação')
    
    documentacao_vencedor = fields.Binary(
        string='Documentação do Vencedor',
        help='Anexo com a documentação do vencedor para análise.')
    
    documentacao_vencedor_filename = fields.Char("Arquivo da Documentação do Vencedor")
    
    certidoes = fields.Selection(
        selection=[(1, 'OK'), (2, 'Pendente')],
        string='Certidões',
        help='Nossas certidões estão prontas?')
    
    certidoes_observacoes = fields.Text(
        string='Observações',
        help='Observações sobre as certidões.')
    
    certidoes_responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável')
    
    certidoes_ultima_lembranca = fields.Datetime(
        string='Lembrado em',
        help='Data da última solicitação de lembrança.')
    
    valor_ganho = fields.Float(
        string='Valor da Proposta Vencedora',
        help='Valor final da proposta vencedora da licitaçao.')
    
    valor_projeto = fields.Float(
        string='Valor Orçado para o Projeto',
        help='Valor orçado pela equipe de projetos para a implantação do projeto.')
    
    
    def cobrar_certidoes(self, cr, uid, ids, context=None):
        import time
        if not context:
            context= {}
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'comercial', 'email_template_vista_certidoes')[1]
        except ValueError:
            template_id = False
            
        lead_obj = self.pool.get('crm.lead')
        lead_obj.write(cr, uid, ids[0], {'certidoes_ultima_lembranca': time.strftime('%Y-%m-%d %H:%M')}, context=context)     
            
        return self.pool['email.template'].send_mail(
           cr, uid, template_id, ids[0], force_send=True,
           context=None)
        
    def cobrar_avaliacao_financeira(self, cr, uid, ids, context=None):
        import time
        if not context:
            context= {}
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'comercial', 'email_template_vista_financeira')[1]
        except ValueError:
            template_id = False
        
        lead_obj = self.pool.get('crm.lead')
        lead_obj.write(cr, uid, ids[0], {'financeiramente_viavel_ultima_lembranca': time.strftime('%Y-%m-%d %H:%M')}, context=context)     
            
        return self.pool['email.template'].send_mail(
           cr, uid, template_id, ids[0], force_send=True,
           context=None)
        
    
    def cobrar_vista_objeto(self, cr, uid, ids, context=None):
        import time
        if not context:
            context= {}
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'comercial', 'email_template_vista_objeto')[1]
        except ValueError:
            template_id = False
        
        lead_obj = self.pool.get('crm.lead')
        lead_obj.write(cr, uid, ids[0], {'objeto_atende_ultima_lembranca': time.strftime('%Y-%m-%d %H:%M')}, context=context)     
            
        return self.pool['email.template'].send_mail(
           cr, uid, template_id, ids[0], force_send=True,
           context=None)
        
        
    def cobrar_vista_orgao(self, cr, uid, ids, context=None):
        import time
        if not context:
            context= {}
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'comercial', 'email_template_vista_orgao')[1]
        except ValueError:
            template_id = False
        
        lead_obj = self.pool.get('crm.lead')
        lead_obj.write(cr, uid, ids[0], {'orgao_interesse_ultima_lembranca': time.strftime('%Y-%m-%d %H:%M')}, context=context)     
            
        return self.pool['email.template'].send_mail(
           cr, uid, template_id, ids[0], force_send=True,
           context=None)
        
        
    def cobrar_vista_restricoes(self, cr, uid, ids, context=None):
        import time
        if not context:
            context= {}
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'comercial', 'email_template_vista_restricoes')[1]
        except ValueError:
            template_id = False
        
        lead_obj = self.pool.get('crm.lead')
        lead_obj.write(cr, uid, ids[0], {'restricao_participacao_ultima_lembranca': time.strftime('%Y-%m-%d %H:%M')}, context=context)     
            
        return self.pool['email.template'].send_mail(
           cr, uid, template_id, ids[0], force_send=True,
           context=None)
    
    def acionar_juridico(self, cr, uid, ids, context=None):
        import time
        if not context:
            context= {}
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'comercial', 'email_template_acionar_juridico')[1]
        except ValueError:
            template_id = False
        
        return self.pool['email.template'].send_mail(
           cr, uid, template_id, ids[0], force_send=True,
           context=None)
        
    
    def on_change_aprovacoes(self, cr, user, ids, certidoes, orgao_interesse, financeiramente_viavel, restricao_participacao, objeto_atende, context=None):
        res = {
             'value': {
                'color': 0,
            }
        }
        
        if (certidoes == 2) or (orgao_interesse == 2) or (financeiramente_viavel == 2) or (restricao_participacao == 1) or (objeto_atende == 2):
            res = {
                 'value': {
                    'color': 2,
                }
            }
        
        if (certidoes == 1) and (orgao_interesse == 1) and (financeiramente_viavel == 1) and (restricao_participacao == 2) and (objeto_atende == 1):
            res = {
                 'value': {
                    'color': 5,
                }
            }
        
        
        # Return the values to update it in the view.
        return res