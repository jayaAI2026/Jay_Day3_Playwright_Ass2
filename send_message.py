def send_message(page, message=None):

    # Default message
    if message is None:
        message = "Hi, I am a bot sending you a message. Testing the WhatsApp bot using Playwright and Python."

    message_box = page.locator(
        "div[contenteditable='true']"
    ).last

    message_box.wait_for(
        state="visible",
        timeout=10000
    )

    message_box.fill(message)
    message_box.press("Enter")

    page.wait_for_timeout(1000)

    print("Message sent ✓")