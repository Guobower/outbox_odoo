#coding=utf-8

{
    'name': 'Agenda de Projetos',
    'category': 'Uncategorized',
    'summary': 'Agenda dos projetistas da Cinte',
    'version': '1.1',
    'description': "Agenda dos projetistas da Cinte",
    'author': 'Edson Junior',
    'depends': ['base'],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/agenda_projetos_form.xml',
        'views/agenda_projetos_calendar.xml',
        'views/agenda_projetos_search.xml',
        'views/agenda_projetos_tree.xml',
        'views/agenda_projetos_graph.xml',
        'views/agenda_projetos_kanban.xml',
        'security/agenda_projetos_security.xml'
    ]
}