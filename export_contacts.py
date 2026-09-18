import openpyxl
from datetime import datetime


# Store the export file name once
export_file = None


def create_export_file():

    global export_file

    # If file is already created, reuse it
    if export_file:
        return export_file

    # Create today's file name
    date = datetime.now().strftime("%Y-%m-%d")
    export_file = f"Sent_Contacts_{date}.xlsx"

    # Create Excel file
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Add headings
    sheet.append([
        "Name",
        "Phone",
        "Message",
        "Status"
    ])

    workbook.save(export_file)

    return export_file


def save_contact(name, phone, message):

    # Get the existing export file
    file_name = create_export_file()

    # Open Excel
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active

    # Add sent contact
    sheet.append([
        name,
        phone,
        message,
        "Sent"
    ])

    # Save Excel
    workbook.save(file_name)