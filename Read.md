# WhatsApp Automation using Playwright

Overall Flow
START
  │
  ▼
Open Playwright
  │
  ▼
Check whatsapp_profile
  │
  ├── Profile exists ──► Open WhatsApp with existing login
  │
  └── No profile ──────► Show QR code
                              │
                              ▼
                         Scan QR manually
  │
  ▼
WhatsApp Ready
  │
  ▼
========== MENU ==========
  │
  ├── 1. Send to one person
  │       │
  │       ├── Ask contact name
  │       ├── Search contact
  │       ├── Skip groups
  │       └── Send message
  │
  ├── 2. Send to multiple people
  │       │
  │       ├── Ask names separated by comma
  │       ├── Search each contact
  │       ├── Skip groups
  │       └── Send message
  │
  ├── 3. Send to contacts from Contact.xlsx
  │       │
  │       ├── Read Name / Phone / Message
  │       ├── Replace {name}
  │       ├── Search contact
  │       ├── Skip groups
  │       ├── Send message
  │       └── Save successful sends
  │
  └── 4. Stop sending
          │
          ▼
     Browser control
          │
          ├── close
          │      └── Close browser
          │          Keep login
          │
          └── logout
                 └── Close browser
                     Delete whatsapp_profile
                     Next run → QR code

## Project Description

This project automates WhatsApp Web using Python and Playwright.

The bot can:

* Open WhatsApp Web
* Use QR code login on the first run
* Save the WhatsApp login session
* Reuse the existing login on the next run
* Search for individual contacts
* Skip group chats
* Send a message to one contact
* Send a message to multiple contacts
* Read contacts and messages from an Excel file
* Replace `{name}` with the actual contact name
* Save successfully sent contacts into an Excel file
* Close the browser while keeping the login
* Logout and remove the saved login profile

---

## Project Files

### `whatappbot.py`

Main program.

It:

1. Opens WhatsApp Web.
2. Checks the saved WhatsApp profile.
3. Uses the existing login if available.
4. Shows the QR code when no login exists.
5. Displays the main menu.
6. Controls closing and logout.

### `choice_menu.py`

Controls the menu options:

```text
1. Send to one person
2. Send to multiple people
3. Send to all contacts in contact sheet
4. Stop sending messages
```

### `search_contact.py`

Searches for contacts in WhatsApp Web.

It also prevents group chats from being selected.

### `send_message.py`

Contains the function used to send WhatsApp messages.

### `export_contacts.py`

Creates and updates the sent-contact Excel file.

The file is named:

```text
Sent_Contacts_YYYY-MM-DD.xlsx
```

### `Contact.xlsx`

Contains contacts and messages for Option 3.

Expected columns:

| Name    | Phone      | Message                 |
| ------- | ---------- | ----------------------- |
| AKM     | 9876543210 | Hi {name}, how are you? |
| Amma    | 9876543211 | Hello {name}            |

The `{name}` value is automatically replaced with the contact name.

### `whatsapp_profile`

Stores the saved WhatsApp browser session.

This folder is ignored by Git and should not be uploaded to GitHub.

---

## Requirements

* Python 3
* Playwright
* openpyxl

Install Playwright:

```bash
pip install playwright
```

Install the Chromium browser:

```bash
python -m playwright install chromium
```

Install openpyxl:

```bash
pip install openpyxl
```


## GitHub

The following files should not be uploaded:

```text
whatsapp_profile/
Contact.xlsx
Sent_Contacts_*.xlsx
```

These are included in `.gitignore`.

The WhatsApp profile should never be committed to GitHub because it contains your saved login/session information.

---

## Important

This project automates WhatsApp Web through Playwright.

Use it responsibly and avoid sending unwanted or excessive messages.

---

## Technologies Used

* Python
* Playwright
* openpyxl
* WhatsApp Web
* Microsoft Excel
