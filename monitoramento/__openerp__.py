#coding=utf-8

{
    'name': 'Monitoramento',
    'category': 'Uncategorized',
    'summary': 'Módulo para monitoramento de problemas.',
    'version': '1.1',
    'description': "Módulo para monitoramento de problemas.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts','redes','suporte'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/monitoramento_kanban.xml',
        'views/monitoramento_tree.xml',
        'views/monitoramento_form.xml',
        'views/monitoramento_graph.xml',
        'security/monitoramento_security.xml'
    ]
}