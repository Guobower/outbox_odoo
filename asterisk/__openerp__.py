#coding=utf-8

{
    'name': 'Asterisk - Cinte',
    'category': 'Uncategorized',
    'summary': 'Gerenciamento do Asterisk',
    'version': '1.0',
    'description': "Gestão das atividades do Asterisk.",
    'author': 'Edson Junior',
    'depends': ['base'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/asterisk_form.xml',
        'views/asterisk_tree.xml',
        'security/asterisk_security.xml'
    ]
}