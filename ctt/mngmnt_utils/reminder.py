from ctt.gapi.gmail import create_message, send_message
from datetime import timedelta


def compose_missing_report_alert(student, mentor, coordinator, form, target_date, msg_template):
    week_start = (target_date - timedelta(days=target_date.weekday())).date()
    return msg_template.format(
        mentor=mentor, student=student, coordinator=coordinator, form=form, week=str(week_start))


def send_reminder(missing, config, target_date, cred_path):
    msg_template_path = config["reminder_message"]["template_path"]
    coordinator_name = config["coordinator"]["name"]
    coordinator_email = config["coordinator"]["email"]

    with open(msg_template_path) as f:
        msg_temp = f.read()

    for doc in missing:
        student, mentor, mentor_email, form_url = doc
        msg = compose_missing_report_alert(
            student, mentor, coordinator_name, form_url, target_date, msg_temp)
        msg = create_message(
            coordinator_email, mentor_email, "Weekly report", msg, cc="", msg_type="html")

        send_message(cred_path, "me", msg)
