from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import get_db_connection

app = Flask(__name__)

app.secret_key = "secret"


# ================= HOME =================

@app.route("/")
def home():
    return render_template("register.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


# ================= AUTH =================

@app.route("/login.html", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["fullname"]

            if user["role"] == "buyer":
                return redirect(url_for("index"))

            elif user["role"] == "farmer":
                return redirect(url_for("farmerDashboard"))

            elif user["role"] == "admin":
                return redirect(url_for("adminDashboard"))

        flash("Invalid Email or Password!", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register.html", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        role = request.form["role"]

        # PASSWORD MATCH CHECK

        if password != confirmPassword:

            flash("Passwords do not match!", "error")

            return redirect(url_for("register"))

        # PASSWORD LENGTH CHECK

        if len(password) < 6:

            flash(
                "Password must contain minimum 6 characters!",
                "error"
            )

            return redirect(url_for("register"))

        # WEAK PASSWORD CHECK

        weak_passwords = [
            "123456",
            "abcdef",
            "qwerty",
            "password"
        ]

        if password.lower() in weak_passwords:

            flash("Choose a stronger password!", "error")

            return redirect(url_for("register"))

        conn = get_db_connection()

        # DUPLICATE CHECK

        existing_user = conn.execute(
            """
            SELECT * FROM users
            WHERE email = ? OR phone = ?
            """,
            (email, phone)
        ).fetchone()

        if existing_user:

            flash(
                "Email or Phone number already exists!",
                "error"
            )

            conn.close()

            return redirect(url_for("register"))

        # INSERT USER

        conn.execute(
            """
            INSERT INTO users
            (fullname, email, phone, password, role)

            VALUES (?, ?, ?, ?, ?)
            """,
            (fullname, email, phone, password, role)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful!", "success")

        return redirect(url_for("login"))

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

    conn = get_db_connection()

    products = conn.execute(
        "SELECT * FROM products"
    ).fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=products
    )


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



@app.route("/product/<int:product_id>")
def productDetails(product_id):

    conn = get_db_connection()

    product = conn.execute(
        """
        SELECT * FROM products
        WHERE id = ?
        """,
        (product_id,)
    ).fetchone()

    conn.close()

    if product is None:
        return "Product Not Found"

    return render_template(
        "product-details.html",
        product=product
    )


# ================= FARMER =================

@app.route("/farmer-dashboard.html")
def farmerDashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("farmer-dashboard.html")


@app.route("/farmer-orders.html")
def farmerOrders():
    return render_template("farmer-orders.html")


@app.route("/add-product.html", methods=["GET", "POST"])
def addProduct():

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]
        description = request.form["description"]
        image = request.form["image"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO products
            (name, category, price, stock, description, image)

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                category,
                price,
                stock,
                description,
                image
            )
        )

        conn.commit()
        conn.close()

        flash(
            "Product Added Successfully!",
            "success"
        )

        return redirect(
            url_for("products")
        )

    return render_template(
        "add-product.html"
    )

# ================= ADMIN =================

@app.route("/admin-dashboard.html")
def adminDashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

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
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully!", "success")

    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)