#coding=utf-8

{
    'name': 'Comercial - Cinte',
    'category': 'Sales',
    'summary': 'Customizações do CRM para o setor Comercial - Cinte',
    'version': '1.0',
    'description': "Customizações do CRM para o setor Comercial - Cinte",
    'author': 'Edson Junior',
    'depends': ['base','crm','mail','contacts',"email_template"],
    'installable': True,
    'data': [
        'views/crm_leads_licitados.xml',
        'views/crm_leads_licitados_kanban.xml',
        'views/crm_leads_form.xml',
        'views/crm_leads_form_oppor.xml',
        'views/email_template_vista_financeira.xml',
        'views/email_template_vista_certidoes.xml',
        'views/email_template_vista_objeto.xml',
        'views/email_template_vista_orgao.xml',
        'views/email_template_vista_restricoes.xml',
        'views/menu.xml'
    ]
}