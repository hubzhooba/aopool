import requests
from app.config import GRAPHQL_API_URL  # Import API URL from config

def fetch_latest_transactions(api_url=GRAPHQL_API_URL, limit=100, sort_order="INGESTED_AT_DESC", cursor="", tags=None):
    """
    Fetches the latest transactions from the GraphQL API.
    """
    headers = {"Content-Type": "application/json"}
    
    query = """
    query GetTransactions($limit: Int!, $sortOrder: SortOrder!, $cursor: String, $tags: [TagFilter!]) {
      transactions(
        sort: $sortOrder
        first: $limit
        after: $cursor
        tags: $tags
      ) {
        edges {
          cursor
          node {
            id
            recipient
            owner { address }
            block { timestamp height }
            tags { name value }
            data { size }
          }
        }
      }
    }
    """
    
    variables = {
        "limit": limit,
        "sortOrder": sort_order,
        "cursor": cursor,
        "tags": tags if tags else [{"name": "Data-Protocol", "values": ["ao"]}]
    }

    try:
        response = requests.post(api_url, json={"query": query, "variables": variables}, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "data" not in data or "transactions" not in data["data"]:
            print(f"⚠️ Unexpected API response format: {data}")
            return {}

        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request failed: {e}")
        return {}