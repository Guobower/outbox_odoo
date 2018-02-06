#coding=utf-8

{
    'name': 'Recursos Humanos - Cinte',
    'category': 'Uncategorized',
    'summary': 'Módulo para recursos humanos da cinte.',
    'version': '1.1',
    'description': "Módulo para recursos humanos da cinte.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/trabalhe_conosco_tree.xml',
        'views/trabalhe_conosco_form.xml'
    ]
}