#coding=utf-8

{
    'name': 'Helpdesk',
    'category': 'Uncategorized',
    'summary': 'Módulo para suporte e atendimento de chamados.',
    'version': '1.1',
    'description': "Módulo para suporte e atendimento de chamados.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/helpdesk_kanban.xml',
        'views/helpdesk_tree.xml',
        'views/helpdesk_form.xml',
        'views/helpdesk_graph.xml',
        'views/helpdesk_notificacoes.xml',
        'security/helpdesk_security.xml',
        'data/schedule_pausa.xml',
        'data/schedule_verifica_atrasos.xml'
    ]
}