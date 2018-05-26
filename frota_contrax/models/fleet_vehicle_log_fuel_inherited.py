# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Fleet_vehicle_log_fuel_inherited(models.Model):
    _inherit = 'fleet.vehicle.log.fuel'
    
    active = fields.Boolean(
                            string="Validado",
                            help="Registro de combustível validado ou não, pode ser bloqueado devido a um registro de combustivel anterior com maior odometro do que o atual",
                            track_visibility='onchange'
                            )
    
    def on_change_odometro(self, cr, uid, ids, odometro, veiculo, context=None):
        if odometro and veiculo:
            obj_abastecimentos = self.pool.get('fleet.vehicle.log.fuel').search(cr, uid, [('odometer', '>', odometro), ('vehicle_id', '=', veiculo)])
            if len(obj_abastecimentos) > 0:
                '''
                res = {
                    'value': {
                        'active': False
                    }
                }
                '''
                res = {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Abastecimento não validado!' + str(len(obj_abastecimentos)),
                        'text': 'Abastecimento automaticamente validado.',
                        'sticky': True
                        }
                }
            else:
                res = {
                    'type': 'ir.actions.client',
                    'tag': 'action_warn',
                    'name': 'Warning',
                    'params': {
                        'title': 'Abastecimento Validado!' + str(len(obj_abastecimentos)),
                        'text': 'Abastecimento automaticamente validado.',
                        'sticky': True
                        }
                }
        else:
            res = {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Nem entrou!' + str(odometro),
                    'text': 'Abastecimento automaticamente validado.' + str(veiculo),
                    'sticky': True
                    }
            }
        
        return res