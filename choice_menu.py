from search_contact import search_contact
from send_message import send_message
import openpyxl
from datetime import datetime
from export_contacts import save_contact


def choice_menu(page, choice):

    # ------------------------------------------------
    # OPTION 1
    # One contact name
    # ------------------------------------------------

    if choice == "1":

        contact_name = input(
            "Enter contact name: "
        ).strip()

        if not contact_name:
            print("Contact name cannot be empty.")
            return

        # Search one name
        selected_contacts = search_contact(
            page,
            contact_name
        )

        # Send message to selected contact(s)
        for contact in selected_contacts:

            print(
                f"\nOpening: {contact['name']}"
            )

            contact["locator"].click()

            page.wait_for_timeout(1500)

            send_message(page)
            save_contact(contact["name"], "", "Default message" )
            
            print(
                f"Sent to {contact['name']} ✓"
            )

    # ------------------------------------------------
    # OPTION 2
    # Multiple contact names
    # Example:
    # Husband, Amma, Deepa
    # ------------------------------------------------

    elif choice == "2":

        contacts_name = [
            name.strip()
            for name in input(
                "Enter contact names separated by comma: "
            ).split(",")
            if name.strip()
        ]

        if not contacts_name:
            print("No contact names entered.")
            return

        # Search each name separately
        for contact_name in contacts_name:

            print(
                f"\nSending to {contact_name}..."
            )

            selected_contacts = search_contact(
                page,
                contact_name
            )

            # Send to every selected contact
            for contact in selected_contacts:

                print(
                    f"\nOpening: {contact['name']}"
                )

                contact["locator"].click()

                page.wait_for_timeout(1500)

                send_message(page)
                save_contact(contact["name"], "", "Default message" )

                print(
                    f"Sent to {contact['name']} ✓"
                )

    # ------------------------------------------------
    # OPTION 3
    # Send message to ALL people in Excel
    # ------------------------------------------------

    elif choice == "3":

        # Excel file containing contact details
        # and messages
        excel_file = "Contact.xlsx"

        try:

            # Open the Excel workbook
            workbook = openpyxl.load_workbook(
                excel_file
            )

            # Select the active worksheet
            sheet = workbook.active

            print(
                f"\nReading contacts from {excel_file}..."
            )

            # Start reading from row 2
            # Row 1 contains the column headings
            for row in sheet.iter_rows(
                min_row=2,
                values_only=True
            ):

                # Column A = Name
                # Column B = Phone
                # Column C = Message
                name = row[0]
                phone = row[1]
                message = row[2]

                # Skip the row if the name is empty
                if not name:
                    continue

                print(
                    f"\nSending to: {name}"
                )

                # Display phone number
                print(f"Phone: ****{str(phone)[-4:]}")

                # Check whether a message is available
                if not message:

                    print(
                        f"No message found for {name}"
                    )

                    continue

                # Convert message to text
                message = str(message)

                # Replace {name} with actual contact name
                message = message.replace(
                    "{name}",
                    str(name)
                )

                # Display final message
                print(
                    f"Message: {message}"
                )

                # Search for the contact in WhatsApp
                selected_contacts = search_contact(
                    page,
                    str(name)
                )

                # Process the contacts found
                for contact in selected_contacts:

                    # Open the selected contact
                    print(
                        f"\nOpening: {contact['name']}"
                    )

                    contact["locator"].click()

                    # Wait for chat to open
                    page.wait_for_timeout(1500)

                    # Send the message from Excel
                    send_message(page, message)
                    save_contact(contact["name"],phone, message)
                    # Display confirmation
                    print(
                        f"Sent to {contact['name']} ✓"
                    )

            # Finished processing all Excel rows
            print(
                "\nAll Excel contacts processed."
            )

        except FileNotFoundError:

            # Excel file does not exist
            print(
                f"\nExcel file not found: {excel_file}"
            )

        except Exception as e:

            # Display any other error
            print(
                f"\nError reading Excel: {e}"
            )

    # ------------------------------------------------
    # OPTION 4
    # Stop sending messages
    # ------------------------------------------------

    elif choice == "4":

        print(
            "\nStopping WhatsApp message bot..."
        )

        print(
            "WhatsApp browser will remain open."
        )

        return True

    else:

        print("Invalid choice.")
        return

    # Return to main menu
    input(
        "\nPress Enter to return to the menu..."
    )