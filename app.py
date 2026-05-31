from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
import razorpay
import json

app = Flask(__name__)

app.secret_key = "secret"
import razorpay

RAZORPAY_KEY_ID = "rzp_test_SvF91JWczZnF6v"
RAZORPAY_KEY_SECRET = "v3ey6Vo7k43b7fPAjVwYVwiQ"

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)
@app.route("/create-razorpay-order", methods=["POST"])
def create_razorpay_order():

    amount = int(float(request.form["amount"]) * 100)

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "key": RAZORPAY_KEY_ID
    }

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
            SELECT *
            FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            # CHECK IF USER IS BLOCKED

            if user["is_blocked"] == 1:

                flash(
                    "Your account has been blocked by Admin!",
                    "error"
                )

                return redirect(
                    url_for("login")
                )

            session["user_id"] = user["id"]
            session["role"] = user["role"]
            session["name"] = user["fullname"]

            if user["role"] == "buyer":

                return redirect(
                    url_for("index")
                )

            elif user["role"] == "farmer":

                return redirect(
                    url_for("farmerDashboard")
                )

            elif user["role"] == "admin":

                return redirect(
                    url_for("adminDashboard")
                )

        flash(
            "Invalid Email or Password!",
            "error"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "login.html"
    )




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


@app.route("/create-admin")
def createAdmin():

    conn = get_db_connection()

    admin = conn.execute(
        """
        SELECT *
        FROM users
        WHERE role='admin'
        """
    ).fetchone()

    if not admin:

        conn.execute(
            """
            INSERT INTO users
            (
                fullname,
                email,
                phone,
                password,
                role,
                status,
                is_blocked,
                verified
            )

            VALUES
            (
                'Admin',
                'admin@agridirect.com',
                '9999999999',
                'admin123',
                'admin',
                'Approved',
                0,
                1
            )
            """
        )

        conn.commit()

    conn.close()

    return "Admin Created Successfully"


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

@app.route("/reject-order/<int:order_id>")
def rejectOrder(order_id):

    conn = get_db_connection()

    conn.execute(
        "UPDATE orders SET status=? WHERE id=?",
        ("Rejected", order_id)
    )

    conn.commit()

    return redirect("/farmer-orders.html")

@app.route("/farmer-orders.html")
def farmerOrders():

    farmer_id = session["user_id"]

    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE farmer_id = ?
        ORDER BY id DESC
        """,
        (farmer_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "farmer-orders.html",
        orders=orders
    )

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

    farmer_id = session["user_id"]

    conn = get_db_connection()

    total_products = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM products
        WHERE farmer_id = ?
        """,
        (farmer_id,)
    ).fetchone()["total"]

    total_orders = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM orders
        WHERE farmer_id = ?
        """,
        (farmer_id,)
    ).fetchone()["total"]

    total_revenue = conn.execute(
        """
        SELECT COALESCE(SUM(total_price),0) as revenue
        FROM orders
        WHERE farmer_id = ?
        AND status IN ('Delivered','Completed')
        """,
        (farmer_id,)
    ).fetchone()["revenue"]

    pending_orders = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM orders
        WHERE farmer_id = ?
        AND status IN
        (
            'Paid',
            'Pending Payment',
            'Accepted',
            'Shipped'
        )
        """,
        (farmer_id,)
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "farmer-dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        pending_orders=pending_orders
    )
@app.route("/update-order-status/<int:order_id>/<status>")
def updateOrderStatus(order_id, status):

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (status, order_id)
    )

    conn.commit()
    conn.close()

    return redirect("/farmer-orders.html")


@app.route("/add-product.html", methods=["GET", "POST"])
def addProduct():

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]
        description = request.form["description"]
        image = request.form["image"]

        farmer_id = session.get("user_id")

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO products
            (
                name,
                category,
                price,
                stock,
                description,
                image,
                farmer_id
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                category,
                price,
                stock,
                description,
                image,
                farmer_id
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
@app.route("/farmer-products.html")
def farmerProducts():

    if "user_id" not in session:
        return redirect(url_for("login"))

    farmer_id = session["user_id"]

    conn = get_db_connection()

    products = conn.execute(
        """
        SELECT *
        FROM products
        WHERE farmer_id = ?
        ORDER BY id DESC
        """,
        (farmer_id,)
    ).fetchall()

    total_products = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM products
        WHERE farmer_id = ?
        """,
        (farmer_id,)
    ).fetchone()["total"]

    out_of_stock = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM products
        WHERE farmer_id = ?
        AND stock = 0
        """,
        (farmer_id,)
    ).fetchone()["total"]

    available_products = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM products
        WHERE farmer_id = ?
        AND stock > 0
        """,
        (farmer_id,)
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "farmer-products.html",
        products=products,
        total_products=total_products,
        out_of_stock=out_of_stock,
        available_products=available_products
    )
@app.route("/show-products")
def showProducts():

    conn = get_db_connection()

    products = conn.execute(
        """
        SELECT id, name, farmer_id
        FROM products
        """
    ).fetchall()

    conn.close()

    return str([dict(product) for product in products])
@app.route("/show-farmers")
def showFarmers():

    conn = get_db_connection()

    farmers = conn.execute(
        """
        SELECT id, fullname, email
        FROM users
        WHERE role='farmer'
        """
    ).fetchall()

    conn.close()

    return str([dict(farmer) for farmer in farmers])
import json

@app.route("/save-order", methods=["POST"])
def saveOrder():

    buyer_id = session.get("user_id")

    payment_method = request.form["payment_method"]

    if payment_method == "cod":
        status = "Pending Payment"
    else:
        status = "Paid"

    cart = json.loads(
        request.form["cart"]
    )

    conn = get_db_connection()

    for item in cart:

        product = conn.execute(
            """
            SELECT farmer_id
            FROM products
            WHERE name = ?
            """,
            (item["name"],)
        ).fetchone()

        farmer_id = None

        if product:
            farmer_id = product["farmer_id"]

        conn.execute(
            """
            INSERT INTO orders
            (
                buyer_id,
                farmer_id,
                product_name,
                quantity,
                total_price,
                payment_method,
                status
            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                buyer_id,
                farmer_id,
                item["name"],
                item["quantity"],
                float(item["price"]) * int(item["quantity"]),
                payment_method,
                status
            )
        )

    conn.commit()
    conn.close()

    return "Order Saved Successfully"
@app.route("/my-orders")
def myOrders():

    buyer_id = session.get("user_id")

    if not buyer_id:
        return redirect(url_for("login"))

    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE buyer_id = ?
        ORDER BY id DESC
        """,
        (buyer_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "my-orders.html",
        orders=orders
    )
@app.route("/track-order/<int:order_id>")
def trackOrder(order_id):

    conn = get_db_connection()

    order = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    conn.close()

    return render_template(
        "order-tracking.html",
        order=order
    )
@app.route("/check-session")
def checkSession():

    return str({
        "user_id": session.get("user_id"),
        "name": session.get("name"),
        "role": session.get("role")
    })
@app.route("/confirm-receipt/<int:order_id>")
def confirmReceipt(order_id):

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE orders
        SET status = 'Completed'
        WHERE id = ?
        """,
        (order_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/my-orders")
@app.route("/ship-order/<int:order_id>", methods=["GET", "POST"])
def shipOrder(order_id):

    conn = get_db_connection()

    if request.method == "POST":

        estimated_date = request.form["estimated_date"]
        estimated_time = request.form["estimated_time"]

        conn.execute(
            """
            UPDATE orders
            SET
                status='Shipped',
                estimated_date=?,
                estimated_time=?
            WHERE id=?
            """,
            (
                estimated_date,
                estimated_time,
                order_id
            )
        )

        conn.commit()
        conn.close()

        return redirect("/farmer-orders.html")

    order = conn.execute(
        """
        SELECT *
        FROM orders
        WHERE id=?
        """,
        (order_id,)
    ).fetchone()

    conn.close()

    return render_template(
        "ship-order.html",
        order=order
    )
# ================= ADMIN =================

@app.route("/admin-dashboard.html")
def adminDashboard():

    conn = get_db_connection()

    total_farmers = conn.execute(
        "SELECT COUNT(*) as total FROM users WHERE role='farmer'"
    ).fetchone()["total"]

    total_buyers = conn.execute(
        "SELECT COUNT(*) as total FROM users WHERE role='buyer'"
    ).fetchone()["total"]

    total_orders = conn.execute(
        "SELECT COUNT(*) as total FROM orders"
    ).fetchone()["total"]

    total_products = conn.execute(
        "SELECT COUNT(*) as total FROM products"
    ).fetchone()["total"]

    revenue = conn.execute(
        """
        SELECT COALESCE(SUM(total_price),0) as revenue
        FROM orders
        WHERE status='Delivered'
        """
    ).fetchone()

    total_revenue = revenue["revenue"]
    recent_farmers = conn.execute(
    """
    SELECT *
    FROM users
    WHERE role='farmer'
    ORDER BY id DESC
    LIMIT 5
    """
).fetchall()

    conn.close()

    return render_template(
    "admin-dashboard.html",
    total_farmers=total_farmers,
    total_buyers=total_buyers,
    total_orders=total_orders,
    total_products=total_products,
    total_revenue=total_revenue,
    recent_farmers=recent_farmers
)



@app.route("/manage-buyers.html")
def manageBuyers():

    conn = get_db_connection()

    buyers = conn.execute(
        """
        SELECT *
        FROM users
        WHERE role='buyer'
        ORDER BY id DESC
        """
    ).fetchall()

    total_buyers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='buyer'
        """
    ).fetchone()["total"]

    blocked_buyers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='buyer'
        AND is_blocked = 1
        """
    ).fetchone()["total"]

    active_buyers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='buyer'
        AND is_blocked = 0
        """
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "manage-buyers.html",
        buyers=buyers,
        total_buyers=total_buyers,
        blocked_buyers=blocked_buyers,
        active_buyers=active_buyers
    )





@app.route("/manage-farmers.html")
def manageFarmers():

    conn = get_db_connection()

    farmers = conn.execute(
        """
        SELECT *
        FROM users
        WHERE role='farmer'
        """
    ).fetchall()

    total_farmers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='farmer'
        """
    ).fetchone()["total"]

    approved_farmers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='farmer'
        AND status='Approved'
        """
    ).fetchone()["total"]

    pending_farmers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='farmer'
        AND status='Pending'
        """
    ).fetchone()["total"]

    rejected_farmers = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM users
        WHERE role='farmer'
        AND status='Rejected'
        """
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "manage-farmers.html",
        farmers=farmers,
        total_farmers=total_farmers,
        approved_farmers=approved_farmers,
        pending_farmers=pending_farmers,
        rejected_farmers=rejected_farmers
    )



@app.route("/manage-orders.html")
def manageOrders():

    conn = get_db_connection()

    orders = conn.execute(
        """
        SELECT *
        FROM orders
        ORDER BY id DESC
        """
    ).fetchall()

    total_orders = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM orders
        """
    ).fetchone()["total"]

    pending_orders = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM orders
        WHERE status != 'Delivered'
        AND status != 'Rejected'
        
        """
    ).fetchone()["total"]

    delivered_orders = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM orders
        WHERE status = 'Delivered'
        """
    ).fetchone()["total"]

    rejected_orders = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM orders
        WHERE status = 'Rejected'
        """
    ).fetchone()["total"]

    total_revenue = conn.execute(
        """
        SELECT COALESCE(SUM(total_price),0) as revenue
        FROM orders
        WHERE status = 'Delivered'
        """
    ).fetchone()["revenue"]

    conn.close()

    return render_template(
        "manage-orders.html",
        orders=orders,
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        rejected_orders=rejected_orders,
        total_revenue=total_revenue
    )



@app.route("/delete-product/<int:product_id>")
def deleteProduct(product_id):

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    conn.commit()
    conn.close()

    flash(
        "Product Deleted Successfully!",
        "success"
    )

    return redirect(
        url_for("manageProducts")
    )


@app.route("/manage-products.html")
def manageProducts():

    conn = get_db_connection()

    products = conn.execute(
        """
        SELECT *
        FROM products
        ORDER BY id DESC
        """
    ).fetchall()

    total_products = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM products
        """
    ).fetchone()["total"]

    out_of_stock = conn.execute(
        """
        SELECT COUNT(*) as total
        FROM products
        WHERE stock = 0
        """
    ).fetchone()["total"]

    conn.close()

    return render_template(
        "manage-products.html",
        products=products,
        total_products=total_products,
        out_of_stock=out_of_stock
    )




@app.route("/reports.html")
def reports():
    return render_template("reports.html")




from flask import request

@app.route("/block-user/<int:user_id>")
def blockUser(user_id):

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE users
        SET is_blocked = 1
        WHERE id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return redirect(request.referrer)


@app.route("/unblock-user/<int:user_id>")
def unblockUser(user_id):

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE users
        SET is_blocked = 0
        WHERE id = ?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    return redirect(request.referrer)




@app.route("/check-users")
def checkUsers():

    conn = get_db_connection()

    users = conn.execute(
        """
        SELECT id,
               fullname,
               email,
               password,
               role
        FROM users
        """
    ).fetchall()

    conn.close()

    return str([dict(user) for user in users])


# ================= ADMIN FARMER MANAGEMENT =================

@app.route("/approve-farmer/<int:user_id>")
def approveFarmer(user_id):

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE users
        SET status='Approved'
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    flash("Farmer Approved Successfully!", "success")

    return redirect("/manage-farmers.html")


@app.route("/reject-farmer/<int:user_id>")
def rejectFarmer(user_id):

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE users
        SET status='Rejected'
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()

    flash("Farmer Rejected!", "error")

    return redirect("/manage-farmers.html")




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