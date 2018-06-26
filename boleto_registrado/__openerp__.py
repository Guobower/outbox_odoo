#coding=utf-8

{
    'name': 'Boletos Registrados',
    'category': 'Uncategorized',
    'summary': 'Emissao, retorno e impressao de boletos registrados',
    'version': '1.1',
    'description': "Emissao, retorno e impressao de boletos registrados ",
    'author': 'Edson Junior',
    'depends': ['base','manuais','financeiro'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/remessa_bancaria_form.xml',
        'views/account_invoice_form_inherited.xml',
        'views/retorno_bancario_form.xml',
        'views/res_partner_bank_form_inherited.xml'
    ]
}