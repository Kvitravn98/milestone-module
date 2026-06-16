from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):
    _inherit = "project.task"

    team_member_id = fields.Many2one(
        "project.team.member",
        string="Assignee",
        domain="[('project_id', '=', project_id), ('active', '=', True)]",
        ondelete="set null",
        help="Project team member assigned to this task.",
    )

    estimated_hours = fields.Float(
        string="Estimated Hours",
        default=0.0,
        help="Estimated effort required to complete this task, expressed in hours.",
    )

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

    @api.constrains("project_id", "team_member_id")
    def _check_team_member_belongs_to_project(self):
        for task in self:
            if (
                    task.team_member_id
                    and task.team_member_id.project_id != task.project_id
            ):
                raise ValidationError(
                    "The selected team member must belong to the same project as the task."
                )