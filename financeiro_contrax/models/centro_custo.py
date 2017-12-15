# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Centro_custo(models.Model):
    _name = 'centro_custo'
    
    name = fields.Char(
        string="Name",
        size=250,
        required=True)
    
    nome = fields.Char(
        string="Nome",
        size=250,
        required=True)
    
    codigo = fields.Char(
        string="Código",
        size=250,
        required=True)
    
    reduzido = fields.Char(
        string="Reduzido",
        size=250,
        required=True)
    
    
    def on_change_codigo_nome(self, cr, user, ids, codigo, nome, context=None):
        res = {
             'value': {
                # Define a distancia entre as cidades e o tempo médio do percurso.
                'name': str(codigo)+" - "+str(nome)
            }
        }
        # Return the values to update it in the view.
        return res
