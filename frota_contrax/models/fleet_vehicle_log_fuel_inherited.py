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
    
    def on_change_odometro(self, cr, user, ids, odometro, veiculo, context=None):
        if odometro:
            obj_abastecimentos = self.pool.get('fleet.vehicle.log.fuel').search(cr, uid, [('odometer', '>', odometro), ('vehicle_id', '=', veiculo)])
            if len(obj_abastecimentos) > 0:
                res = {
                    'value': {
                        'active': False
                    }
                }
            else:
                res = {
                        'type': 'ir.actions.client',
                        'tag': 'action_warn',
                        'name': 'Warning',
                        'params': {
                            'title': 'Abastecimento Validado!',
                            'text': 'Abastecimento automaticamente validado.',
                            'sticky': False
                            }
                    }
            return res