# -*- coding: utf-8 -*-
import simplejson, urllib

from openerp import models, fields, api

class Agenda_projetos(models.Model):
    _name = 'agenda_projetos'
    
    name = fields.Char(
        string="Nome",
        size=150,
        required=True)
    
    atividade = fields.Text(
        string='Atividade',
        help='Atividade a ser desenvolvida pela equipe')
    
    cidade_destino = fields.Many2one(
        string='Cidade de Destino',
        help='Cidade de destino final dos projetistas',
        comodel_name='l10n_br_base.city',
        domain=['|',('state_id', '=', 70),('state_id', '=', 72)])
    
    cidade_origem = fields.Many2one(
        string='Cidade de Origem',
        help='Cidade de origem dos projetistas',
        comodel_name='l10n_br_base.city',
        domain=['|',('state_id', '=', 70),('state_id', '=', 72)])

    cliente_nome = fields.Char(
        string='Cliente',
        size=200,
        help='Nome do cliente')
    
    data = fields.Datetime(
        string='Data de Início',
        help='Data de início da atividade')
    
    data_termino = fields.Datetime(
        string='Data de Término',
        help='Data de término da atividade')
    
    distancia = fields.Float(
        string='Distância (km)',
        help='Distância percorrida entre a cidade de origem e a de destino do atendimento')
    
    equipe = fields.Many2many(
        comodel_name='res.users',
        string='Equipe',
        help='Equipe envolvida na atividade')
    
    observacoes = fields.Text(
        string='Observações',
        help='Adicione observações sobre o andamento da atividade')
    
    status = fields.Selection(
        selection=[('pendente', 'Pendente'),
                   ('concluido', 'Concluída'),
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
    
    veiculo = fields.Many2one(
        string='Veículo',
        help='Veículo utilizado na atividade',
        comodel_name='fleet.vehicle')
    
    color = fields.Integer(
        string="Color Index")
    
    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável pela atividade')
    
    def on_change_cidade(self, cr, user, ids, cidadeOrigem, cidadeDestino, context=None):
        if cidadeOrigem:
            if cidadeDestino:
                origem = self.pool.get('l10n_br_base.city').browse(cr, user, cidadeOrigem)
                destino = self.pool.get('l10n_br_base.city').browse(cr, user, cidadeDestino)
        
                url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origem.name + ","+origem.state_id.name+"&destinations=" + destino.name + ","+destino.state_id.name+"&key=AIzaSyDYRUAfCeT3uwCqZzvVoGv1QqRIAL0h5dk"
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