from odoo import fields, models
from odoo.exceptions import UserError

class ProjectCsvImportWizard(models.TransientModel):
    _name = "project.csv.import.wizard"
    _description = "Project Csv Import Wizard"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
    )

    csv_file = fields.Binary(
        string="CSV File",
        required=True,
        attachment=False,
    )

    import_milestones = fields.Boolean(
        string="Import Milestones",
        default=True,
    )

    filename = fields.Char(
        string="File Name",
    )

    import_team_members = fields.Boolean(
        string="Import Team Members",
        default=True,
    )


    def action_import_csv(self):
        self.ensure_one()

        if not self.import_milestones and not self.import_team_members:
            raise UserError("Please select at least one import option.")

        self._check_csv_file_extension()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Import CSV",
                "message": "Import wizard configured correctly.",
                "type": "success",
                "sticky": False,
            },
        }

    def _check_csv_file_extension(self):
        self.ensure_one()

        filename = (self.filename or "").lower().strip()

        if not filename.endswith(".csv"):
            raise UserError("Please upload a CSV file.")


