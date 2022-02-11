# aiosendgrid

A simple SendGrid asynchronous client based on [httpx](https://github.com/encode/httpx).


# Installation

```bash
pip install aiosendgrid
```

Or, to include the optional SendGrid helpers support, use:

```bash
pip install aiosendgrid[helpers]
```

# Usage

## With Mail Helper Class

```python
import aiosendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To

SENDGRID_API_KEY = "SG.XXX" 

from_email = Email("test@example.com")
to_email = To("test@example.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, to_email, subject, content)

async with aiosendgrid.AsyncSendGridClient(api_key=SENDGRID_API_KEY) as client:
    response = await client.send_mail_v3(body=mail.get())
```

More info on [sendgrid-python](https://github.com/sendgrid/sendgrid-python) official repository.

## Without Mail Helper Class

```python
import aiosendgrid

SENDGRID_API_KEY = "SG.XXX"

data = {
    "personalizations": [
        {
            "to": [{"email": "test@example.com"}],
            "subject": "Sending with SendGrid is Fun",
        }
    ],
    "from": {"email": "test@example.com"},
    "content": [
        {"type": "text/plain", "value": "and easy to do anywhere, even with Python"}
    ],
}

async with aiosendgrid.AsyncSendGridClient(api_key=SENDGRID_API_KEY) as client:
    response = await client.send_mail_v3(body=data)
```

