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

    task_ids = fields.Many2many(
        "project.task",
        string="Assigned Tasks",
        compute="_compute_task_stats",
    )

    task_count = fields.Integer(
        string="Assigned Tasks Count",
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
            role = dict(member._fields["role"].selection).get(member.role, "No Role")

            member.display_name = f"{user_name} - {project_name} ({role})"

    @api.depends("project_id", "user_id")
    def _compute_task_stats(self):
        ProjectTask = self.env["project.task"]

        empty_tasks = ProjectTask.browse()
        valid_members = self.filtered(lambda member: member.project_id and member.user_id)

        tasks_by_member_key = {}

        member_keys = {
            (member.project_id.id, member.user_id.id)
            for member in valid_members
        }

        if valid_members:
            tasks = ProjectTask.search([
                ("project_id", "in", valid_members.mapped("project_id").ids),
                ("user_ids", "in", valid_members.mapped("user_id").ids),
            ])

            for task in tasks:
                for user in task.user_ids:
                    key = (task.project_id.id, user.id)

                    if key not in member_keys:
                        continue

                    tasks_by_member_key[key] = (
                        tasks_by_member_key.get(key, empty_tasks) | task
                    )

        for member in self:
            key = (
                member.project_id.id if member.project_id else False,
                member.user_id.id if member.user_id else False,
            )

            member_tasks = tasks_by_member_key.get(key, empty_tasks)

            member.task_ids = member_tasks
            member.task_count = len(member_tasks)