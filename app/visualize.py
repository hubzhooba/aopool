import networkx as nx
import matplotlib.pyplot as plt

def create_bubblemap(data):
    G = nx.DiGraph()
    
    for tx in data.get("data", {}).get("transactions", {}).get("edges", []):
        sender = tx["node"]["owner"]["address"] if "owner" in tx["node"] else "Unknown"
        print(f"🔍 Extracted Sender for Tx {tx['node']['id']}: {sender}")
        recipient = tx["node"].get("recipient", "Unknown Recipient")
        G.add_edge(sender, recipient)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_size=3000, node_color="lightblue", edge_color="gray", font_size=10, font_weight='bold')
    plt.title("AO Token Transaction BubbleMap")

    # Save the image instead of showing it
    plt.savefig("/workspaces/aopool/bubblemap.png")  # Adjust the path as needed
    print("Bubblemap saved as bubblemap.png")

if __name__ == "__main__":
    sample_data = {
        "data": {
            "transactions": {
                "edges": [
                    {"node": {"owner": {"address": "wallet1"}, "recipient": "wallet2"}},
                    {"node": {"owner": {"address": "wallet2"}, "recipient": "wallet3"}},
                    {"node": {"owner": {"address": "wallet3"}, "recipient": "wallet1"}},
                ]
            }
        }
    }
    create_bubblemap(sample_data)