<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alam Chicken Corner - Patna</title>
<style>
    body { font-family: 'Roboto', Arial; margin: 0; background: #f1f3f6; }
    .navbar { background: #d32f2f; color: white; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; }
    .navbar img { width: 40px; height: 40px; border-radius: 50%; }
    .navbar input { width: 50%; padding: 8px; border-radius: 4px; border: none; }
    .cart-btn { background: white; color: #d32f2f; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer; }
    .banner { background: url('https://images.unsplash.com/photo-1565557623262-aab9914dbbef?q=80&w=1200') center/cover; color: white; text-align: center; padding: 60px 20px; }
    .banner h1 { font-size: 32px; text-shadow: 2px 2px 4px black; }
    .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
    .category { display: flex; gap: 15px; margin-bottom: 20px; overflow-x: auto; }
    .cat-item { background: white; padding: 10px 20px; border-radius: 8px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
    .product { background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
    .product img { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; }
    .price { color: #d32f2f; font-size: 18px; font-weight: bold; }
    .btn { background: #d32f2f; color: white; padding: 10px; border: none; width: 100%; border-radius: 4px; cursor: pointer; margin-top: 10px; }
    .footer { background: #172337; color: white; text-align: center; padding: 20px; margin-top: 30px; }
</style>
</head>
<body>
    <div class="navbar">
        <img src="{{ url_for('static', filename='logo.png') }}">
        <input type="text" placeholder="Search for Chicken, Biryani, Rolls...">
        <div class="cart-btn" onclick="checkout()">Cart (<span id="cart-count">0</span>)</div>
    </div>

    <div class="banner">
        <h1>Alam Chicken Corner</h1>
        <p>Patna me 30-40 Min me Garam Garam Delivery</p>
    </div>

    <div class="container">
        <div class="category">
            <div class="cat-item">🍗 All</div>
            <div class="cat-item">🍛 Biryani</div>
            <div class="cat-item">🍲 Curry</div>
            <div class="cat-item">🌯 Rolls</div>
            <div class="cat-item">🔥 Starters</div>
        </div>

        <div class="product-grid">
            {% for item in menu %}
            <div class="product">
                <img src="https://source.unsplash.com/300x200/?chicken,food">
                <h3>{{ item.name }}</h3>
                <p>{{ item.desc }}</p>
                <p class="price">₹{{ item.price }}</p>
                <button class="btn" onclick="addToCart({{ item.id }}, '{{ item.name }}', {{ item.price }})">ADD TO CART</button>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="footer">
        <p>📍 Alam Chicken Corner, giridih, jharkhand</p>
        <p>Call: +91 9229280318 | WhatsApp Order</p>
    </div>

<script>
let cart = [];
function addToCart(id, name, price) {
    let item = cart.find(i => i.id === id);
    if(item) { item.qty++; } else { cart.push({id, name, price, qty: 1}); }
    document.getElementById('cart-count').innerText = cart.reduce((sum, i) => sum + i.qty, 0);
    alert(name + " cart me add ho gaya!");
}
function checkout() {
    let name = prompt("Apna Naam:");
    let address = prompt("Delivery Pata:");
    if(!name || !address) return;
    fetch('/place_order', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({cart, name, address})})
    .then(res => res.json()).then(data => { window.open(data.url, '_blank'); });
}
</script>
</body>
</html>
