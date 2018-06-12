# -*- coding: utf-8 -*-

from openerp import api
from openerp import fields
from openerp import models

class Remessa_bancaria(models.Model):
    _name = 'remessa_bancaria'
    _description = 'Remessa bancaria para registro de boletos'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
                       string="Nome",
                       size=150,
                       required=True,
                       track_visibility='onchange')
                       
    empresa = fields.Many2one(
                              string='Empresa Emitente',
                              help='Empresa emissora dos boletos',
                              comodel_name='res.company',
                              required=True,
                              track_visibility='onchange')
    
    volume = fields.Selection(
                              selection=[(1, 1),
                              (2, 2),
                              (3, 3),
                              (4, 4),
                              (5, 5)],
                              string='Numero Sequencial',
                              help='Número sequencial do lote de remessa, iniciando-se em 1 diariamente',
                              required=True,
                              track_visibility='onchange')
    
    faturas = fields.Many2many(
                               comodel_name='account.invoice',
                               string='Faturas de Clientes',
                               help='Selecione as faturas de clientes que farão parte desse lote',
                               track_visibility='onchange')
    
    remessa_gerada = fields.Boolean(
                                    string="Remessa Gerada",
                                    help='Remessa já gerada no sistema',
                                    track_visibility='onchange')
    
    def gerar_remessa(self, cr, user, ids, context=None):
        import requests
        import base64
        import json
        
        obj_remessa = self.pool.get('remessa_bancaria').browse(cr, user, ids[0]) 
        
        if obj_remessa.remessa_gerada:
            return {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name': 'Warning',
                'params': {
                    'title': 'Remessa já gerada!',
                    'text': 'Verifique o anexo para baixar a remessa',
                    'sticky': True
                    }
            }
        else:
            faturas = json.JSONEncoder().encode(self.gerar_array_faturas(obj_remessa.faturas))

            r = requests.get('http://syncron.cinte.com.br/scriptOdoo/remessa_cnab/cintenet.php?faturas=' + str(faturas))
            
            attach_obj = self.pool.get('ir.attachment')
            context.update({'default_res_id': ids[0], 'default_res_model': 'remessa_bancaria'})
            
            print 'FATURAAAS ' + str(r)
            if r.json():
                for linha in r.json():
                    if linha["status"] == "Sucesso":
                        attach_id = attach_obj.create(cr, user, {'name': 'teste.REM',
                                                      'datas': base64.encodestring(linha["texto"]),
                                                      'datas_fname': 'teste.REM'}, context=context)
                        obj_remessa.write({'remessa_gerada':True})
                    else:
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'action_warn',
                            'name': 'Warning',
                            'params': {
                                'title': 'Erro ao gerar!',
                                'text': 'Contate o administrador do sistema',
                                'sticky': True
                                }
                        }

            pass
    
    
    def gerar_array_faturas(self, obj_faturas):
        retorno = list()
        
        for item in obj_faturas:
            if item.partner_id.is_company:
                cpf_cnpj_tipo = 'cnpj'
            else:
                cpf_cnpj_tipo = 'cpf'
            valores = {
                'nosso_numero':item.id
            }
            retorno.append(valores)
        
        return retorno
    
    def registrar_pagamentos(self, cr, user, ids, context=None):
        invoice = self.pool.get('account.invoice').browse(cr, user, 2241) 
        
        if not invoice.state == "open":
            return 
        
        payable_amount = 1 # The amount you want to pay
        
        voucher = self.pool.get("account.voucher").create(cr, user, {
                                                          "name": "",
                                                          "amount": payable_amount,
                                                          "journal_id": self.pool.get("account.journal").search(cr, user, [("type", "=", "bank")], limit=1)[0],
                                                          "account_id": invoice.partner_id.property_account_receivable.id,
                                                          "period_id": self.pool.get("account.voucher")._get_period(cr, user),
                                                          "partner_id": invoice.partner_id.id,
                                                          "type": "receipt"
                                                          }, context)
        
        print "voucheeer " + str(invoice.partner_id.property_account_receivable.id)
        voucher_obj = self.pool.get('account.voucher').browse(cr, user, voucher) 
        voucher_line = self.pool.get("account.voucher.line").create(cr, user, {
                                                                    "name": "",
                                                                    "payment_option": "without_writeoff",
                                                                    "amount": payable_amount,
                                                                    "voucher_id": voucher,
                                                                    "partner_id": invoice.partner_id.id,
                                                                    "account_id": invoice.partner_id.property_account_receivable.id,
                                                                    "type": "cr",
                                                                    "move_line_id": invoice.move_id.line_id[0].id,
                                                                    }, context)
        voucher_obj.signal_workflow("proforma_voucher")
        
        pass