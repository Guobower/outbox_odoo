#coding=utf-8

{
    'name': 'Almoxarifado - Contrax',
    'category': 'Uncategorized',
    'summary': 'Customizações do almoxarifado para a Contrax',
    'version': '1.1',
    'description': "Customizações do almoxarifado para a Contrax",
    'author': 'Edson Junior',
    'depends': ['base','stock'],
    'installable': True,
    'data': [
        'views/stock_picking_inherited.xml',
        'views/stock_picking_graph.xml'
    ]
}