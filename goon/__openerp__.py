#coding=utf-8

{
    'name': 'Goon',
    'category': 'Uncategorized',
    'summary': 'Integracao com o Goon',
    'version': '1.0',
    'description': "Integracao do Odoo com o Goon",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/tecnico_form.xml',
        'views/tecnico_tree.xml',
        'views/res_company_form_inherited.xml',
        'views/tipo_servico_form.xml',
        'views/tipo_servico_tree.xml',
        'views/chamado_goon_form.xml'
    ]
}