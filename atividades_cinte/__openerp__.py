#coding=utf-8

{
    'name': 'Atividades dos setores - Cinte',
    'category': 'Uncategorized',
    'summary': 'Atividades de funcionários e setores Cinte',
    'version': '1.0',
    'description': "Gestão de atividades individuais e de setores da Cinte para maior controle dos processos dos setores.",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts',"email_template"],
    'installable': True,
    'data': [
        'atividades_cinte_report.xml',
        'views/report_atividades_cinte.xml',
        'views/menu.xml',
        'views/atividades_cinte_kanban.xml',
        'views/atividades_cinte_form.xml',
        'views/atividades_cinte_calendar.xml',
        'views/atividades_cinte_search.xml',
        'views/atividades_cinte_tree.xml',
        'views/atividades_cinte_graph.xml',
        'views/atividades_cinte_notificacoes.xml',
        'views/email_template_aviso_conclusao.xml',
        'security/atividades_cinte_security.xml',
        'security/ir.rule.xml'
    ]
}