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
            obj_veiculo = self.pool.get('fleet.vehicle').browse(cr, uid, veiculo)
            if obj_veiculo.odometer >= odometro:
                res = {
                    'value': {
                        'active': False
                    }
                }
            else:
                res = {
                    'value': {
                        'active': True
                    }
                }
        else:
            res = {
                'value': {
                    'active': False
                }
            }
        
        return res