from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    team_member_ids = fields.One2many(
        "project.team.member",
        "project_id",
        string="Team Members",
    )

    milestone_count = fields.Integer(
        string="Milestone Count",
        compute="_compute_milestone_progress",
        store=True,
    )

    completed_milestone_count = fields.Integer(
        string="Completed Milestones",
        compute="_compute_milestone_progress",
        store=True,
    )

    milestone_progress = fields.Float(
        string="Milestone Progress",
        compute="_compute_milestone_progress",
        store=True,
    )

    def _is_milestone_completed(self, milestone):
        return milestone.state == "done"

    def _count_completed_milestones(self, milestones):
        completed = 0

        for milestone in milestones:
            if self._is_milestone_completed(milestone):
                completed += 1

        return completed

    @api.depends("milestone_ids", "milestone_ids.state")
    def _compute_milestone_progress(self):
        for project in self:
            milestones = project.milestone_ids

            total = len(milestones)
            completed = project._count_completed_milestones(milestones)

            project.milestone_count = total
            project.completed_milestone_count = completed
            project.milestone_progress = (
                completed / total * 100 if total else 0
            )