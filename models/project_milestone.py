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