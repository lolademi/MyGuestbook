import os
from datetime import datetime
import pytz
from supabase import create_client, Client
from dotenv import load_dotenv
from fasthtml.common import *

#load environment variables
load_dotenv()

# Constants for input character limits and timestamp format
MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50
TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p CET"

#initialize supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def get_cet_time():
    cet_tz = pytz.timezone("CET")
    return datetime.now(cet_tz)


def add_message(name, message):
    timestamp = get_cet_time().strftime(TIMESTAMP_FMT)
    supabase.table("MyGuestbook").insert(
        {"name": name, "message": message, "created_at": timestamp}
    ).execute()

# def get_messages():
#     """Fetch messages from the Supabase database."""
#     response = supabase.table("MyGuestbook").select("*").execute()
#     return response.data if response.data else []

def get_messages():
    # Sort by 'id' in descending order to get the latest entries first
    response = supabase.table("MyGuestbook").select("*").order("id", desc=True).execute()
    return response.data

# def render_message():
#     Article(
#         Header("Name:" "Lolade"),
#         P("Message:" "Hi there"),
#         Footer("Time:" "Today")
#     )
    
# def render_messages():
#     """Render all messages from the database."""
#     messages = get_messages()
#     if not messages:
#         return P("No messages yet. Be the first to leave a message!")
    
#     return Div(
#         *[Article(
#             Header(f"Name: {msg['name']}"),
#             P(f"Message: {msg['message']}"),
#             Footer(f"Time: {msg['created_at']}")
#         ) for msg in messages]
#     )
    
def render_message(entry):
    return (
        Article(
            Header(f"Name: {entry['name']}"),
            P(entry["message"]),
            Footer(Small(Em(f"Posted: {entry['created_at']}"))),
        ),
    )
# globalcss = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css")
app, rt = fast_app(
    hdrs=(Link(rel="icon", type="assets/x-icon", href="/assets/favicon.png"),
        #   (Script(code='',src='https://cdn.tailwindcss.com'), globalcss)
          ),
    )
    
def render_message_list():
        messages = get_messages()
        return Div(
            *[render_message(entry) for entry in messages],
            id="message-list",
    )

    
# def render_content():
#     return Div(
#         Hr(),
#         P(Em("Welcome to Lolade's Guestbook!")),
#         P("Please leave a message below:"),
#         Form(
#             Fieldset(
#                 Label(
#             Input(
#                 name="name",
#                 placeholder="Name",
#                 autocomplete="given-name"
#             )
#         ),
#         Label(
#             Input(
#                 type="text",
#                 name="message",
#                 placeholder="Message",
#                 autocomplete=""
#             )
#         ),
#         Button("Submit", type="submit"),
#         role="group"), 
# ),
#         Hr(),
#         render_messages()
#     )


# @rt("/")
# def get():
#     return Titled("📖 Lolade Guestbook", render_content())
    
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
            Button("Submit", type="submit", cls=
                   "bg-blue-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
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

    
    
serve() 