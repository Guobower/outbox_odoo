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
        'views/account_bank_statement_form.xml',
        'views/account_bank_statement_form2_inherited_infraestrutura.xml',
        'views/account_bank_statement_form2_inherited_tecnico.xml',
        'views/account_bank_statement_form2.xml',
        'views/account_move_line_tree.xml',
        'views/account_invoice_form.xml',
        'views/account_invoice_form_vencimentos.xml',
        'views/account_invoice_tree.xml',
        'views/report_recibo_caixa.xml',
        'views/report_extrato_caixa.xml',
        'views/report_entradas_caixa.xml',
        'views/report_saidas_caixa.xml',
        'views/report_recibo_nota_fiscal.xml',
        'security/account_bank_statement_security.xml',
        'views/natureza_financeira_form.xml',
        'views/natureza_financeira_tree.xml',
        'views/account_bank_statement_line_tree.xml',
        'views/account_bank_statement_line_graph.xml'
    ]
}