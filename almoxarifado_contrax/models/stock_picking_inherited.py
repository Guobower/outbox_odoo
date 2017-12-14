# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime, timedelta

class Stock_picking_inherited(models.Model):
    _inherit = 'stock.picking'
        
    tipo_material = fields.Selection(
        selection=[('epi_epc', 'EPIs/EPCs'), 
                   ('consumo_obra', 'Consumo de Obra'), 
                   ('material_aplicacao', 'Material de Aplicação'), 
                   ('ferramentas_equipamentos_producao', 'Ferramentas e Equipamentos de Produção'), 
                   ('equipamentos_escritorio_moveis_utensilios', 'Equipamentos de Escritório, Móveis e Utensílios'), 
                   ('material_expediente_limpeza_primeiros_socorros', 'Material de Expediente, Limpeza e Primeiros Socorros')],
        string='Tipo de Material',
        required=True,
        help='Informe o tipo de material solicitado')
    
    prioridade_solicitacao = fields.Selection(
        selection=[('normal', 'Normal'), 
                   ('urgente', 'Urgente'), 
                   ('emergencial', 'Emergencial')],
        string='Prioridade da Solicitação',
        help='Prioridade da solicitação com base no prazo para entrega')
    
    
    
    def on_change_data_programada(self, cr, user, ids, data_programada, context=None):
        prioridade = 'normal'
        
        data_pedido = datetime.now()
        
        if data_programada:
            data_prazo = datetime.strptime(data_programada, '%Y-%m-%d %H:%M:%S')
            
            prazo = abs((data_prazo - data_pedido).days)
            
            if prazo <= 1:
                prioridade = 'emergencial'
            if prazo > 1 and prazo < 5:
                prioridade = 'urgente'
            if prazo >= 5:
                prioridade = 'normal'
                
            res = {
                 'value': {
                    'prioridade_solicitacao': prioridade,
                    'origin': prazo
                }
            }
            # Return the values to update it in the view.
            return res
        else:
            res = {
                 'value': {
                    'prioridade_solicitacao': '',
                    'origin': 0
                }
            }
            # Return the values to update it in the view.
            return res
            
