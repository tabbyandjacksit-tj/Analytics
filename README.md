# Tabby & Jack's Analytics 

What?

Benefits? 

For? 

---


## Features / Reports 

## Functions
#### from sheet_reader.py: 
    load_sheet(sheet_idL str, gid: str) -> pd.DataFrame: 
        loads in a google sheet TAB as a DataFrame. This automatically 
        refreshes every 60 seconds. Takes argument of sheet ID from google 
        sheet, as well as the GID for the correct sheet.

    get_google_client() _> gspread.Client: 
        authorizes the credentials of a google client account. This function 
        is used for the back-and-forth editing between sheets and site. 
        Scopes is defined at the start of the file.
    
    def get_worksheet(sheet_id: str, worksheet_name: str):
        opens a worksheet by its spreadsheet ID and tab name. It pulls the
        client through get_google_client(), and gets the spreadsheet key
        from open_by_key. This is why get_google_client() has to exist above. 
    
    def load_private_sheet(sheet_id: str, worksheet_name: str,) -> pd.DataFrame:
        uses get_worksheet to open a worksheet by its spreadsheet ID and tab name. Also obtains all values from the worksheet. This offically loads in 
        the dataframe and stores headers, rows, columns and values. 

    def append_row(sheet_id: str, worksheet_name: str, row_data: dict[str, Any], columns: list[str],) -> None: 
        appends a row to a worksheet. It takes arguments that read in the sheet, creates the workbook and than appends a row to it based on the value_input_option. Immediately after adding, it clears the cache so that it will refresh. This is great for things like officehours

    def update_row_by_id(sheet_id: str, worksheet_name: str, record_id: str, updated_data: dict[str, Any], columns: list[str], id_column_number: int = 1,) -> bool:
        updates a google sheet by finding a row and replalcing the entire rows values. The function uses google sheet indexing, so 1 = COL A rather than 0. This function also clears the cache at the end to ensure that the sheet refreshes. 

    def column_number_to_letter(column_number: int) -> str:
        takes in a column number and turns it into a google sheets column letter.
        This is because google sheets indexes through letters, which is the majority of our functions, but not all columns are in number format. This is a helper function that is nice for anytime that you read in a sheet incase it is not a google sheet. 

    def clear_sheet_cache() -> None:
        clears cached sheet after a function that is written over. 

## Imports/Technologies

## Structure

## Dependencies: 

## How to run application? 

## Configuration 
