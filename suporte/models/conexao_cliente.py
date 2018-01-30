# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Conexao_cliente(models.Model):
    _name = 'conexao_cliente'
    _description = 'Conexao de Clientes'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    name = fields.Char(
        string="Nome",
        size=250,
        required=True,
        track_visibility='onchange')
    
    descricao = fields.Text(
        string="Descricao",
        help="Descrição da Conexão",
        track_visibility="onchange")
    
    adesao = fields.Many2one(
        string="Adesao",
        comodel_name='adesao',
        help="Adesão a qual esta conexão está vinculada")
    
    pop_name = fields.Char('Nome do Pop', related='adesao.pop.name', store=True)
    
    id_pop = fields.Many2one(
        string="pop",
        comodel_name='pop')
    
    retorno_login = fields.Integer(
        string="Retorno de Login")
    
    mac_radio = fields.Char(
        string="MAC do Radio/ONU",
        help="MAC do Rádio do cliente",
        track_visibility="onchange")
    
    login = fields.Char(
        string="Login de Acesso",
        help="Login de acesso",
        track_visibility="onchange")
    
    senha = fields.Char(
        string="Senha de Acesso",
        help="Senha de acesso",
        track_visibility="onchange")
    
    router = fields.Many2one(
        string='Router',
        help='Router',
        comodel_name='router',
        track_visibility="onchange"
        )
    
    slot = fields.Integer(
        string="Slot",
        help="Slot",
        track_visibility="onchange")
    
    porta = fields.Integer(
        string="Porta",
        help="Porta",
        track_visibility="onchange")
    
    ontid = fields.Integer(
        string="Ontid",
        help="Ontid",
        track_visibility="onchange")
    
    service_port = fields.Integer(
        string="Service Port",
        help="Service Port",
        track_visibility="onchange")
    
    ont_srvprofile_id = fields.Integer(
        string="Ont Srvprofile Id",
        help="Ont Srvprofile Id",
        track_visibility="onchange")
    
    ont_lineprofile_id = fields.Integer(
        string="Ont Lineprofile Id",
        help="Ont Lineprofile Id",
        track_visibility="onchange")
    
    porta_onu_condominio = fields.Integer(
        string="Porta da ONU do Condomínio",
        help="Porta da ONU do condomínio",
        track_visibility="onchange")
    
    vlan = fields.Integer(
        string="VLAN",
        help="Vlan",
        track_visibility="onchange")
    
    index = fields.Integer(
        string="Index",
        help="Index",
        track_visibility="onchange")
    
    
    id_syncron = fields.Integer(
        string='ID no Syncron',
        help='ID de identificação no Syncron')
    
    
    def on_change_verificar_login(self, cr, user, ids, login, adesao, context=None):
        import requests
        
        if login:
            r = requests.get('http://syncron.cinte.com.br/adesoes/verificarLogin.php?login=' + login)
            if r.json() > 0:
                res = {
                     'value': {
                        'retorno_login': -1,
                        'name': 'Adesão ' + str(adesao)
                    }
                }
            else:
                res = {
                     'value': {
                        'retorno_login': 1,
                        'name': 'Adesão ' + str(adesao)
                    }
                }
            return res
    
    def find_slot_porta(self, cr, user, ids, context=None):
        import requests
        
        r = requests.get('http://syncron.cinte.com.br/index.php?proc=conexoesclientes&buscarSlotPorta&clrouter=110&mac=00-A1-02-01-8B-90')
        return {
            'type': 'ir.actions.client',
            'tag': 'action_warn',
            'name': 'Warning',
            'params': {
                'title': 'Não encontrado!',
                'text': 'Coordenadas não encontradas!'+str(r.json().decode('utf-8').replace('\0', ''))
                }
        }
        
        
    def on_change_case(self, cr, uid, ids, mac_radio, context=None):
        result = {'value': {
            'mac_radio': str(mac_radio).upper()
            }
        }
        return result