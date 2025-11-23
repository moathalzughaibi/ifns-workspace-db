import notion_client
import inspect
from notion_client.api_endpoints import DatabasesEndpoint as D

print("module:", inspect.getfile(notion_client))
print("has_query_on_class:", hasattr(D, "query"))
