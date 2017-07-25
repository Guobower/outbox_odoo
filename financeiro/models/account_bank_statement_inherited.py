# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Account_bank_statement_inherited(models.Model):
    _inherit = 'account.bank.statement'
    
    def exportar_conciliacao(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        assert len(ids) == 1, "Only one ID accepted"
        
        model_obj = self.pool.get('account.bank.statement')  # the model of record you want file attached
        record_obj = model_obj.browse(cr, uid, ids[0])  # actual record to wich you attach file
        
        self.gerar_arquivo_exportacao(cr, uid, ids, model_obj, record_obj, context)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Arquivos Gerados!',
                'text': 'Arquivos gerados com sucesso, confira nos anexos do documento.',
                'sticky': True
                }
         }
        
    # Método para gerar arquivo de exportação
    def gerar_arquivo_exportacao(self, cr, uid, ids, model_obj, record_obj, context):
        import base64
        
        # Gerando nome do arquivo
        file_name = record_obj.name + '.txt'
        
        modelo_diario = self.pool.get('account.move.line')  # the model of record you want file attached
        lancamentos_diario = modelo_diario.search(cr, uid, [('statement_id', '=', record_obj.id)])
        
        # txt_content = txt_content + "|6100|17/07/2017|58|5|1,00|1|REGISTRO DE TESTE||||\n"
        # txt_content = txt_content + "|6100|17/07/2017|58|5|3,00|1|REGISTRO DE TESTE 2||||"
        
        txt_content = ""
        for item in lancamentos_diario:
            linha_obj = modelo_diario.browse(cr, uid, item)
            conciliacao = modelo_diario.search(cr, uid, [('move_id', '=', linha_obj.move_id.id)])
            
            for item_conciliados in conciliacao:
                if item_conciliados != item:
                    linha_conciliada = modelo_diario.browse(cr, uid, item_conciliados)
            
            if linha_obj.credit > 0:
                if linha_conciliada.debit > 0:
                    if linha_obj.id < linha_conciliada.id:
                        data_real = str(linha_obj.date).split("-")
                        string_data_real = data_real[2] + "/" + data_real[1] + "/" + data_real[0]
                        # Gerando dados do arquivo
                        txt_content = txt_content + "|0000|08378641000196|\n"
                        txt_content = txt_content + "|6000|X||||\n"
                        txt_content = txt_content + "|6100|" + string_data_real + "|" + str(linha_conciliada.account_id.de_para.reduzido) + "|" + str(linha_obj.account_id.de_para.reduzido) + "|" + str('%.2f' % (linha_obj.credit)).replace(".", ",") + "|1|" + str(linha_obj.name) + "||||\n"
            
            if linha_obj.debit > 0:
                if linha_conciliada.credit > 0:
                    if linha_obj.id < linha_conciliada.id:
                        data_real = str(linha_obj.date).split("-")
                        string_data_real = data_real[2] + "/" + data_real[1] + "/" + data_real[0]
                        # Gerando dados do arquivo
                        txt_content = txt_content + "|0000|08378641000196|\n"
                        txt_content = txt_content + "|6000|X||||\n"
                        txt_content = txt_content + "|6100|" + string_data_real + "|" + str(linha_conciliada.account_id.de_para.reduzido) + "|" + str(linha_obj.account_id.de_para.reduzido) + "|" + str('%.2f' % (linha_obj.debit)).replace(".", ",") + "|1|" + str(linha_obj.name) + "||||\n"
            
            
            
            # txt_content = txt_content + "|6100|"+str(linha_obj.date)+"|58|5|"+str(linha_obj.credit)+"|1|"+str(linha_obj.name)+"||||\n"
            # txt_content = txt_content + ""+str(item)+"\n"
        
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        
        context.update({'default_res_id': ids[0], 'default_res_model': 'account.bank.statement'})

        attach_id = attach_obj.create(cr, uid, {'name': attach_name,
                                                'datas': base64.encodestring(txt_content),
                                                'datas_fname': file_name}, context=context)
        
        return attach_id
    
    
    def gerar_recibo(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Warning!',
                'text': 'Entered Quantity is greater than quantity on source.',
                'sticky': True
                }
         }
        #if ids:
        #    if not isinstance(ids, list):
        #        ids = [ids]
        #    context = dict(context or {}, active_ids=ids, active_model=self._name)
        #return {
        #    'type': 'ir.actions.report.xml',
        #    'report_name': 'mrp.products_consume_document',
        #    'context': context,
        #}