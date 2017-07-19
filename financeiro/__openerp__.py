#coding=utf-8

{
    'name': 'Financeiro Cinte',
    'category': 'Uncategorized',
    'summary': 'Customizações financeiras para a Cinte',
    'version': '1.1',
    'description': "Customizações financeiras para a Cinte",
    'author': 'Edson Junior',
    'depends': ['base','l10n_br_account_banking_payment_cnab'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/plano_contas_destino_form.xml',
        'views/plano_contas_destino_tree.xml',
        'views/account_account_form_inherited.xml',
        'views/account_bank_statement_form.xml'
    ]
}