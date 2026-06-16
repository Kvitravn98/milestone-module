from odoo import fields, models


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    deadline = fields.Date(
        string="Deadline",
        required=True,
        tracking=True,
        copy=False,
    )

    state = fields.Selection(
        [
            ("todo", "To Do"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        string="Status",
        default="todo",
        required=True,
        tracking=True,
        copy=False,
    )

    _sql_constraints = [
        (
            "unique_project_milestone_name",
            "unique(project_id, name)",
            "A milestone with this name already exists for this project.",
        )
    ]

    def action_open_assign_tasks_wizard(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Assign Existing Tasks",
            "res_model": "project.milestone.assign.tasks.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_milestone_id": self.id,
                "default_project_id": self.project_id.id,
            },
        }