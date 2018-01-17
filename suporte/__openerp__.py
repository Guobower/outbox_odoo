#coding=utf-8

{
    'name': 'Suporte',
    'category': 'Uncategorized',
    'summary': 'Módulo customizado para o setor de suporte da Cinte.',
    'version': '1.1',
    'description': "Módulo customizado para o setor de suporte da Cinte.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts','account_analytic_analysis'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'security/suporte_security.xml',
        'views/res_partner_notificacoes.xml',
        'views/res_partner_form_inherited.xml',
        'views/status_contrato_form.xml',
        'views/status_contrato_notificacoes.xml',
        'views/status_contrato_tree.xml',
        'views/status_adesao_form.xml',
        'views/status_adesao_notificacoes.xml',
        'views/status_adesao_tree.xml',
        'views/plano_form.xml',
        'views/plano_notificacoes.xml',
        'views/plano_tree.xml',
        'views/grupo_servico_form.xml',
        'views/grupo_servico_notificacoes.xml',
        'views/grupo_servico_tree.xml',
        'views/modo_aquisicao_form.xml',
        'views/modo_aquisicao_notificacoes.xml',
        'views/modo_aquisicao_tree.xml',
        'views/account_analytic_account_form.xml'
    ]
}