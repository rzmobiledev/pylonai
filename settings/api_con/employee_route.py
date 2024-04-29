from fileinput import filename
from flask_restx import fields, Resource, Namespace
from flask import request, jsonify, make_response
import csv
from pathlib import Path
import os
from datetime import datetime
from .employee_format import employeeList, employee_detail, employee_update

api = Namespace("employee", description="EMPLOYEE ENDPOINT")

manpower_fields = api.model(
    "Manpower Fields",
    {
        "nric4Digit": fields.String(description="resignDate", required=True),
        "designation": fields.String(description="designation", required=True),
        "project": fields.String(description="project", required=True),
        "team": fields.String(description="team", required=True),
        "supervisor": fields.String(description="supervisor", required=True),
        "joinDate": fields.String(description="joinDate", required=True),
        "resignDate": fields.String(description="resignDate", required=True),
    },
)


@api.route("")
class ManPowerListRoute(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    def get(self):
        try:
            data = employeeList()
            return make_response(jsonify({"data": data}))
        except Exception:
            return make_response(
                jsonify({"message": "Cannot retrieve employee data"}), 500
            )


@api.route("/<int:id>")
@api.doc(params={"id": "id"})
class ManPowerDetailRoute(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    def get(self, id):
        try:
            data = employee_detail(id)
            return make_response(jsonify({"data": data}))
        except Exception:
            return make_response(jsonify({"message": "Data not found"}), 404)

    @api.response(500, "Internal error")
    @api.response(200, "Success")
    @api.doc(
        model=manpower_fields,
        params={
            "designation": "designation",
            "project": "project",
            "team": "team",
            "supervisor": "supervisor",
            "joinDate": "joinDate",
            "resignDate": "resignDate",
        },
    )
    def put(self, id):
        try:
            designation = request.args.get("designation")
            project = request.args.get("project")
            team = request.args.get("team")
            supervisor = request.args.get("supervisor")
            joinDate = request.args.get("joinDate")
            resignDate = request.args.get("resignDate")

            if (
                designation and project and team and supervisor and joinDate
            ):  # using swagger
                data = dict(
                    designation=designation,
                    project=project,
                    team=team,
                    supervisor=supervisor,
                    joinDate=datetime.strptime(joinDate, "%Y-%m-%d"),
                    resignDate=(
                        datetime.strptime(resignDate, "%Y-%m-%d")
                        if resignDate
                        else None
                    ),
                )

            else:  # using postman. need to change string date to python date
                data = request.get_json()
                joindate = datetime.strptime(data.get("joinDate"), "%Y-%m-%d")
                resigndate = (
                    datetime.strptime(data.get("resignDate"), "%Y-%m-%d")
                    if data.get("resignDate")
                    else None
                )
                data["joinDate"] = joindate
                data["resignDate"] = resigndate

            employee_update(
                data.get("designation"),
                data.get("project"),
                data.get("team"),
                data.get("supervisor"),
                data.get("joinDate"),
                data.get("resignDate"),
                id,
            )
            return make_response(jsonify({"data": "Employee's data updated."}))
        except Exception:
            return make_response(
                jsonify({"message": "Cannot update employee."}), 500
            )


@api.route("/csv")
class EmployeeCSV(Resource):
    @api.response(500, "Internal error")
    @api.response(200, "Success")
    def get(self):
        try:
            data = employeeList()
            create_csv(data)
            return make_response(
                jsonify({"data": "Employee data exported succesfuly."})
            )
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
            # return make_response(
            #     jsonify({"message": "Cannot create employee report."}), 500
            # )


def create_csv(employeeList: list[dict]):

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    report_folder = "report"
    employee_csv = "employee.csv"

    file_path = os.path.join(BASE_DIR, report_folder)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    with open(f"{file_path}/{employee_csv}", "a") as f:
        w = csv.writer(f)
        """
        write csv header column
        """
        w.writerow(head for head in employeeList[0].keys())
        for employee in employeeList:
            w.writerow(row for row in employee.values())
