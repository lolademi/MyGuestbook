import os
from datetime import datetime
from pathlib import Path
import pytz
from supabase import create_client, Client
from dotenv import load_dotenv
from fasthtml.common import *

# Load environment variables
load_dotenv(Path(__file__).resolve().parent / ".env")

# Constants for input character limits and timestamp format
MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50
TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p WAT"

# Initialize Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def get_wat_time():
    wat_tz = pytz.timezone("Africa/Lagos")
    return datetime.now(wat_tz)


def add_message(name, message):
    timestamp = get_wat_time().strftime(TIMESTAMP_FMT)
    supabase.table("MyGuestBook").insert(
        {"name": name, "message": message, "created_at": timestamp}
    ).execute()


def get_messages():
    response = (
        supabase.table("MyGuestBook")
        .select("*")
        .order("id", desc=True)
        .execute()
    )
    return response.data if response.data else []


def render_message(entry):
    return Article(
        Header(f"Name: {entry['name']}"),
        P(entry["message"]),
        Footer(Small(Em(f"Posted: {entry['created_at']}"))),
    )


# FastHTML initialization
app, rt = fast_app(
    hdrs=(Link(rel="icon", type="image/x-icon", href="/assets/favicon.png"),)
)

# Expose raw ASGI application for Vercel
app = app.app if hasattr(app, "app") else app


def render_message_list():
    messages = get_messages()
    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list",
    )


def render_content():
    form = Form(
        Fieldset(
            Input(
                type="text",
                name="name",
                placeholder="Name",
                required=True,
                maxlength=MAX_NAME_CHAR,
            ),
            Input(
                type="text",
                name="message",
                placeholder="Message",
                required=True,
                maxlength=MAX_MESSAGE_CHAR,
            ),
            Button(
                "Submit",
                type="submit",
                cls="bg-blue-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded",
            ),
            role="group",
        ),
        method="post",
        hx_post="/submit-message",
        hx_target="#message-list",
        hx_swap="outerHTML",
        hx_on__after_request="this.reset()",
    )

    return Div(
        P(Em("Write something nice!")),
        form,
        Div(
            "Made with ❤️ by ",
            A("Lolade", href="https://X.com/read1she2", target="_blank"),
        ),
        Hr(),
        render_message_list(),
    )


@rt("/", methods=["GET"])
def get():
    return Titled("📖 Lolade's Guestbook", render_content())


@rt("/submit-message", methods=["POST"])
def post(name: str, message: str):
    add_message(name, message)
    return render_message_list()


if __name__ == "__main__":
    serve()
    
    
### end of file: main.py