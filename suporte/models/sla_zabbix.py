# -*- coding: utf-8 -*-
from openerp import api
from openerp import fields
from openerp import models

class Sla_zabbix(models.Model):
    _name = 'sla_zabbix'
    _description = 'SLA Zabbix'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Selection(
                            string="Servico",
                            selection=[('Ping', 'Latência')],
                            required=True,
                            track_visibility='onchange')
    
    contrato = fields.Many2one(
                               comodel_name='account.analytic.account',
                               string='Contrato',
                               required=True,
                               domain=[('tipo_contrato', '=', 3)],
                               help='Contrato a verificar',
                               track_visibility='onchange')
    
    host = fields.Many2many(
                            comodel_name='host',
                            string='Host',
                            required=True,
                            help='Host para visualização',
                            track_visibility='onchange')
    
    data_inicio = fields.Date(
                              string='Data de Inicio',
                              help='Data de Inicio',
                              required=True,
                              track_visibility='onchange')
    
    data_termino = fields.Date(
                               string='Data de Termino',
                               help='Data de Termino',
                               required=True,
                               track_visibility='onchange')

    def gerar_sla_backup(self, cr, user, ids, context=None):
        from zabbix_api import ZabbixAPI
        import time
        import datetime

        sla = self.pool.get('sla_zabbix').browse(cr, user, ids[0])

        time_inicio = time.mktime(datetime.datetime.strptime(sla.data_inicio, "%Y-%m-%d").timetuple())
        time_fim = time.mktime(datetime.datetime.strptime(sla.data_termino, "%Y-%m-%d").timetuple())

        server = 'http://10.10.200.217/zabbix/api_jsonrpc.php'
        username = 'Admin'
        password = 'zabbix'

        # Instanciando a API
        zapi = ZabbixAPI(server=server, path="", log_level=6)
        zapi.login(username, password)

        host_id = self.get_host_id(zapi, "3c4800g-CLIENTE-MPRN-Natal")

        itens_metrica = zapi.item.get({
            'output': ["itemid", "name", "hostid"],
            'hostids': host_id
        })

        trends = zapi.trend.get({
            "itemids": itens_metrica[0]["itemid"],
            "time_from": time_inicio,
            "time_till": time_fim,
            "output": ["value_avg"]
        })

    def get_host_id(self, zapi, host):
        # Obtendo uma lista com os hosts que já estão no zabbix
        hosts = zapi.host.get({
            "output": ["hostid"],
            "filter": {"host": host}
        })
        if hosts:
            return hosts[0]["hostid"]
        else:
            return 0

    def get_dias(self, cr, uid, data_inicio, data_termino, context=None):
        from datetime import datetime, timedelta
        data_inicio
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_termino = datetime.strptime(data_termino, '%Y-%m-%d')

        dias = []

        while data_inicio <= data_termino:
            dias.append(data_inicio)
            data_inicio = data_inicio + timedelta(days=1)

        return dias

    def gerar_sla(self, cr, user, data_inicio, host_name, context=None):
        from zabbix_api import ZabbixAPI
        import time
        import datetime
        from datetime import timedelta

        data_inicio = data_inicio + timedelta(hours=3)
        data_termino = data_inicio + timedelta(days=1)
        time_inicio = time.mktime(data_inicio.timetuple())

        time_fim = time.mktime(data_termino.timetuple())

        server = 'http://10.10.200.218/zabbix/api_jsonrpc.php'
        username = 'Admin'
        password = 'zabbix'

        # Instanciando a API
        zapi = ZabbixAPI(server=server, path="", log_level=6)
        zapi.login(username, password)

        host_id = self.get_host_id(zapi, host_name)

        if host_id:
            itens_metrica = zapi.item.get({
                'output': ["itemid", "name", "hostid"],
                'hostids': host_id
            })

            return self.get_resultado_sla(zapi, itens_metrica, time_inicio, time_fim)
        else:
            return "-"

    def get_resultado_sla(self, zapi, itens, time_inicio, time_fim):
        for item in itens:
            if item["name"].upper() == "LATENCIA":
                latencia = zapi.trend.get({
                    "itemids": item["itemid"],
                    "time_from": time_inicio,
                    "time_till": time_fim,
                    "output": ["value_avg"]
                })
            elif item["name"].upper() == "PERDA DE PACOTES":
                perda_pacotes = zapi.trend.get({
                    "itemids": item["itemid"],
                    "time_from": time_inicio,
                    "time_till": time_fim,
                    "output": ["value_avg"]
                })

        return str(self.calcular_media_diaria(latencia)) + " / " + str(self.calcular_media_diaria(perda_pacotes))

    def calcular_media_diaria(self, lista):
        resultado = 0

        if lista:
            for item in lista:
                resultado += float(item["value_avg"])
            return round(resultado/len(lista), 2)
        else:
            return 0
