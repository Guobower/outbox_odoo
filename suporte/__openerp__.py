#coding=utf-8

{
    'name': 'Suporte',
    'category': 'Uncategorized',
    'summary': 'Módulo customizado para o setor de suporte da Cinte.',
    'version': '1.1',
    'description': "Módulo customizado para o setor de suporte da Cinte.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'security/suporte_security.xml',
        'views/res_partner_notificacoes.xml',
        'views/res_partner_form_inherited.xml',
        'views/status_contrato_form.xml',
        'views/status_contrato_notificacoes.xml',
        'views/status_contrato_tree.xml',
        'views/account_analytic_account_form.xml'
    ]
}