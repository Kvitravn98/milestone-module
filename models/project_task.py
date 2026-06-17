from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):
    _inherit = "project.task"

    estimated_hours = fields.Float(
        string="Estimated Hours",
        default=0.0,
        help="Estimated effort required to complete this task, expressed in hours.",
    )

    def action_remove_from_milestone(self):
        for task in self:
            task.milestone_id = False

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    @api.constrains("estimated_hours")
    def _check_estimated_hours(self):
        for task in self:
            if task.estimated_hours < 0:
                raise ValidationError("Estimated hours cannot be negative.")

    @api.constrains("project_id", "milestone_id")
    def _check_milestone_belongs_to_project(self):
        for task in self:
            if task.milestone_id and task.milestone_id.project_id != task.project_id:
                raise ValidationError(
                    "The selected milestone must belong to the same project as the task."
                )