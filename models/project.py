from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    team_member_ids = fields.One2many(
        "project.team.member",
        "project_id",
        string="Team Members",
    )

    custom_milestone_count = fields.Integer(
        string="Milestone Count",
        compute="_compute_custom_milestone_progress",
        store=True,
    )

    custom_completed_milestone_count = fields.Integer(
        string="Completed Milestones",
        compute="_compute_custom_milestone_progress",
        store=True,
    )

    custom_milestone_progress = fields.Float(
        string="Milestone Progress",
        compute="_compute_custom_milestone_progress",
        store=True,
    )

    def _is_custom_milestone_completed(self, milestone):
        return milestone.state == "done"

    def _count_custom_completed_milestones(self, milestones):
        completed = 0

        for milestone in milestones:
            if self._is_custom_milestone_completed(milestone):
                completed += 1

        return completed

    @api.depends("milestone_ids", "milestone_ids.state")
    def _compute_custom_milestone_progress(self):
        for project in self:
            milestones = project.milestone_ids

            total = len(milestones)
            completed = project._count_custom_completed_milestones(milestones)

            project.custom_milestone_count = total
            project.custom_completed_milestone_count = completed
            project.custom_milestone_progress = (
                completed / total * 100 if total else 0
            )