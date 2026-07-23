# Tabby & Jack's Analytics 

What?

Benefits? 

For? 

---


## Features / Reports 

## Functions
#### from sheet_reader.py: 
    load_sheet(sheet_idL str, gid: str) -> pd.DataFrame: 
        loads in a public google sheet TAB as a pandas DataFrame. This automatically caches every 60 seconds. Best used for read-only sheets, that also do not require authentication

    get_google_client() _> gspread.Client: 
        creates and returns an authenticated google sheet client using the google service account credentials. The permissions that are avaliable to the user are controlled by the SCOPES, which is defined at the top of the file. This allows the application to read and write from PRIVATE google sheets. 
    
    def get_worksheet(sheet_id: str, worksheet_name: str):
        opens and returns a specific google sheets worksheet using  the sheet ID and tab name. This  function ues get_google_client() to create an authenticated connection and open_by_key to open the spreedsheet. Worksheet() gets used to select the requested tab. This is a helper function that is used by other functions needing direct workbook access. 
    
    def load_private_sheet(sheet_id: str, worksheet_name: str,) -> pd.DataFrame:
        loads in a private google sheet into a pd DF. This function uses get_worksheet() to access the worksheet. It also uses get_all_values() to get the rows/cols. The first row is used to hold the df's col. This is cached after running to reduce API calls. 

    def append_row(sheet_id: str, worksheet_name: str, row_data: dict[str, Any], columns: list[str],) -> None: 
        appends a row to the end of a google sheet. It uses the column list to determine how the values should be stored in that sheet. The sheet is immediately cached after in order to reload/refresh the updated data. This is particularly helpful for things like Office Hours Tasks. 

    def update_row_by_id(sheet_id: str, worksheet_name: str, record_id: str, updated_data: dict[str, Any], columns: list[str], id_column_number: int = 1,) -> bool:
        updates a sheet's existing row using a unique record ID and updates that row with a new value. id_column_number identifies which sheet contains that record. Google sheet uses indexing that begins at 1, so column A is = 1. The function returns True if the record was found AND updated. The cache is than cleared to reload  the newest data. 

    def column_number_to_letter(column_number: int) -> str:
        converts a numeric column position into its correspoinding CSV column letter. This is a helper function that is used for creating  A1-style cell ranges. 

    def clear_sheet_cache() -> None:
        clears cached sheet after a function that is written over. This should be called after data is written or updated. 

#### from secrets.py: 
    def _read_local_secrets() -> Any | None:
        
    def get_secret(name: str) -> str:

    def get_optional_secret(name: str, default: str = "",) -> str:

    def get_google_service_account() -> dict[str, Any]:

## Imports/Technologies

## Structure

## Dependencies: 

## How to run application? 

## Configuration 
