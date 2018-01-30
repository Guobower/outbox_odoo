#coding=utf-8

{
    'name': 'Redes',
    'category': 'Uncategorized',
    'summary': 'Módulo customizado para o setor de redes da Cinte.',
    'version': '1.1',
    'description': "Módulo customizado para o setor de redes da Cinte.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'security/redes_security.xml',
        'views/torre_tree.xml',
        'views/torre_form.xml',
        'views/torre_notificacoes.xml',
        'views/pop_tree.xml',
        'views/pop_form.xml',
        'views/pop_notificacoes.xml',
        'views/router_tree.xml',
        'views/router_form.xml',
        'views/checkagem_acesso_tree.xml',
        'views/checkagem_acesso_form.xml',
        'views/report_checkagem_acesso.xml',
        'views/router_search.xml',
        'views/router_notificacoes.xml'
    ]
}