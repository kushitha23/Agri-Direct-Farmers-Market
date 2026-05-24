from flask import Flask, render_template

app = Flask(__name__)

# ================= HOME =================

@app.route("/")
def home():
    return render_template("register.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

# ================= AUTH =================

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

# ================= MAIN PAGES =================

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/products.html")
def products():
    return render_template("products.html")

@app.route("/cart.html")
def cart():
    return render_template("cart.html")

@app.route("/checkout.html")
def checkout():
    return render_template("checkout.html")

@app.route("/order-success.html")
def orderSuccess():
    return render_template("order-success.html")

@app.route("/order-tracking.html")
def orderTracking():
    return render_template("order-tracking.html")

@app.route("/order-history.html")
def orderHistory():
    return render_template("order-history.html")

# ================= PRODUCT DETAILS =================

@app.route("/apple-details.html")
def appleDetails():
    return render_template("apple-details.html")

@app.route("/carrot-details.html")
def carrotDetails():
    return render_template("carrot-details.html")

@app.route("/fruits-details.html")
def fruitsDetails():
    return render_template("fruits-details.html")

@app.route("/mango-details.html")
def mangoDetails():
    return render_template("mango-details.html")

@app.route("/milk-details.html")
def milkDetails():
    return render_template("milk-details.html")

@app.route("/rice-details.html")
def riceDetails():
    return render_template("rice-details.html")

@app.route("/tomato-details.html")
def tomatoDetails():
    return render_template("tomato-details.html")

@app.route("/vegetables-details.html")
def vegetablesDetails():
    return render_template("vegetables-details.html")

@app.route("/product-details.html")
def productDetails():
    return render_template("product-details.html")

# ================= FARMER =================

@app.route("/farmer-dashboard.html")
def farmerDashboard():
    return render_template("farmer-dashboard.html")

@app.route("/farmer-orders.html")
def farmerOrders():
    return render_template("farmer-orders.html")

@app.route("/add-product.html")
def addProduct():
    return render_template("add-product.html")

# ================= ADMIN =================

@app.route("/admin-dashboard.html")
def adminDashboard():
    return render_template("admin-dashboard.html")

@app.route("/manage-customers.html")
def manageCustomers():
    return render_template("manage-customers.html")

@app.route("/manage-farmers.html")
def manageFarmers():
    return render_template("manage-farmers.html")

@app.route("/manage-products.html")
def manageProducts():
    return render_template("manage-products.html")

@app.route("/reports.html")
def reports():
    return render_template("reports.html")

# ================= CUSTOMER =================

@app.route("/buyer-dashboard.html")
def buyerDashboard():
    return render_template("buyer-dashboard.html")

# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)