# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models
import simplejson
import urllib

class Agenda_tecnicos(models.Model):
    _name = 'agenda_tecnicos'
    
    name = fields.Many2one(
                           string='Tecnico',
                           help='Tecnico responsavel',
                           comodel_name='tecnico',
                           required=True)
        
    ocorrencia = fields.Many2one(
                                 string='Ocorrencia',
                                 help='Ocorrência vinculada a agenda',
                                 comodel_name='ocorrencia')
        
    cliente = fields.Many2one(
                              string='Cliente',
                              help='Cliente',
                              comodel_name='res.partner',
                              domain=[('customer', '=', 'true')])
        
    contrato = fields.Many2one(
                               string="Contrato",
                               comodel_name='account.analytic.account',
                               help="Contrato ao qual a agenda está vinculada")
        
    localidade = fields.Many2one(
                                 string='Localidade',
                                 help='Localidade de atendimento do cliente',
                                 comodel_name='localidade')
        
    tipo_servico = fields.Many2one(
                                   string='Tipo de Servico',
                                   help='Tipo de Serviço no Goon',
                                   comodel_name='tipo_servico')
    
    codigo_goon = fields.Many2one(
                                  string='Cod no Goon',
                                  help='Código do chamado no goon',
                                  comodel_name='chamado_goon')
        
    atividade = fields.Text(
                            string='Atividade',
                            help='Atividade a ser desenvolvida pela equipe')
    
    cidade_destino = fields.Many2one(
                                     string='Cidade de Destino',
                                     help='Cidade de destino final dos técnicos',
                                     comodel_name='l10n_br_base.city',
                                     domain=['|', ('state_id', '=', 70), ('state_id', '=', 72)])
    
    cidade_origem = fields.Many2one(
                                    string='Cidade de Origem',
                                    help='Cidade de origem dos técnicos',
                                    comodel_name='l10n_br_base.city',
                                    domain=['|', ('state_id', '=', 70), ('state_id', '=', 72)])

    cliente_nome = fields.Char(
                               string='Cliente',
                               size=200,
                               help='Nome do cliente')
    
    data = fields.Datetime(
                           string='Data',
                           help='Data da Agenda')
    
    distancia = fields.Float(
                             string='Distância (km)',
                             help='Distância percorrida entre a cidade de origem e a de destino do atendimento')
    
    equipe = fields.Many2many(
                              comodel_name='res.users',
                              string='Equipe',
                              help='Equipe envolvida na atividade')
    
    hospedagem = fields.Selection(
                                  selection=[(1, 'Sim'), (0, 'Não')],
                                  string='Hospedagem',
                                  help='Houve hospedagem no andamento das atividades?')
    
    motivo = fields.Selection(
                              selection=[('acidenteTrabalho', 'Acidente de trabalho'),
                              ('dificuldadesTecnicas', 'Dificuldades técnicas'),
                              ('equipamentoProblema', 'Equipamento deu problema'),
                              ('erroProjeto', 'Erro no projeto de instalação'),
                              ('faltaMaterial', 'Falta de material para realizar atividade'),
                              ('faltaCliente', 'Falta do cliente'),
                              ('faltaAtivar', 'Faltou ativar o link'),
                              ('faltouFechar', 'Faltou fechar o link'),
                              ('faltouTestar', 'Faltou testar o link'),
                              ('fatoresClimaticos', 'Fatores climáticos'),
                              ('imprevistosLocais', 'Imprevistos locais'),
                              ('naoDeuTempo', 'Não deu tempo'),
                              ('outros', 'Outros'),
                              ('problemaNaoCorrigido', 'Problema não foi corrigido corretamente'),
                              ('problemaLink', 'Problema no link'),
                              ('remanejamentoEquipe', 'Remanejamento da equipe')],
                              string='Motivo',
                              help='Motivo')
    
    observacoes = fields.Text(
                              string='Observações',
                              help='Adicione observações sobre o andamento da atividade')
    
    quantidade = fields.Float(
                              string='Quantidade',
                              help='Quantidade')
    
    status = fields.Selection(
                              selection=[('nao_aplica', 'Não se Aplica'),
                              ('pendente', 'Pendente'),
                              ('ok', 'OK'),
                              ('cancelada', 'Cancelada')],
                              string='Status',
                              help='Status da atividade')
    
    tempo_viagem = fields.Float(
                                string='Tempo de Viagem (minutos)',
                                help='Tempo médio do percurso entre a cidade de origem e de destino')
    
    tipo_cliente = fields.Selection(
                                    selection=[('bandaLarga', 'Banda Larga'),
                                    ('licitado', 'Licitado'),
                                    ('linkPuro', 'Link Puro'),
                                    ('backbone', 'Backbone'),
                                    ('atividadesInternas', 'Atividades Internas')],
                                    string='Tipo de Cliente',
                                    help='Tipo do cliente da atividade')
    
    turno = fields.Selection(
                             selection=[('primeiro', 'Primeiro'),
                             ('segundo', 'Segundo'),
                             ('terceiro', 'Terceiro'),
                             ('quarto', 'Quarto'),
                             ('quinto', 'Quinto')],
                             string='Turno',
                             help='Turno da atividade')
    
    veiculo = fields.Many2one(
                              string='Veículo',
                              help='Veículo utilizado na atividade',
                              comodel_name='fleet.vehicle')
    
    status_goon = fields.Selection(
                                   string="Status no Goon",
                                   selection=[('DESP', 'Despachado'),
                                   ('ACTE', 'Recebido pelo Agente'),
                                   ('INIC', 'Iniciado'),
                                   ('CTEC', 'Cancelado pelo Agente'),
                                   ('COPE', 'Cancelado pelo Atendente'),
                                   ('CCLI', 'Cancelado pelo cliente'),
                                   ('FIOK', 'Finalizado OK'),
                                   ('AGEN', 'Agendado')],
                                   )
    
    retirada_almoxarifado = fields.Many2one(
                              string='Retirada do Almoxarifado',
                              help='Retirada de materiais para uso na atividade',
                              comodel_name='stock.picking')
                              
    devolucao_almoxarifado = fields.Many2one(
                              string='Devolucao de Materiais',
                              help='Devolução de materiais não usados ou recolhidos na atividade',
                              comodel_name='stock.picking')
                              
                              
    def on_change_cidade(self, cr, user, ids, cidadeOrigem, cidadeDestino, context=None):
        if cidadeOrigem:
            if cidadeDestino:
                origem = self.pool.get('l10n_br_base.city').browse(cr, user, cidadeOrigem)
                destino = self.pool.get('l10n_br_base.city').browse(cr, user, cidadeDestino)
        
                url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origem.name + "," + origem.state_id.name + "&destinations=" + destino.name + "," + destino.state_id.name + "&key=AIzaSyDYRUAfCeT3uwCqZzvVoGv1QqRIAL0h5dk"
                url = url.encode('utf-8')
                result = simplejson.load(urllib.urlopen(url))
        
                distancia = (result['rows'][0]['elements'][0]['distance']['value']) / 1000
                tempoViagem = (result['rows'][0]['elements'][0]['duration']['value']) / 60
        
                res = {
                    'value': {
                        # Define a distancia entre as cidades e o tempo médio do percurso.
                        'distancia': distancia,
                        'tempo_viagem': tempoViagem
                }
                }
                # Return the values to update it in the view.
                return res
            
            
    def on_change_contrato(self, cr, user, ids, contrato, context=None):
        if contrato:
            obj_contrato = self.pool.get('account.analytic.account').browse(cr, user, contrato)
            return {'domain':{'tipo_servico':[('grupo_servico', '=', obj_contrato.grupo_servico.id)]}}

            
    def sincronizar_dados(self, cr, user, ids, context=None):
        agenda_tecnicos = self.pool.get('agenda_tecnicos').browse(cr, user, ids[0])
        
        if agenda_tecnicos.codigo_goon:
            chamado_goon = self.pool.get('chamado_goon').browse(cr, user, agenda_tecnicos.codigo_goon.id)
            retorno = chamado_goon.sincronizar_dados()
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            valores = {
                'tecnico': agenda_tecnicos.name.id,
                'agenda_tecnicos': agenda_tecnicos.id,
                'data': agenda_tecnicos.data,
                'observacao': agenda_tecnicos.atividade,
                'localidade': agenda_tecnicos.localidade.id,
                'tipo_servico': agenda_tecnicos.tipo_servico.id,
                'ocorrencia': agenda_tecnicos.ocorrencia.id,
                'status': 'DESP'
            }

            obj_chamado_goon = self.pool.get('chamado_goon').create(cr, user, valores, context)

            agenda_tecnicos.write({'codigo_goon': obj_chamado_goon})
            
            agenda_tecnicos.write({'status_goon': 'DESP'})
            
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }