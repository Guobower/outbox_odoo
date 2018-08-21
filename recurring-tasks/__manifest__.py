# -*- coding: utf-8 -*-
{
    'name': "recurring-tasks",

    'summary': """
        Tarefas recorrentes para o módulo de projetos""",

    'description': """
        Módulo para a criação de tarefas recorrentes dentro do módulo de projetos da OCA.
    """,

    'author': "Outbox Sistemas",
    'website': "http://www.outboxsistemas.com",
    'category': 'Project',
    'version': '1.0',
    'depends': ['base','project'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}