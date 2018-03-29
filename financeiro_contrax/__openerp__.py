#coding=utf-8

{
    'name': 'Financeiro Contrax',
    'category': 'Uncategorized',
    'summary': 'Customizações financeiras para a Contrax',
    'version': '1.1',
    'description': "Customizações financeiras para a Contrax",
    'author': 'Edson Junior',
    'depends': ['base','account'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/centro_custo_form.xml',
        'views/centro_custo_tree.xml',
        'views/natureza_financeira_form.xml',
        'views/natureza_financeira_tree.xml',
        'data/schedule_atualiza_campos_relacao.xml'
    ]
}
