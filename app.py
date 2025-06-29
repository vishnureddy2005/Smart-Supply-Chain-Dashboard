from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import pickle
import requests

app = Flask(__name__)
CORS(app)

# Load AI Model
with open('delay_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Google Distance Matrix API Key
GOOGLE_API_KEY = 'AIzaSyCLHyehvlGHt6bs9spz9fmcm8cA6dhdEvY'  # Your provided key

# Get database connection
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='walmart_sparkathon'
    )

# ✅ Inventory API
@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT product_name, MAX(stock_level) AS stock_level FROM products GROUP BY product_name")
        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

# ✅ Update stock API
@app.route('/update-stock', methods=['POST'])
def update_stock():
    try:
        data = request.json
        product_id = data['product_id']
        new_stock = data['stock_level']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET stock_level=%s WHERE product_id=%s", (new_stock, product_id))
        conn.commit()
        return jsonify({'message': 'Stock updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

# ✅ Add new delivery API with debug prints
@app.route('/add-delivery', methods=['POST'])
def add_delivery():
    conn = None
    try:
        data = request.json
        print('Received Data:', data)  # Debug

        product_id = data['product_id']
        destination = data['destination']
        source = data['origin_address']
        weather_condition = data['weather_condition']
        traffic_level = data['traffic_level']
        holiday_flag = data['holiday_flag']

        # Calculate distance using Google Distance Matrix API
        distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={source}&destinations={destination}&key={GOOGLE_API_KEY}"
        print('Distance API URL:', distance_url)  # Debug

        response = requests.get(distance_url).json()
        print('Google API Response:', response)  # Debug

        if response['status'] != 'OK' or response['rows'][0]['elements'][0]['status'] != 'OK':
            return jsonify({'error': 'Distance calculation failed'}), 400

        distance_text = response['rows'][0]['elements'][0]['distance']['text']
        distance_km = float(distance_text.replace(' km', '').replace(',', ''))
        print('Calculated Distance (km):', distance_km)  # Debug

        traffic_value = {'Low': 1, 'Medium': 2, 'High': 3}.get(traffic_level, 1)
        weather_value = {'Clear': 1, 'Rainy': 2, 'Storm': 3}.get(weather_condition, 1)

        features = [[distance_km, traffic_value, holiday_flag, weather_value]]
        predicted_delay = model.predict(features)[0]
        print('Predicted Delay:', predicted_delay)  # Debug

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO deliveries (product_id, origin_address, destination, distance_km, weather_condition, traffic_level, holiday_flag, predicted_delay_minutes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (product_id, source, destination, distance_km, weather_condition, traffic_level, holiday_flag, predicted_delay))
        conn.commit()
        print('Delivery Inserted Successfully')  # Debug

        return jsonify({'message': 'Added delivery successfully', 'predicted_delay': round(predicted_delay, 2)})
    except Exception as e:
        print('Error:', e)  # Debug
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

# ✅ Deliveries API (only required fields)
@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT delivery_id, origin_address, destination, predicted_delay_minutes
            FROM deliveries
            ORDER BY delivery_id DESC LIMIT 5
        """)
        deliveries = cursor.fetchall()
        print('Fetched Deliveries:', deliveries)  # Debug
        return jsonify(deliveries)
    except Exception as e:
        print('Error fetching deliveries:', e)  # Debug
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
