

def format_report2mnger(
        reports, config, topic, target_date, report2mngr_dir=".",
        report2mngr_name="./report2mngr_{}.html"):
    """

    :param reports: pd.DataFrame. The report from Google Sheet which includes the following columns:
                    - student: str. Student's name
                    - mentor: str. Mentor's name
                    - Timestamp: datetime. Meeting time
                    - The other two string columns are the mentor's comments.
    :param config: dict. The configurations loaded from the yaml file.
    :param topic: str. The topic this week.
    :param target_date: datetime. The first date of the week for which the report is written. As long as the date
                    component is correct, the time component is irrelevant.
    :param report2mngr_dir: str. The dir where the generated report is to be saved.
    :param report2mngr_name: str. The name of the generated report.
    """
    css_tmplt_path = config["report_tmplt"]["css"]
    body_tmplt_path = config["report_tmplt"]["body"]

    comfort = "What's the student's comfort level on the subject this week?"
    comment = "Your comment on the student's performance?"

    report2manager = reports[["student", "mentor", comfort, comment]].rename(columns={
        "mentor": "Mentor", "student": "Student", "Timestamp": "Meeting Date",
        comfort: "Student's Comfort Level", comment: "Mentor's Comment"
    })

    table = report2manager.to_html(index=False)

    with open(css_tmplt_path) as f:
        css = f.read()

    with open(body_tmplt_path) as f:
        body = f.read()

    report2mngr_html = css + body.format(table=table, week=str(target_date.date()), topic=topic)

    path = "{}/{}".format(report2mngr_dir, report2mngr_name.format(str(target_date.date())))
    with open(path, "w") as f:
        f.write(report2mngr_html)
