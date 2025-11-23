from notion_client import Client

c = Client(auth="dummy")
print("has databases.query:", hasattr(c.databases, "query"))
