#coding=utf-8

{
    'name': 'Almoxarifado - Cinte',
    'category': 'Uncategorized',
    'summary': 'Customizações do almoxarifado para a Cinte',
    'version': '1.1',
    'description': "Customizações do almoxarifado para a Cinte",
    'author': 'Edson Junior',
    'depends': ['base','account'],
    'installable': True,
    'data': [
        'views/product_template_inherited.xml',
        'views/product_template_tree_inherited.xml'
    ]
}