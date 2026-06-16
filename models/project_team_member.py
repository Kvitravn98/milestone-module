from odoo import api, fields, models


class ProjectTeamMember(models.Model):
    _name = "project.team.member"
    _description = "Project Team Member"
    _rec_name = "display_name"

    display_name = fields.Char(
        string="Display Name",
        compute="_compute_display_name",
        store=True,
    )

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        ondelete="cascade",
    )

    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        ondelete="restrict",
    )

    role = fields.Selection(
        [
            ("team_lead", "Team Lead"),
            ("developer", "Developer"),
            ("tester", "Tester"),
            ("analyst", "Analyst"),
        ],
        string="Role",
        required=True,
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    task_ids = fields.One2many(
        "project.task",
        "team_member_id",
        string="Assigned Tasks",
    )

    task_count = fields.Integer(
        string="Assigned Tasks Count",
        compute="_compute_task_stats",
    )

    allocated_hours = fields.Float(
        string="Allocated Hours",
        compute="_compute_task_stats",
    )

    _sql_constraints = [
        (
            "unique_project_user",
            "unique(project_id, user_id)",
            "This user is already assigned to this project team.",
        )
    ]

    @api.depends("user_id", "project_id", "role")
    def _compute_display_name(self):
        for member in self:
            user_name = member.user_id.name or "Unknown User"
            project_name = member.project_id.name or "No Project"
            role = dict(member._fields["role"].selection).get(
                member.role,
                "No Role",
            )

            member.display_name = f"{user_name} - {project_name} ({role})"

    @api.depends("task_ids", "task_ids.estimated_hours")
    def _compute_task_stats(self):
        for member in self:
            member.task_count = len(member.task_ids)
            member.allocated_hours = sum(
                member.task_ids.mapped("estimated_hours")
            )