from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.data_fetch import fetch_latest_transactions
from app.config import GRAPHQL_API_URL  

TOKEN_DECIMALS = {
    "0syT13r0s0tgPmIed95bJnuSqaD29HQNN8D3ElLSrsc": ("AO", 1_000_000_000_000),
    "7zH9dlMNoxprab9loshv3Y7WG45DOny_Vrq9KrXObdQ": ("Ethereum-Wrapped USDC", 1_000_000_000_000),
    "xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10": ("wAR", 1_000_000_000_000),
    "NG-0lVX882MG5nhARrSzyprEK6ejonHpdUmaaMPsHE8": ("qAR", 1_000_000_000_000),
}

POOLS = {
    "wTIpisZKMtG5WsLFqQBdoJEObyyeoJQmwWFm1h462D4": "AO/qAR",
    "B6qAwHi2OjZmyFCEU8hV6FZDSHbAOz8r0yy-fBbuTus": "AO/wAR",
    "3biQvRjIp_9Qz1L9D3SJ9laK4akCkP-8bvAo3pQ6jVI": "AO/qAR",
    "FRF1k0BSv0gRzNA2n-95_Fpz9gADq9BGi5PyXKFp6r8": "AO/wAR",
    "OevPKwznmOKv42BgKLOWQhiqiY4MkHQNLfzFgKhQKkU": "AO/wUSDC",
    "QvpGcggxE1EH0xUzL5IEFjkQd1Hdp1FrehGKIiyLczk": "AO/wAR",
    "xKT5_B0-8fpwSUC6VnWggvOzN-mXt28kHVzx4sbvIqo": "AO/wUSDC",
}

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def serve_homepage():
    return FileResponse("app/static/index.html")

@app.get("/filtered-swaps")
async def get_filtered_swaps():
    """Fetches and filters only token swaps involving defined pools and tokens."""
    data = fetch_latest_transactions(GRAPHQL_API_URL, limit=50)

    swaps = []

    for tx in data.get("data", {}).get("transactions", {}).get("edges", []):
        tags = {tag["name"]: tag["value"] for tag in tx["node"].get("tags", [])}
        sender = tx["node"].get("owner", {}).get("address", "Unknown")
        recipient = tx["node"].get("recipient", "")

        # Ensure the recipient is in POOLS and the transaction involves relevant tokens
        if recipient in POOLS and "TokenIn" in tags and "TokenOut" in tags:
            token_in_id = tags["TokenIn"]
            token_out_id = tags["TokenOut"]

            if token_in_id in TOKEN_DECIMALS and token_out_id in TOKEN_DECIMALS:
                token_in_name, token_in_decimal = TOKEN_DECIMALS[token_in_id]
                token_out_name, token_out_decimal = TOKEN_DECIMALS[token_out_id]

                amount_in = int(tags.get("AmountIn", "0")) / token_in_decimal
                amount_out = int(tags.get("AmountOut", "0")) / token_out_decimal

                block_info = tx["node"].get("block") or {}

                swap_transaction = {
                    "Transaction ID": tx["node"]["id"],
                    "Sender": sender,
                    "Pool": POOLS[recipient],
                    "Token Sent": token_in_name,
                    "Token Received": token_out_name,
                    "Amount Sent": amount_in,
                    "Amount Received": amount_out,
                    "Block Timestamp": block_info.get("timestamp", "N/A"),
                    "Block Height": block_info.get("height", "N/A"),
                }
                swaps.append(swap_transaction)

    return {"Token Swaps": swaps}