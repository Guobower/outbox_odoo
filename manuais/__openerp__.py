#coding=utf-8

{
    'name': 'Manuais',
    'category': 'Uncategorized',
    'summary': 'Módulo para controle de manuais dos módulos e processos.',
    'version': '1.1',
    'description': "Módulo para controle de manuais dos módulos e processos.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/manuais_form.xml',
        'views/manuais_notificacoes.xml'
    ]
}