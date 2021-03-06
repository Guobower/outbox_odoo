# -*- coding: utf-8 -*-
from openerp import fields
from openerp import models

class Account_invoice_inherited(models.Model):
    _inherit = 'account.invoice' 

    def atualiza_campos(self, cr, uid, context=None):
        #obj_faturas = self.pool.get('account.invoice').search(cr, uid, [('state','=','open'),('state','=','paid')])
        obj_faturas = self.pool.get('account.invoice').search(cr, uid, [])
        for nota in obj_faturas:
            fatura = self.pool.get('account.invoice').browse(cr, uid, nota)
            for item in fatura.payment_ids:
                # pagamento = self.pool.get('account.move.line').browse(cr, uid, item)
                item.write({'centro_custo': fatura.x_centro_custo.id, 'natureza_financeira': fatura.x_natureza_financeira.id})