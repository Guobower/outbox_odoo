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
        # Buscando o modelo de lançamentos de diário contábil
        modelo_diario = self.pool.get('account.move.line')
        # Buscando os lançamentos de diário do referido extrato
        lancamentos_diario = modelo_diario.search(cr, uid, [('statement_id', '=', record_obj.id)])
        # String que irá alimentar o arquivo de importação
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
                        txt_content = txt_content + "|6100|" + string_data_real + "|" + str(linha_conciliada.account_id.de_para.reduzido) + "|" + str(linha_obj.account_id.de_para.reduzido) + "|" + str('%.2f' % (linha_obj.credit)).replace(".", ",") + "|1|" + str(linha_obj.name.encode('ascii', 'ignore').decode('ascii')) + "||||\n"
            
            if linha_obj.debit > 0:
                if linha_conciliada.credit > 0:
                    if linha_obj.id < linha_conciliada.id:
                        data_real = str(linha_obj.date).split("-")
                        string_data_real = data_real[2] + "/" + data_real[1] + "/" + data_real[0]
                        # Gerando dados do arquivo
                        txt_content = txt_content + "|0000|08378641000196|\n"
                        txt_content = txt_content + "|6000|X||||\n"
                        txt_content = txt_content + "|6100|" + string_data_real + "|" + str(linha_obj.account_id.de_para.reduzido) + "|" + str(linha_conciliada.account_id.de_para.reduzido) + "|" + str('%.2f' % (linha_obj.debit)).replace(".", ",") + "|1|" + str(linha_obj.name.encode('ascii', 'ignore').decode('ascii')) + "||||\n"
            
            
            
            # txt_content = txt_content + "|6100|"+str(linha_obj.date)+"|58|5|"+str(linha_obj.credit)+"|1|"+str(linha_obj.name)+"||||\n"
            # txt_content = txt_content + ""+str(item)+"\n"
        
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        
        context.update({'default_res_id': ids[0], 'default_res_model': 'account.bank.statement'})

        attach_id = attach_obj.create(cr, uid, {'name': attach_name,
                                                'datas': base64.encodestring(txt_content),
                                                'datas_fname': file_name}, context=context)
        
        return attach_id