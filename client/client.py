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
            print(f"ID: {order['id']} | Name: {order['client_name']} | Type: {order['paper_type']} | Pages: {order['pages']} | Total Cost: {order['total_cost']}")

    else:
        print("Fetch Error")

def search(args):
    print("Search by ID")

    try:
        order_id = int(args[1])
    except ValueError:
        print("Invalid ID")
        return
    
    response = requests.get(f"{url}/orders/{order_id}")

    if response.status_code == 200:
        data = response.json()
        
        print(f"Name: {data['client_name']} | Type: {data['paper_type']} | Pages: {data['pages']} | Total Cost: {data['total_cost']}")
    else:
        print("Not Found")

def order(args):
    print("Create Order")

    client_name, paper_type, pages = args[1], args[2], int(args[3]) 

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

def main():
    
    cmnd = sys.argv[1]


    if cmnd == "order":
        order (sys.argv[1:])
    
    elif cmnd == "search":
        search (sys.argv[1:])

    elif cmnd == "view":
        view()

    else:
        print("Invalid Format")

if __name__ == "__main__":
    main()