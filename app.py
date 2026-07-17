from flask import Flask, render_template, request, jsonify
import urllib.parse

app = Flask(__name__)

WHATSAPP_NUMBER = "919229280318"  # apna number 91 ke saath

menu = [
    {"id": 1, "name": "Chicken Biryani", "desc": "Basmati Rice + Raita", "price": 180, "cat": "Biryani"},
    {"id": 2, "name": "Chicken Curry", "desc": "4 Piece + 2 Roti", "price": 160, "cat": "Curry"},
    {"id": 3, "name": "Chicken Roll", "desc": "Spicy Mayo Roll", "price": 80, "cat": "Rolls"},
    {"id": 4, "name": "Chicken 65", "desc": "200gm Crispy", "price": 140, "cat": "Starters"},
]

@app.route('/')
def home():
    return render_template('index.html', menu=menu)

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    cart = data['cart']
    name = data['name']
    address = data['address']
    
    message = f"*New Order - Alam Chicken Corner*\n\n"
    message += f"*Name:* {name}\n*Address:* {address}\n\n*Order:*\n"
    total = 0
    for item in cart:
        message += f"- {item['name']} x {item['qty']} = ₹{item['price']*item['qty']}\n"
        total += item['price']*item['qty']
    message += f"\n*Total: ₹{total}*"
    
    encoded_msg = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_msg}"
    return jsonify({"url": whatsapp_url})

if __name__ == '__main__':
    app.run(debug=True)
