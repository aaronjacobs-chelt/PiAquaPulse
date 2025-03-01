from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

# Function to read the latest data from CSV
def read_latest_data():
    try:
        with open("river_data.csv", "r") as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                return reader[-1]  # Last row (latest data)
    except FileNotFoundError:
        return None
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    latest_data = read_latest_data()
    if latest_data:
        return jsonify({
            "timestamp": latest_data[0],
            "temperature": latest_data[1],
            "pH": latest_data[2],
            "turbidity": latest_data[3],
            "gps": latest_data[4]
        })
    return jsonify({"error": "No data available"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
