{
    'name': "Milestones Module",
    "version": "18.0.1.0.0",
    'summary': """Modulo per la gestione delle milestones di progetti.""",
    'description': """Il modulo è un'estensione del modulo Projects. Permette la gestione delle milestones e dei relativi task.""",
    'author': "Armando Colone",
    "category": "Project",
    "depends": ["project"],
    'sequence': 1,
    'data': [
        "security/ir.model.access.csv",
        "views/project_team_member_views.xml",
        "views/project_milestone_views.xml",
        "views/project_milestone_assign_tasks_wizard_views.xml",
    ],
    'application': True,
    'installable': True,
    'license': "LGPL-3"
}
