# -*- coding: utf-8 -*-
"""
Módulo Agenda de Projetos responsável pelo registro da agenda de projetistas da Cinte.
"""

__author__ = "Edson de Lima Cosme Junior"
__copyright__ = "Copyright 2017, Edson Junior"
__credits__ = ["equipe de desenvolvimento Cinte"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Edson de Lima Cosme Junior"
__email__ = "edson.junior@outboxsistemas.com"
__status__ = "Production"

import simplejson, urllib

from openerp import models, fields, api


class Agenda_projetos(models.Model):
    """
    Classe Agenda de Projetos define os atributos e métodos necessários para o registro da agenda de projetistas da Cinte.
    
    Define a atividade a ser desenvolvida e em qual data será executada, além de prover campos necessários para indicadores
    gerenciais, como as cidades de origem e destino, tempo e distância percorrida. Possui também integração com o almoxarifado
    para registro do material retirado para execução da atividade e o que foi retornado após a conclusão.
    """
    _name = 'agenda_projetos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(
        string="Nome",
        size=150,
        required=True,
        track_visibility='onchange')

    atividade = fields.Text(
        string='Atividade',
        help='Atividade a ser desenvolvida pela equipe',
        track_visibility='onchange')

    cidade_destino = fields.Many2one(
        string='Cidade de Destino',
        help='Cidade de destino final dos projetistas',
        comodel_name='l10n_br_base.city',
        domain=['|', ('state_id', '=', 70), ('state_id', '=', 72)],
        track_visibility='onchange')

    cidade_origem = fields.Many2one(
        string='Cidade de Origem',
        help='Cidade de origem dos projetistas',
        comodel_name='l10n_br_base.city',
        domain=['|', ('state_id', '=', 70), ('state_id', '=', 72)],
        track_visibility='onchange')

    cliente_nome = fields.Char(
        string='Cliente',
        size=200,
        help='Nome do cliente',
        track_visibility='onchange')

    data = fields.Datetime(
        string='Data de Início',
        help='Data de início da atividade',
        track_visibility='onchange')

    data_termino = fields.Datetime(
        string='Data de Término',
        help='Data de término da atividade',
        track_visibility='onchange')

    distancia = fields.Float(
        string='Distância (km)',
        help='Distância percorrida entre a cidade de origem e a de destino do atendimento',
        track_visibility='onchange')

    equipe = fields.Many2many(
        comodel_name='res.users',
        string='Equipe',
        help='Equipe envolvida na atividade',
        track_visibility='onchange')

    observacoes = fields.Text(
        string='Observações',
        help='Adicione observações sobre o andamento da atividade',
        track_visibility='onchange')

    status = fields.Selection(
        selection=[('pendente', 'Pendente'),
                   ('concluido', 'Concluída'),
                   ('cancelada', 'Cancelada')],
        string='Status',
        help='Status da atividade',
        track_visibility='onchange')

    tempo_viagem = fields.Float(
        string='Tempo de Viagem (minutos)',
        help='Tempo médio do percurso entre a cidade de origem e de destino',
        track_visibility='onchange')

    tipo_cliente = fields.Selection(
        selection=[('bandaLarga', 'Banda Larga'),
                   ('licitado', 'Licitado'),
                   ('linkPuro', 'Link Puro'),
                   ('backbone', 'Backbone'),
                   ('atividadesInternas', 'Atividades Internas')],
        string='Tipo de Cliente',
        help='Tipo do cliente da atividade',
        track_visibility='onchange')

    veiculo = fields.Many2one(
        string='Veículo',
        help='Veículo utilizado na atividade',
        comodel_name='fleet.vehicle',
        track_visibility='onchange')

    color = fields.Integer(
        string="Color Index")

    responsavel = fields.Many2one(
        comodel_name='res.users',
        string='Responsável',
        help='Responsável pela atividade',
        track_visibility='onchange')

    retirada_almoxarifado = fields.Many2one(
        string='Retirada do Almoxarifado',
        help='Retirada de materiais para uso na atividade',
        comodel_name='stock.picking',
        track_visibility='onchange')

    devolucao_almoxarifado = fields.Many2one(
        string='Devolucao de Materiais',
        help='Devolução de materiais não usados ou recolhidos na atividade',
        comodel_name='stock.picking',
        track_visibility='onchange')

    def on_change_cidade(self, cr, user, ids, cidade_origem, cidade_destino, context=None):
        """
        Função onchange para as cidades no formulário.

        Recebe a cidade de origem e destino adicionadas ao formulário, caso ambas estejam preenchidas utiliza a API do
        Google Maps para buscar a distância e o tempo de percurso entre as cidades e atualiza no formulário os dados
        calculados na consulta.

        :param cr: Cursor da base de dados.
        :param user: Usuário logado.
        :param ids: IDs das instâncias da classe.
        :param cidade_origem: Cidade de origem definida no formulário.
        :param cidade_destino: Cidade de destino definida no formulário.
        :param context: Contexto da aplicação. Default None
        :return: Retorna o par distância/tempo de viagem e atualiza os campos do formulário
        """
        if cidade_origem and cidade_destino:
            origem = self.pool.get('l10n_br_base.city').browse(cr, user, cidade_origem)
            destino = self.pool.get('l10n_br_base.city').browse(cr, user, cidade_destino)

            url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origem.name + "," + origem.state_id.name + "&destinations=" + destino.name + "," + destino.state_id.name + "&key=AIzaSyDYRUAfCeT3uwCqZzvVoGv1QqRIAL0h5dk"
            url = url.encode('utf-8')
            result = simplejson.load(urllib.urlopen(url))

            distancia = (result['rows'][0]['elements'][0]['distance']['value']) / 1000
            tempo_viagem = (result['rows'][0]['elements'][0]['duration']['value']) / 60

            res = {
                'value': {
                    'distancia': distancia,
                    'tempo_viagem': tempo_viagem
                }
            }
            return res
