import os
from typing import Any, Dict, List
from gspread.worksheet import Worksheet
import gspread


class Sheet:
    """
    A wrapper around a Google Sheets "sheet" (e.g. one tab of a spreadsheet).
    """

    def __init__(self, sheet: Worksheet) -> None:
        self.sheet: Worksheet = sheet
        self.all_values = self.sheet.get_all_values()
        self.all_records = self.sheet.get_all_records()
        self.headers = self.all_values[0]

    def get_headers(self) -> List[str]:
        return self.headers

    def get_all_values(self) -> List[List[Any]]:
        return self.all_values

    def get_all_records(self) -> List[Dict[str, Any]]:
        return self.all_records


class BaseSpreadsheet:
    """
    A pointer to the master spreadsheet.
    """

    def __init__(self, spreadsheet_url: str) -> None:
        if not os.path.exists("service-account.json"):
            raise Exception(
                "Could not find Google Service Account at service-account.json.")

        self.spreadsheet_url = spreadsheet_url
        self.spreadsheet = gspread.service_account(
            "service-account.json").open_by_url(spreadsheet_url)

    def get_sheet(self, sheet_name: str) -> Sheet:
        return Sheet(sheet=self.spreadsheet.worksheet(sheet_name))
