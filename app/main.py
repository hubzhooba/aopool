@app.get("/filtered-transactions")
async def get_filtered_transactions():
    """Fetches and filters only token swaps and transfers"""
    data = fetch_latest_transactions(limit=50)  # Fetch latest 50 transactions

    swaps = []
    transfers = []

    for tx in data.get("data", {}).get("transactions", {}).get("edges", []):
        tx_tags = {tag["name"]: tag["value"] for tag in tx["node"].get("tags", [])}

        # Identify Token Swaps (Token Y -> Token X)
        if "X-Token-A" in tx_tags and "X-Token-B" in tx_tags:
            swap_transaction = {
                "Transaction ID": tx["node"]["id"],
                "Sender": tx["node"].get("owner", {}).get("address", "Unknown"),
                "Token Sent": tx_tags.get("X-Token-A"),
                "Token Received": tx_tags.get("X-Token-B"),
                "Amount Sent": tx_tags.get("X-PS-AmountIn"),
                "Executed Value": tx_tags.get("X-Executed-Value"),
                "Status": tx_tags.get("X-PS-Status"),
            }
            swaps.append(swap_transaction)

        # Identify Token Transfers (Wallet A -> Wallet B)
        elif "Sender" in tx_tags and "Recipient" in tx_tags and "Quantity" in tx_tags:
            transfer_transaction = {
                "Transaction ID": tx["node"]["id"],
                "Sender": tx_tags["Sender"],
                "Recipient": tx_tags["Recipient"],
                "Amount": tx_tags["Quantity"],
            }
            transfers.append(transfer_transaction)

    return {
        "Token Swaps": swaps,
        "Token Transfers": transfers
    }