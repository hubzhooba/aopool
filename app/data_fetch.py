import requests
from app.config import GRAPHQL_API_URL

def fetch_latest_transactions(limit=100, sort_order="INGESTED_AT_DESC", cursor="", tags=None):
    """
    Fetches the latest transactions from the GraphQL API with filtering by tags.
    """
    headers = {"Content-Type": "application/json"}

    query = """
    query GetTransactions($limit: Int!, $sortOrder: SortOrder!, $cursor: String, $tags: [TagFilter!]) {
      transactions(
        sort: $sortOrder
        first: $limit
        after: $cursor
        ingested_at: {min: 1696107600}
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

    response = requests.post(GRAPHQL_API_URL, json={"query": query, "variables": variables}, headers=headers)
    return response.json()