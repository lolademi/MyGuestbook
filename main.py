import os
from supabase import create_client
from dotenv import load_dotenv
from fasthtml.common import *

#load environment variables
load_dotenv()

#initialize supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app,rt = fast_app()

def get_messages():
    """Fetch messages from the Supabase database."""
    response = supabase.table("MyGuestbook").select("*").execute()
    return response.data if response.data else []


# def render_message():
#     Article(
#         Header("Name:" "Lolade"),
#         P("Message:" "Hi there"),
#         Footer("Time:" "Today")
#     )
    
def render_messages():
    """Render all messages from the database."""
    messages = get_messages()
    if not messages:
        return P("No messages yet. Be the first to leave a message!")
    
    return Div(
        *[Article(
            Header(f"Name: {msg['name']}"),
            P(f"Message: {msg['message']}"),
            Footer(f"Time: {msg['created_at']}")
        ) for msg in messages]
    )
    
def render_content():
    return Div(
        Hr(),
        P(Em("Welcome to Lolade's Guestbook!")),
        P("Please leave a message below:"),
        Form(
            Fieldset(
                Label(
            "Name",
            Input(
                name="name",
                placeholder="Name",
                autocomplete="given-name"
            )
        ),
        Label(
            "Message",
            Input(
                type="text",
                name="message",
                placeholder="Message",
                autocomplete=""
            )
        ),
        Button("Submit", type="submit"),
        role=""), 
),
        Hr(),
        render_messages()
    )


@rt("/")
def get():
    return Titled("📖 Lolade Guestbook", render_content())
    
    
    
serve() 
