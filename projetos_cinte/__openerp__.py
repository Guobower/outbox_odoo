#coding=utf-8

{
    'name': 'Projetos Cinte',
    'category': 'Uncategorized',
    'summary': 'Customizações do módulo de projetos para a Cinte',
    'version': '1.1',
    'description': "Customizações da empresa Cinte no módulo de projetos original do Odoo",
    'author': 'Edson Junior',
    'depends': ['base','project'],
    'installable': True,
    'data': [
        'views/report_dossie_viabilidade.xml',
        'views/project_licitados_kanban.xml',
        'views/project_licitados.xml',
        'views/project_internos_kanban.xml',
        'views/project_internos.xml',
        'views/ponto_interno_form.xml',
        'views/ponto_cliente_licitado_form.xml',
        'views/menu.xml',
        'dossie_viabilidade_report.xml'
    ]
}