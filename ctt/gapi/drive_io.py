import io
import pandas as pd
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from ctt.gapi.gapi_connection import get_drive_service, get_sheet_service


def list_files(cred_path, folder_id):
    dservice = get_drive_service(cred_path)
    all_files = []
    page_token = None
    while True:
        response = dservice.files().list(q="parents in '{}'".format(folder_id),
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name)',
                                         pageToken=page_token).execute()
        for file in response.get('files'):
            # Process change
            all_files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return all_files



def get_google_sheet(cred_path, spreadsheet_id, range_name):
    sservice = get_sheet_service(cred_path)

    # Call the Sheets API
    gsheet = sservice.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet


def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        raise ValueError("The sheet is empty.")
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df


def get_df_from_sheet(cred_path, SPREADSHEET_ID, range_name="Sheet1"):
    """
    
    :param cred_path:
    :param SPREADSHEET_ID:
    :param range_name:
    :return:
    """
    gsheet = get_google_sheet(cred_path, SPREADSHEET_ID, range_name)
    gdf = gsheet2df(gsheet)

    return gdf



def list_objects_by_name(cred_path, parent_id, name):
    collected = [
        d for d in list_files(cred_path, parent_id) if d["name"] == name]
    return collected

