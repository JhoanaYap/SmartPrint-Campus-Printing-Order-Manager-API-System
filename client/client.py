#!C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe

import sys
import requests

url = "http://127.0.0.1:8000"

def view():
    print("List of Orders")
    response = requests.get(f"{url}/orders")

    if response.status_code == 200:
        data = response.json()
        orders_list = data.get("orders", []) 

        for order in orders_list:
            print(f"ID: {order['id']} | Name: {order['client_name']} | Type: {order['paper_type']} | Pages: {order['pages']} | Total Cost: {order['total_cost']} | Status: {order.get('status', 'N/A')}")
    else:
        print("Fetch Error")

def search(args):
    print("Search by ID")

    try:
        order_id = int(args[0])
    except (IndexError, ValueError):
        print("Invalid ID. Usage: python client.py search <id>")
        return
    
    response = requests.get(f"{url}/orders/{order_id}")

    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['client_name']} | Type: {data['paper_type']} | Pages: {data['pages']} | Total Cost: {data['total_cost']} | Status: {data.get('status', 'N/A')}")
    else:
        print("Not Found")

def order(args):
    print("Create Order")

    try:
        client_name, paper_type, pages = args[0], args[1], int(args[2]) 
    except (IndexError, ValueError):
        print("Invalid Format. Usage: python client.py order <name> <type> <pages>")
        return

    data = {
        "client_name": client_name,
        "paper_type": paper_type,
        "pages": pages
    } 

    response = requests.post(f"{url}/orders", json=data)

    if response.status_code == 200:
        print("Order Completed, Total Cost: ", response.json().get("total_cost"))
    else:
        print("Order Not Processed!", response.json().get("detail", "Unknown Error"))

def pricing():
    print("Printing Prices")
    response = requests.get(f"{url}/pricing")

    if response.status_code == 200:
        prices = response.json()
        for paper, cost in prices.items():
            print(f"- {paper}: {cost}")
    else:
        print("Fetch Error")

def update(args):
    print("Update Order Status")
    
    try:
        order_id = int(args[0])
        status = args[1].lower()
    except (IndexError, ValueError):
        print("Invalid Format. Usage: python client.py update <id> <status>")
        print("Valid statuses: pending, completed, cancelled")
        return

    if status not in ["pending", "completed", "cancelled"]:
        print("Invalid status! Must be 'pending', 'completed', or 'cancelled'.")
        return

    data = {"status": status}
    response = requests.put(f"{url}/orders/{order_id}/status", json=data)

    if response.status_code == 200:
        print(f"Order {order_id} successfully updated to '{status}'.")
    else:
        print("Update Failed!", response.json().get("detail", "Unknown Error"))

def delete(args):
    print("Delete Order")
    
    try:
        order_id = int(args[0])
    except (IndexError, ValueError):
        print("Invalid ID. Usage: python client.py delete <id>")
        return

    response = requests.delete(f"{url}/orders/{order_id}")

    if response.status_code == 200:
        print(f"Order {order_id} deleted successfully.")
    else:
        print("Delete Failed!", response.json().get("detail", "Unknown Error"))

def main():
    if len(sys.argv) < 2:
        print("Please provide a command (view, search, order, pricing, update, delete)")
        return

    cmnd = sys.argv[1].lower()
    args = sys.argv[2:] 
    if cmnd == "order":
        order(args)
    elif cmnd == "search":
        search(args)
    elif cmnd == "view":
        view()
    elif cmnd == "pricing":
        pricing()
    elif cmnd == "update":
        update(args)
    elif cmnd == "delete":
        delete(args)
    else:
        print("Invalid Command Format")

if __name__ == "__main__":
    main()