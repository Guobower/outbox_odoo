# -*- coding: utf-8 -*- © 2017 Carlos R. Silveira, ATSti
from openerp import api, fields, models


class AccountMoveLineInherited(models.Model):
    _inherit = 'account.move.line'
    
    name = fields.Char(
        required=False)

    @api.multi
    def action_payment_installment(self):
        compose_form = self.env.ref('view_move_installment_form', False)
        return {
            'view_mode': 'form',
            'view_id': compose_form,
            'res_model': 'account.move',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.move_id.id,
        }

