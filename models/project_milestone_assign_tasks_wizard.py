from odoo import fields, models
from odoo.exceptions import ValidationError


class ProjectMilestoneAssignTasksWizard(models.TransientModel):
    _name = "project.milestone.assign.tasks.wizard"
    _description = "Assign Existing Tasks to Milestone"

    milestone_id = fields.Many2one(
        "project.milestone",
        string="Milestone",
        required=True,
        readonly=True,
    )

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        readonly=True,
    )

    task_ids = fields.Many2many(
        "project.task",
        string="Tasks",
        domain="[('project_id', '=', project_id), '|', ('milestone_id', '=', False), ('milestone_id', '=', milestone_id)]",
    )

    def action_assign_tasks(self):
        self.ensure_one()

        if not self.task_ids:
            raise ValidationError("Please select at least one task.")

        invalid_tasks = self.task_ids.filtered(
            lambda task: task.project_id != self.project_id
        )

        if invalid_tasks:
            raise ValidationError(
                "All selected tasks must belong to the same project as the milestone."
            )

        self.task_ids.write(
            {
                "milestone_id": self.milestone_id.id,
            }
        )

        return {"type": "ir.actions.act_window_close"}