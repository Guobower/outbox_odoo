#coding=utf-8

{
    'name': 'Agenda de Técnicos',
    'category': 'Uncategorized',
    'summary': 'Agenda dos técnicos de campo da Cinte',
    'version': '1.1',
    'description': "Agenda dos técnicos de campo da Cinte",
    'author': 'Edson Junior',
    'depends': ['base','mail','contacts',"email_template"],
    'installable': True,
    'data': [
        'views/menu.xml',
        'views/agenda_tecnicos_form.xml',
        'views/agenda_tecnicos_calendar.xml',
        'views/agenda_tecnicos_search.xml',
        'views/agenda_tecnicos_tree.xml',
        'views/agenda_tecnicos_graph.xml',
        'views/email_template_solicitacao_visita_tecnica.xml',
        'security/agenda_tecnicos_security.xml'
    ]
}