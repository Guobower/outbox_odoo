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
        'views/torre_tree.xml',
        'views/torre_form.xml',
        'views/torre_notificacoes.xml',
        'security/redes_security.xml'
    ]
}