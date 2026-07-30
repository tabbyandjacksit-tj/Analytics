# Tabby & Jack's Analytics 

What?

Benefits? 

For? 

---


## Features / Reports 

## Functions
#### from utils/tools/sheet_reader.py: 
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

#### from utils/tools/secrets.py: 
    def _read_local_secrets() -> Any | None:
        
    def get_secret(name: str) -> str:

    def get_optional_secret(name: str, default: str = "",) -> str:

    def get_google_service_account() -> dict[str, Any]:

#### from utils/tools/images.py: 
    def image_to_base64(image_path: str) -> str:
        converts an image file to base64 to enable enbedding in HTML. All images are kept in images/ and must all be read in with this function in order to be read on the website. 

#### from utils/reporting/officehours.py
    TASK_COLUMNS: 
        sets the columns of the task sheet. includes a myriad of tabs that will be crucial in reading in sheet and tracking information about office hours worked and tasks completed. 

    LOCAL_TIMEZONE: 
        sets the timezone to America/Chicago. This is hardcoded in, but if we ever have employees outside of this zone, we could make adjustments. 

    def get_week_start(target_date: date | None = None) -> date:
        helper function that always returns the first day of the start of the week that an inputed date is given. It will always start at Monday rather than Sunday. 

    def get_saved_minutes(task: dict) -> float:
        helper function that obtains the previously recorded minutes as a number. If there is nothing recorded, than 0.0 minutes is reported. 
    
    def get_active_session_minutes(task: dict) -> float:
        helper function that returns the time elapsed in minutes during the current active session. This function also uses LOCAL_TIMEZONE to get the correct date and time when reporting the final elapsed time. Will return 0.0 if there is nothing else to return. 

    def create_task_record(employee: str, project: str, task: str = "", notes: str = "",) -> dict:
        creates a new project record and places it in the to-do status. It also gathers the date = today and sets it as the created date. This is also where get_week_start() gets implemented to get the start of the week based on the date of today. 

    def start_task_record(task: dict) -> dict:
        created an "updated task" which is going to set the task to active, obtain the start time, set end time and completed date to "", and saves a dictionary with that information
    
    def pause_task_record(task: dict) -> dict: 
        creates an "updated task" which is going to set the task to "In Progress", save the minutes as what has already been saved + the current active counter, and than set the start time, end time, and completed date to blank. 

    def resume_task_record(task: dict) -> dict:
        this will resume a task that is in progress without getting rid of the saved time. Instead it will just mark it as resumed and continue the timer. This sets the status to "Active" as well. 

    def finish_task_record(task: dict) -> dict:
        creates a finished_task dictionary that also calculates the current time for the finished time, updates the saved minutes using get_saved_minutes and produces the amount of time that task took, marks the status as finished, and saves the completed date as the day today. 






## Imports/Technologies

## Structure

## Dependencies: 

## How to run application? 

## Configuration 
