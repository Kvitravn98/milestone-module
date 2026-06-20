from odoo import fields, models

import base64
import binascii
import csv
import io

from odoo.exceptions import UserError, ValidationError

class ProjectCsvImportWizard(models.TransientModel):
    _name = "project.csv.import.wizard"
    _description = "Project Csv Import Wizard"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
    )

    csv_file = fields.Binary(
        string="CSV File",
        required=True,
        attachment=False,
    )

    import_milestones = fields.Boolean(
        string="Import Milestones",
        default=True,
    )

    filename = fields.Char(
        string="File Name",
    )

    import_team_members = fields.Boolean(
        string="Import Team Members",
        default=True,
    )

    def action_import_csv(self):
        self.ensure_one()

        if not self.import_milestones and not self.import_team_members:
            raise UserError("Please select at least one import option.")

        self._check_csv_file_extension()

        rows = self._get_csv_rows()
        self._check_csv_headers(rows)

        stats = self._import_rows(rows)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "CSV Import Completed",
                "message": self._get_import_summary_message(stats),
                "type": "success",
                "sticky": True,
            },
        }


    def _check_csv_file_extension(self):
        self.ensure_one()

        filename = (self.filename or "").lower().strip()

        if not filename.endswith(".csv"):
            raise UserError("Please upload a CSV file.")


    def _get_csv_rows(self):
        self.ensure_one()

        try:
            decoded_file = base64.b64decode(self.csv_file)
        except (binascii.Error, ValueError):
            raise UserError("The uploaded file could not be decoded.")

        try:
            csv_content = decoded_file.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise UserError("The uploaded file must be a valid UTF-8 CSV file.")

        reader = csv.DictReader(io.StringIO(csv_content))

        try:
            return list(reader)
        except csv.Error:
            raise UserError("The uploaded CSV file could not be read.")


    def _check_csv_headers(self, rows):
        self.ensure_one()

        fieldnames = set(rows[0].keys())

        required_headers = {"record_type"}

        if self.import_milestones:
            required_headers.update({
                "milestone_name",
                "milestone_deadline",
                "milestone_state",
            })

        if self.import_team_members:
            required_headers.update({
                "team_member_login",
                "team_member_role",
            })

        missing_headers = required_headers - fieldnames

        if missing_headers:
            raise UserError(
                "The uploaded CSV file is missing required columns: %s"
                % ", ".join(sorted(missing_headers))
            )


    def _import_rows(self, rows):
        stats = {
            "milestones_created": 0,
            "milestones_skipped": 0,
            "team_members_created": 0,
            "team_members_skipped": 0,
            "rows_ignored": 0,
        }

        for row in rows:
            record_type = (row.get("record_type") or "").strip()

            if record_type == "milestone" and self.import_milestones:
                self._import_milestones_rows(row, stats)
                continue

            if record_type == "team_member" and self.import_team_members:
                self._import_team_members_rows(row, stats)
                continue

            stats["rows_ignored"] += 1

        return stats


    def _import_milestones_rows(self, row, stats):
        milestone_name = (row.get("milestone_name") or "").strip()
        milestone_deadline = (row.get("milestone_deadline") or "").strip()
        milestone_state = (row.get("milestone_state") or "").strip()

        if not milestone_name:
            stats["milestones_skipped"] += 1
            print(f"Milestone import skipped: {milestone_name} empty")
            return

        valid_states = ("todo","in_progress","done")

        if milestone_state not in valid_states:
            stats["milestones_skipped"] += 1
            print(f"Milestone import skipped: {milestone_state} not in valid states")
            return

        existing_milestone = self.env["project.milestone"].search([
            ("name", "=", milestone_name),
            ("project_id", "=", self.project_id.id)
        ], limit = 1)

        if existing_milestone:
            stats["milestones_skipped"] += 1
            print(f"Milestone import skipped: {milestone_name} already exists")
            return

        values = {
            "project_id": self.project_id.id,
            "name": milestone_name,
            "state": milestone_state,
        }

        if milestone_deadline:
            try:
                values["deadline"] = fields.Date.to_date(milestone_deadline)
            except (ValueError, TypeError) as error:
                stats["milestones_skipped"] += 1
                print(f"Milestone import skipped - date error: {error}")
                return

        try:
            self.env["project.milestone"].create([values])
            stats["milestones_created"] += 1
            return
        except (UserError, ValidationError) as error:
            stats["milestones_skipped"] += 1
            print(f"Milestone import skipped: {error}")
            return


    def _import_team_members_rows(self, row, stats):
        team_member_login = (row.get("team_member_login") or "").strip()
        team_member_role = (row.get("team_member_role") or "").strip()

        if not team_member_login:
            stats["team_members_skipped"] += 1
            return

        valid_roles = {"team_lead","developer","tester","analyst"}

        if team_member_role not in valid_roles:
            stats["team_members_skipped"] += 1
            return

        user = self.env["res.users"].search(
            [
                ("login", "=", team_member_login),
            ], limit = 1
        )

        if not user:
            stats["team_members_skipped"] += 1
            return

        existing_member = self.env["project.team.member"].search([
            ("user_id", "=", user.id),
            ("project_id", "=", self.project_id.id)
        ], limit = 1)

        if existing_member:
            stats["team_members_skipped"] += 1
            return
        try:
            self.env["project.team.member"].create([{
                "project_id": self.project_id.id,
                "user_id": user.id,
                "role": team_member_role,
                "active": True,
            }])
            stats["team_members_created"] += 1
            return
        except UserError:
            stats["team_members_skipped"] += 1
            return

    def _get_import_summary_message(self, stats):
        return (
            "Milestones created: %(milestones_created)s\n"
            "Milestones skipped: %(milestones_skipped)s\n"
            "Team members created: %(team_members_created)s\n"
            "Team members skipped: %(team_members_skipped)s\n"
            "Rows ignored: %(rows_ignored)s"
        ) % stats






