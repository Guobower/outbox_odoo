# -*- coding: utf-8 -*-

from openerp import api
from openerp import fields
from openerp import models

class Remessa_bancaria(models.Model):
    _name = 'remessa_bancaria'
    
    name = fields.Char(
                       string="Nome",
                       size=150,
                       required=True)
                       
    empresa = fields.Many2one(
                              string='Empresa Emitente',
                              help='Empresa emissora dos boletos',
                              comodel_name='res.company',
                              required=True)
    
    volume = fields.Selection(
                              selection=[(1, 1),
                              (2, 2),
                              (3, 3),
                              (4, 4),
                              (5, 5)],
                              string='Numero Sequencial',
                              help='Número sequencial do lote de remessa, iniciando-se em 1 diariamente',
                              required=True)
    
    faturas = fields.Many2many(
                               comodel_name='account.invoice',
                               string='Faturas de Clientes',
                               help='Selecione as faturas de clientes que farão parte desse lote')
    
    remessa_gerada = fields.Boolean(
                                    string="Remessa Gerada",
                                    help='Remessa já gerada no sistema')
    
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
            
            print 'FATURAAAS '+str(r)
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
                'nosso_numero':item.id,
                'numero_documento':item.id,
                'valor':item.amount_total,
                'razao_social':item.partner_id.legal_name,
                'cpf_cnpj_tipo':cpf_cnpj_tipo,
                'cpf_cnpj':item.partner_id.cnpj_cpf,
                'logradouro':item.partner_id.street,
                'bairro':item.partner_id.district,
                'cep':item.partner_id.zip,
                'cidade':item.partner_id.l10n_br_city_id.name,
                'uf':item.partner_id.state_id.code,
                'data_vencimento':item.date_due,
                'data_cadastro':item.date_invoice,
                'mensagem':item.comment
            }
            retorno.append(valores)
        
        return retorno