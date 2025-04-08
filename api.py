from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from scheduler import read_orders, schedule_orders
from datetime import datetime
import csv
import os
import webbrowser

app = Flask(__name__, static_folder="static")
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/orders", methods=["GET"])
def get_orders():
    algorithm = request.args.get("algorithm", "Priority")
    quantum = int(request.args.get("quantum", 5))
    orders = read_orders(DATA_PATH)
    scheduled = schedule_orders(orders, algorithm, quantum)
    return jsonify({"algorithm": algorithm, "orders": scheduled})

@app.route("/api/orders", methods=["POST"])
def add_order():
    data = request.json
    with open(DATA_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            data["customer_name"],
            data["dish_name"],
            data["prep_time"],
            data["category"],
            data["priority"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
    return jsonify({"message": "Order added"}), 201

if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}/"
    webbrowser.open(url)
    app.run(debug=True, port=port)
