'''Open whatsapp using  QR code Manually 
Search the name  i mention and send message Hi am bot send you message 
collect the call the contact info name number and last message and save it in a excel file 
using only playwright and python '''

import shutil
import os

from playwright.sync_api import sync_playwright
from choice_menu import choice_menu

with sync_playwright() as s:

    # Open Chrome with a persistent WhatsApp profile.
    # This saves the WhatsApp login session.
    browser = s.chromium.launch_persistent_context(
        "whatsapp_profile",
        headless=False
    )

    # Use existing page if available.
    # Otherwise create a new page.
    page = (
        browser.pages[0]
        if browser.pages
        else browser.new_page()
    )

    # Open WhatsApp Web
    page.goto("https://web.whatsapp.com/")

    print("Opening WhatsApp Web...")
    print("Checking WhatsApp login...")

    # Wait until WhatsApp is logged in.
    # If not logged in, scan QR code manually.
    page.get_by_placeholder(
        "Search or start a new chat"
    ).wait_for(
        state="visible",
        timeout=0
    )

    print("WhatsApp login successful!")

    # Handle WhatsApp popup if it appears
    try:
        page.get_by_role(
            "button",
            name="Continue"
        ).click(timeout=3000)

        print("Popup closed.")

    except:
        print("No popup found.")

    print("WhatsApp is ready.")

   
    # ------------------------------------------------
    # Keep showing menu until user chooses 3
    # ------------------------------------------------
    while True:
       # export_file = create_export_file()
        choice = input("""
                ========== WHATSAPP BOT ==========

                1. Send to one person
                2. Send to multiple people
                3. Send to all contacts in contact sheet
                4. Stop sending messages

                Enter choice: """).strip()
        stop=choice_menu(page,choice)
        if stop:
             break

# ------------------------------------------------
# Browser control
# ------------------------------------------------
    while True:
        command = input(
            "\nType 'close' to close browser "
            "or 'logout' to remove login: "
        ).strip().lower()

        if command == "close":

            print("\nClosing WhatsApp browser...")
            browser.close()
            print("Browser closed.")
            print("WhatsApp login is saved.")
            break

        elif command == "logout":

            print("\nLogging out...")

            browser.close()

            if os.path.exists("whatsapp_profile"):
                shutil.rmtree("whatsapp_profile")

            print("Browser closed.")
            print("WhatsApp login removed.")

            break