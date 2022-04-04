from ctt.gapi.drive_io import *
from datetime import timedelta


def get_response_sheet_id(folder_id, cred_path):
    response_sheet_id = [
        doc["id"] for doc in list_files(cred_path, folder_id)
        if doc["name"] == "Mentor Report (Responses)"][0]
    return response_sheet_id


def collect_report(sheet_id, target_date, cred_path):
    week_start = (target_date - timedelta(days=target_date.weekday())).date()
    week_end = week_start + timedelta(days=7)
    df_report = get_df_from_sheet(cred_path, sheet_id, "Form Responses 1")
    df_report = df_report.assign(
        Timestamp=lambda x: pd.to_datetime(x["Timestamp"], format="%m/%d/%Y %H:%M:%S")
    )
    mask = df_report["Timestamp"].apply(
        lambda x: (x.date() > week_start) and (x.date() < week_end))
    df_report = df_report.loc[mask]
    return df_report


def collect_reports_of_the_week(mentor_students, target_date, cred_path):
    lst_folder_ids = mentor_students["folder_id"].to_list()
    lst_reports = []

    for folder_id in lst_folder_ids:
        sheet_id = get_response_sheet_id(folder_id, cred_path)
        report = collect_report(sheet_id, target_date, cred_path)
        report["folder_id"] = folder_id
        lst_reports.append(report)

    reports = pd.concat(lst_reports).reset_index(drop=True)
    return mentor_students.merge(reports, how="left")
