#coding=utf-8

{
    'name': 'Suporte',
    'category': 'Uncategorized',
    'summary': 'Módulo customizado para o setor de suporte da Cinte.',
    'version': '1.1',
    'description': "Módulo customizado para o setor de suporte da Cinte.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts','account_analytic_analysis','l10n_br_hr'],
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
        'views/conexao_cliente_form.xml',
        'views/conexao_cliente_tree.xml',
        'views/conexao_cliente_search.xml',
        'views/adesao_form.xml',
        'views/adesao_tree.xml',
        'views/adesao_search.xml',
        'views/adesao_graph.xml',
        'views/report_contrato.xml',
        'views/report_adesao.xml',
        'views/account_analytic_account_form.xml',
        'views/account_analytic_account_graph.xml',
        'views/manifestacao_atendimento_form.xml',
        'views/manifestacao_atendimento_tree.xml',
        'views/grupo_atendimento_form.xml',
        'views/grupo_atendimento_tree.xml',
        'views/tipo_atendimento_form.xml',
        'views/tipo_atendimento_tree.xml',
        'views/atendimento_form.xml',
        'views/atendimento_kanban.xml',
        'views/atendimento_tree.xml',
        'views/atendimento_graph.xml',
        'views/status_atendimento_form.xml',
        'views/status_atendimento_tree.xml',
        'views/protocolo_sequencia.xml',
        'views/modo_contato_form.xml',
        'views/modo_contato_tree.xml'
    ]
}