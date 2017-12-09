# -*- coding: utf-8 -*-
##############################################################################
#
# OdooBro - odoobro.contact@gmail.com
#
##############################################################################

{
    'name': 'Ticket Management',
    'version': '1.0',
    'category': 'OdooBro Apps',
    'description': """
OdooBro - odoobro.contact@gmail.com
    """,
    'author': 'OdooBro Apps',
    'website': 'odoobro.com',
    'depends': [
        'project',
    ],
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        'security/ir.model.access.csv',
        

        # ============================================================
        # DATA
        # ============================================================
        # 'data/',

        # ============================================================
        # VIEWS
        # ============================================================
        'views/project_instance_view.xml',
        'views/project_internal_ticket_view.xml',
        'views/project_step_view.xml',
        'views/project_ticket_view.xml',
        'views/project_working_hour_view.xml',
        'views/res_users_view.xml',

        # ============================================================
        # MENU
        # ============================================================
        'menu/ticket_menu.xml',

        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
        # "data/projecttk_update_functions_data.xml",
    ],

    'test': [],
    'demo': [],

    'installable': True,
    'active': False,
    'application': True,
}
