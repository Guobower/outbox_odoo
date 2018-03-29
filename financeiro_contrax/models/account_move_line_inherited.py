# -*- coding: utf-8 -*- © 2017 Carlos R. Silveira, ATSti
from openerp import api
from openerp import fields
from openerp import models


class AccountMoveLineInherited(models.Model):
    _inherit = 'account.move.line'
    
    name = fields.Char(
                       required=False)
        
    centro_custo_name = fields.Char('Centro de Custo', related='invoice.x_centro_custo.name', store=True)
    
    natureza_financeira_name = fields.Char('Natureza Financeira', related='invoice.x_natureza_financeira.name', store=True)
    
    tipo_documento_name = fields.Char('Tipo de Documento', related='invoice.fiscal_document_id.name', store=True)
    
    centro_custo = fields.Many2one(
                              string='Centro de Custo',
                              help='Centro de Custo do vencimento',
                              comodel_name='x_centro_custo',
                              required=True)
                              
    natureza_financeira = fields.Many2one(
                              string='Natureza Financeira',
                              help='Natureza Financeira do vencimento',
                              comodel_name='x_natureza_financeira',
                              required=True)
    
    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(AccountMoveLineInherited, self).create(values)
        
        vencimento = self.pool.get('account.move.line').browse(self.env.cr, self.env.uid, record['id'])
        
        vencimento.write({'centro_custo': vencimento.invoice.x_centro_custo.id, 'natureza_financeira': vencimento.invoice.x_natureza_financeira.id})
        # Return the record so that the changes are applied and everything is stored.
	return record
    
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

