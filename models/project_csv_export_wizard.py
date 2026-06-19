from odoo import fields, models

class ProjectCsvExportWizard(models.TransientModel):
    _name = "project.csv.export.wizard"
    _description = "Project Csv Export Wizard"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
    )

    export_milestones = fields.Boolean()
    export_team_members = fields.Boolean()
    export_tasks = fields.Boolean()

    def action_export_wizard(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "url": f"/milestones_module/export_project_csv?project_id={self.project_id.id}&export_milestones={self.export_milestones}&export_team_members={self.export_team_members}&export_tasks={self.export_tasks}",
            "target": "download",
        }
