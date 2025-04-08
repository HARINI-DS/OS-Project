
from datetime import datetime, timedelta

def get_status(start_time_str, end_time_str):
    now = datetime.now().time()
    fmt = "%H:%M"
    start_time = datetime.strptime(start_time_str, fmt).time()
    end_time = datetime.strptime(end_time_str, fmt).time()
    if now < start_time:
        return "Pending"
    elif start_time <= now < end_time:
        return "In Progress"
    else:
        return "Completed"

def read_orders(file_path):
    import csv
    orders = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["prep_time"] = int(row["prep_time"])
            row["priority"] = int(row["priority"])
            row["order_time"] = datetime.strptime(row["order_time"], "%Y-%m-%d %H:%M:%S")
            orders.append(row)
    return orders

def schedule_orders(orders, algorithm="Priority", quantum=5):
    if algorithm == "FCFS":
        orders.sort(key=lambda x: x["order_time"])
    elif algorithm == "SJF":
        orders.sort(key=lambda x: x["prep_time"])
    elif algorithm == "Priority":
        orders.sort(key=lambda x: x["priority"])
    elif algorithm == "Round Robin":
        return round_robin_schedule(orders, quantum)
    current_time = datetime.now()
    scheduled = []
    for order in orders:
        start = current_time
        end = current_time + timedelta(minutes=order["prep_time"])
        scheduled.append({
            "customer_name": order["customer_name"],
            "dish_name": order["dish_name"],
            "prep_time": order["prep_time"],
            "priority": order["priority"],
            "category": order["category"],
            "start_time": start.strftime("%H:%M"),
            "end_time": end.strftime("%H:%M"),
            "status": get_status(start.strftime("%H:%M"), end.strftime("%H:%M"))
        })
        current_time = end
    return scheduled

def round_robin_schedule(orders, quantum=5):
    from copy import deepcopy
    queue = sorted(deepcopy(orders), key=lambda x: x["order_time"])
    current_time = datetime.now()
    remaining_time = {i: order["prep_time"] for i, order in enumerate(queue)}
    scheduled = []
    index_queue = list(range(len(queue)))
    while index_queue:
        i = index_queue.pop(0)
        order = queue[i]
        time_used = min(quantum, remaining_time[i])
        start = current_time
        end = start + timedelta(minutes=time_used)
        scheduled.append({
            "customer_name": order["customer_name"],
            "dish_name": order["dish_name"],
            "prep_time": time_used,
            "priority": order["priority"],
            "category": order["category"],
            "start_time": start.strftime("%H:%M"),
            "end_time": end.strftime("%H:%M"),
            "status": get_status(start.strftime("%H:%M"), end.strftime("%H:%M"))
        })
        current_time = end
        remaining_time[i] -= time_used
        if remaining_time[i] > 0:
            index_queue.append(i)
    return scheduled
