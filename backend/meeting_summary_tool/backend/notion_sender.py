import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

def create_notion_task(task: str, assignee: str = "", deadline: str = ""):
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Task": {"title": [{"text": {"content": task}}]},
            "Assigned To": {"rich_text": [{"text": {"content": assignee}}]},
            "Deadline": {"date": {"start": deadline}} if deadline else {}
        }
    )