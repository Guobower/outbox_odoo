#coding=utf-8

{
    'name': 'Goon',
    'category': 'Uncategorized',
    'summary': 'Integracao com o Goon',
    'version': '1.0',
    'description': "Integracao do Odoo com o Goon",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts','agenda_tecnicos'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/tecnico_form.xml',
        'views/tecnico_tree.xml',
        'views/res_company_form_inherited.xml'
    ]
}