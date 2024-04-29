import os
import pyodbc
from datetime import datetime


class ManPowerData:

    def __init__(
        self,
        id: int,
        nric4Digit: int,
        name: str,
        manpowerid: str,
        designation: str,
        nationality: str,
        company: str,
        project: str,
        team: str,
        supervisor: str,
        joinDate: str,
        resignDate: str,
    ) -> None:
        self.id = id
        self.nric4Digit = nric4Digit
        self.name = name
        self.manpowerid = manpowerid
        self.designation = designation
        self.nationality = nationality
        self.company = company
        self.project = project
        self.team = team
        self.supervisor = supervisor
        self.joinDate = joinDate
        self.resignDate = resignDate

    def json(self) -> dict:
        return {
            "id": self.id,
            "nric4Digit": self.nric4Digit,
            "name": self.name,
            "manpowerid": self.manpowerid,
            "designation": self.designation,
            "nationality": self.nationality,
            "company": self.company,
            "project": self.project,
            "team": self.team,
            "supervisor": self.supervisor,
            "joinDate": self.joinDate,
            "resignDate": self.resignDate,
        }


def pylon_db_connection():
    s = os.environ.get("PYLONSERVER")  # Your server name
    d = os.environ.get("PYLONDATABASE")  # Your database
    u = os.environ.get("PYLONUSERNAME")  # Your login
    p = os.environ.get("PYLONPASSWORD")  # Your login password

    pylon_driver = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + s
        + ";DATABASE="
        + d
        + ";UID="
        + u
        + ";PWD="
        + p
    )
    return pyodbc.connect(pylon_driver)


def manpowerlist() -> list:
    data = []
    conn = pylon_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test.SampleManpowerList")
    data = [
        ManPowerData(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
        ).json()
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return data


def detail_manpower(nric4digit: str):
    conn = pylon_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM test.SampleManPowerList WHERE nric4digit=?", nric4digit
    )
    data = [
        ManPowerData(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
        ).json()
        for row in cursor.fetchall()
    ][0]
    cursor.close()
    conn.close()
    return data


def update_manpower(
    designation: str,
    project: str,
    team: str,
    supervisor: str,
    joinDate: datetime,
    resignDate: datetime,
    nric4Digit: str,
):
    conn = pylon_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE test.SampleManPowerList SET designation = ?, project = ?, team = ?, supervisor = ?, joinDate = ?, resignDate = ? WHERE nric4Digit = ?",
        designation,
        project,
        team,
        supervisor,
        joinDate,
        resignDate,
        nric4Digit,
    )
    conn.commit()
    cursor.close()
    conn.close()
