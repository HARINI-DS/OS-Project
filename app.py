from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from scheduler import read_orders, schedule_orders
from datetime import datetime
import csv
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# File path for the orders CSV
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def serve_static_file(path):
    return send_from_directory("static", path)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
