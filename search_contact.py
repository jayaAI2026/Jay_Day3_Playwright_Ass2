
import re


def search_contact(page, contact_name):

    try:

        contact_name = contact_name.strip()

        if not contact_name:
            print("Contact name is empty.")
            return []

        # ------------------------------------------------
        # Search box
        # ------------------------------------------------

        search_box = page.get_by_placeholder(
            "Search or start a new chat"
        )

        if not search_box.is_visible():

            page.keyboard.press("Escape")

            page.wait_for_timeout(500)

        search_box.wait_for(
            state="visible",
            timeout=10000
        )

        # Clear previous search
        search_box.fill("")

        # Enter contact name
        search_box.fill(contact_name)

        print(
            f"Searching for: {contact_name}"
        )

        page.wait_for_timeout(2000)

        # ------------------------------------------------
        # Get WhatsApp search results
        # ------------------------------------------------

        results = page.locator(
            "div[role='gridcell']"
        )

        matching_results = []

        # ------------------------------------------------
        # Check every result
        # ------------------------------------------------

        for i in range(results.count()):

            result = results.nth(i)

            try:

                text = result.inner_text().strip()

                if not text:
                    continue

                lines = [
                    line.strip()
                    for line in text.splitlines()
                    if line.strip()
                ]

                if not lines:
                    continue

                # ------------------------------------------------
                # Get ONLY contact/chat name
                # ------------------------------------------------

                contact_title = ""

                for line in lines:

                    # Ignore unread message
                    if re.fullmatch(
                        r"\d+\s+unread\s+messages?",
                        line,
                        re.IGNORECASE
                    ):
                        continue

                    # Ignore time
                    if re.fullmatch(
                        r"\d{1,2}:\d{2}\s*(am|pm)",
                        line,
                        re.IGNORECASE
                    ):
                        continue

                    # Ignore date
                    if re.fullmatch(
                        r"\d{1,2}/\d{1,2}/\d{4}",
                        line
                    ):
                        continue

                    # Ignore numbers
                    if line.isdigit():
                        continue

                    contact_title = line

                    break

                if not contact_title:
                    continue

                # ------------------------------------------------
                # Ignore groups
                # ------------------------------------------------

                if "is also in this group" in text.lower():
                    continue

                # Group names often contain &
                if "&" in contact_title:
                    continue                   

                # ------------------------------------------------
                # Match only contact name
                # ------------------------------------------------

                if (
                    contact_name.lower()
                    in contact_title.lower()
                ):

                    # Avoid duplicate contacts
                    already_added = False

                    for existing in matching_results:

                        if (
                            existing["name"].lower()
                            == contact_title.lower()
                        ):
                            already_added = True
                            break

                    if not already_added:

                        matching_results.append({
                            "name": contact_title,
                            "locator": result
                        })

            except Exception:

                continue

        # ------------------------------------------------
        # No matching contact
        # ------------------------------------------------

        if not matching_results:

            print(
                f"\nNo individual chat found for: "
                f"{contact_name}"
            )

            return []

        # ------------------------------------------------
        # Only ONE matching contact
        # ------------------------------------------------

        if len(matching_results) == 1:

            selected = matching_results[0]

            print(
                f"\nFound chat: "
                f"{selected['name']}"
            )

            return [selected]

        # ------------------------------------------------
        # Multiple matching contacts
        # ------------------------------------------------

        print(
            "\nMultiple contacts found:\n"
        )

        for number, item in enumerate(
            matching_results,
            start=1
        ):

            print(
                f"{number}. {item['name']}"
            )

        # ------------------------------------------------
        # Allow:
        #
        # 1
        # 1,2
        # 1,3,2
        # ------------------------------------------------

        while True:

            choice = input(
                "\nChoose contacts "
                "(example: 1,3,2): "
            ).strip()

            try:

                choice_numbers = [
                    int(number.strip())
                    for number in choice.split(",")
                    if number.strip()
                ]

                # Remove duplicate selections
                choice_numbers = list(
                    dict.fromkeys(
                        choice_numbers
                    )
                )

                if not choice_numbers:
                    raise ValueError

                # Check numbers
                if any(
                    number < 1
                    or number > len(matching_results)
                    for number in choice_numbers
                ):
                    raise ValueError

                break

            except ValueError:

                print(
                    f"Please enter numbers between 1 "
                    f"and {len(matching_results)}, "
                    f"separated by commas."
                )

        # ------------------------------------------------
        # Create selected contact list
        # ------------------------------------------------

        selected_contacts = []

        for choice_number in choice_numbers:

            selected_contacts.append(
                matching_results[
                    choice_number - 1
                ]
            )

        # ------------------------------------------------
        # Show selected contacts
        # ------------------------------------------------

        print(
            "\nSelected contacts:"
        )

        for contact in selected_contacts:

            print(
                f"- {contact['name']}"
            )

        return selected_contacts

    except Exception as e:

        print(
            f"\nError while searching for "
            f"'{contact_name}': {e}"
        )

        return []
