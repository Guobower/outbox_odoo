#coding=utf-8

{
    'name': 'Almoxarifado - Cinte',
    'category': 'Uncategorized',
    'summary': 'Customizações do almoxarifado para a Cinte',
    'version': '1.1',
    'description': "Customizações do almoxarifado para a Cinte",
    'author': 'Edson Junior',
    'depends': ['base','account','stock'],
    'installable': True,
    'data': [
        'views/product_template_inherited.xml',
        'views/product_template_tree_inherited.xml',
        'wizard/stock_valuation_history_view.xml'
        #'views/product_template_graph.xml',
        #'views/menu.xml'
        #'wizard/stock_valuation_history_view.xml'
    ]
}