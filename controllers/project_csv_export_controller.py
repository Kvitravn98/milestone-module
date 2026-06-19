import csv
import io
from datetime import date

from odoo import http
from odoo.http import request, content_disposition

print("CSV EXPORT CONTROLLER LOADED")
class ProjectCsvExportController(http.Controller):

    @http.route(
        "/milestones_module/export_project_csv",
        type="http",
        auth="user",
    )
    def export_project_csv(self, **kwargs):

        project_id = kwargs.get("project_id")
        export_milestones = kwargs.get("export_milestones")
        export_team_members = kwargs.get("export_team_members")
        export_tasks = kwargs.get("export_tasks")

        try:
            project_id = int(project_id)
            export_milestones = self._to_bool(kwargs.get("export_milestones"))
            export_tasks = self._to_bool(kwargs.get("export_tasks"))
            export_team_members = self._to_bool(kwargs.get("export_team_members"))

            print(f"Exporting project {project_id} with options: Milestones:{export_milestones} - Team Members: {export_team_members} - Tasks: {export_tasks}")

        except (TypeError, ValueError):
            return request.not_found()

        project = request.env["project.project"].browse(project_id)

        if not project.exists():
            return request.not_found()

        output = io.StringIO(newline="")

        fieldnames = [
            "record_type",
            "project_name",
            "project_manager",
            "customer",
            "milestone_name",
            "milestone_deadline",
            "milestone_state",
            "task_name",
            "task_milestone",
            "task_assignee_logins",
            "task_stage",
            "estimated_hours",
            "team_member_login",
            "team_member_name",
            "team_member_role",
            "team_member_active",
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        self._write_project_summary(writer, project)
        if export_milestones:
            self._write_milestones(writer, project)

        if export_tasks:
            self._write_tasks(writer, project)

        if export_team_members:
            self._write_team_members(writer, project)

        content = output.getvalue().encode("utf-8-sig")
        filename = self._get_filename(project)

        return request.make_response(
            content,
            headers=[
                ("Content-Type", "text/csv; charset=utf-8"),
                ("Content-Disposition", content_disposition(filename)),
            ]
        )

    def _write_project_summary(self, writer, project):
        writer.writerow({
            "record_type": "project_summary",
            "project_name": project.name or "Project",
            "project_manager": project.user_id.name,
            "customer": project.partner_id or "Customer",
        })

    def _write_milestones(self, writer, project):
        milestones = project.milestone_ids.sorted(
            key=lambda m: (
                m.deadline or date.max,
                m.name or "Milestone",
            )
        )

        for milestone in milestones:
            writer.writerow({
                "record_type": "milestone",
                "project_name": project.name or "Project",
                "milestone_name": milestone.name or "Milestone",
                "milestone_deadline": (
                    milestone.deadline.isoformat()
                    if milestone.deadline
                    else ""
                ),
                "milestone_state": milestone.state or "",
            })

    def _write_tasks(self, writer, project):
        tasks = project.task_ids.sorted(
            key=lambda t: (
                t.milestone_id.id or 0,
            )
        )

        for task in tasks:
            writer.writerow({
                "record_type": "task",
                "project_name": project.name or "Project",
                "task_name": task.name or "Task",
                "task_milestone": task.milestone_id.name or "",
                "task_assignee_logins": ";".join(task.user_ids.mapped("login")),
                "task_stage": task.stage_id.name or "",
                "estimated_hours": task.estimated_hours or 0.0,
        })

    def _write_team_members(self, writer, project):
        team_members = project.team_member_ids.sorted(
            key=lambda m: (
                m.role or "",
                m.user_id.name or "",
            )
        )

        for member in team_members:
            writer.writerow({
                "record_type": "team_member",
                "project_name": project.name or "Project",
                "team_member_login": member.user_id.login or "",
                "team_member_name": member.user_id.name or "Member",
                "team_member_role": member.role or "",
                "team_member_active": member.active
            })

    def _to_bool(self, value):
        return str(value).lower() in ("1", "true", "yes", "on")

    def _get_filename(self, project):
        safe_project_name = (project.name or "Project").strip().lower()
        safe_project_name = safe_project_name.replace(" ", "_")

        return f"{safe_project_name}_export.csv"