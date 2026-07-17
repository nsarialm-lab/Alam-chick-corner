from flask import Flask, request, session, redirect, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = "alamsecret123"

# Database banana
conn = sqlite3.connect("orders.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS orders 
             (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, items TEXT, total TEXT, address TEXT)''')
conn.commit()

# Menu
MENU = [
    {'id': 1, 'name': 'Chicken Biryani', 'price': 180},
    {'id': 2, 'name': 'Chicken Curry', 'price': 220},
    {'id': 3, 'name': 'Tandoori Roti', 'price': 15},
    {'id': 4, 'name': 'Chicken Roll', 'price': 90},
    {'id': 5, 'name': 'Chilli Chicken', 'price': 200}
]

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session['name'] = request.form['name']
        session['phone'] = request.form['phone']
        return redirect("/menu")
    return '''
    <div style="text-align:center;margin-top:100px">
    <h2>🍗 Alam Chick Corner</h2>
    <form method="post">
    <input name="name" placeholder="Aapka Naam" required><br><br>
    <input name="phone" placeholder="Mobile Number" required><br><br>
    <button>Login</button>
    </form>
    </div>
    <style>input,button{padding:10px;width:200px} button{background:orange;color:white;border:0}</style>
    '''

# Menu Page
@app.route("/menu")
def menu():
    menu_html = ""
    for item in MENU:
        menu_html += f"<div><b>{item['name']}</b> - ₹{item['price']} <a href='/add/{item['id']}'>+ Add</a></div><br>"
    return f'''
    <div style="padding:20px">
    <h2>Menu</h2>
    {menu_html}
    <a href="/cart">🛒 Cart Dekho</a>
    </div>
    '''

# Cart me add karna
@app.route("/add/<int:item_id>")
def add(item_id):
    cart = session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session['cart'] = cart
    return redirect("/menu")

# Cart Page
@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart = session.get('cart', {})
    if request.method == "POST":
        address = request.form['address']
        
        items_text = ""
        total = 0
        for id, qty in cart.items():
            if qty > 0:
                item = next(i for i in MENU if i['id'] == int(id))
                items_text += f"{item['name']} x {qty}, "
                total += item['price'] * qty
        
        c.execute("INSERT INTO orders (name, phone, items, total, address) VALUES (?,?,?,?,?)",
                  (session['name'], session['phone'], items_text, f"₹{total}", address))
        conn.commit()

        # WhatsApp link
        msg = f"Naya Order!%0ANaam:{session['name']}%0APhone:{session['phone']}%0AItems:{items_text}%0ATotal:₹{total}%0APata:{address}"
        wa_link = f"https://api.whatsapp.com/send?phone=919229280318&text={msg}"
        session['cart'] = {}
        return f'<div style="text-align:center;margin-top:50px"><h2>✅ Order Ho Gaya!</h2><a href="{wa_link}" class="wa-btn">WhatsApp pe Bhejein</a><br><br><a href="/menu">Aur Order Karein</a></div><style>.wa-btn{{background:#25D366;padding:12px 20px;color:white;text-decoration:none;border-radius:5px;font-size:18px}}</style>'

    cart_html = ""
    total = 0
    for id, qty in cart.items():
        if qty > 0:
            item = next(i for i in MENU if i['id'] == int(id))
            cart_html += f"<div>{item['name']} x {qty} = ₹{item['price']*qty}</div>"
            total += item['price'] * qty
    
    return f'''
    <div style="padding:20px">
    <h2>Aapka Cart</h2>
    {cart_html}
    <h3>Total: ₹{total}</h3>
    <form method="post">
    <textarea name="address" placeholder="Delivery Address" required></textarea><br><br>
    <button>Order Confirm</button>
    </form>
    </div>
    <style>textarea{{width:90%;height:80px;padding:10px}} button{{background:green;color:white;padding:10px 20px;border:0}}</style>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
