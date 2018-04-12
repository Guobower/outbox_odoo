# -*- coding: utf-8 -*-
from openerp import models, fields

class Account_invoice_inherited(models.Model):
    _inherit = 'account.invoice' 

    def atualiza_campos(self, cr, uid, context=None):
        print "ENTREI PORRAAA, CADEEE"
        '''
        obj_faturas = self.pool.get('account.invoice').search(cr, uid, [('state','=','open'),('state','=','paid')]) 
        print "FATURAAAAS "+str(obj_faturas)
        for nota in obj_faturas:
            fatura = self.pool.get('account.invoice').browse(cr, uid, nota)
            for item in fatura.payment_ids:
                print "PAGAMENTOOOS "+str(pagamento)
                pagamento = self.pool.get('account.move.line').browse(cr, uid, item)
                pagamento.write({'centro_custo': fatura.x_centro_custo.id, 'natureza_financeira': fatura.x_natureza_financeira.id})
        '''