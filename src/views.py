from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from .algorithms import hill_climb, get_reorder_point, plot_points
from datetime import datetime, timezone
from sqlalchemy import or_
from .model import Product
from math import ceil
from . import db

views = Blueprint("views", __name__)

# GET WEBPAGES
@views.route("/")
def home():
    return render_template("index.html")

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/tnc")
def tnc():
    return render_template("tnc.html")

@views.route("/dashboard")
def dashboard():
    products = Product.query.all()
    out_of_stock = sum(1 for product in products if product.qty_in_stock < 1)
    low_stock = sum(1 for product in products if product.reorder_point < product.qty_in_stock <= (product.reorder_point + 10))
    reorder_stock = sum(1 for product in products if product.qty_in_stock <= product.reorder_point)
    
    return render_template("dashboard.html", 
                           products=products, 
                           out_of_stock=out_of_stock, 
                           low_stock=low_stock, 
                           reorder_stock=reorder_stock)

# FUNCTIONAL ROUTES #

# GET ONE PRODUCT
@views.route("/product/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return ({"id": product.id, 
                 "name": product.name, 
                 "unit_price": product.unit_price, 
                 "qty_in_stock": product.qty_in_stock, 
                 "reorder_point": product.reorder_point, 
                 "reorder_quantity": product.reorder_quantity, 
                 "restock_date": product.restock_date, 
                 "lead_time": product.lead_time,
                 "setup_cost": product.setup_cost,
                 "ordering_cost": product.ordering_cost,
                 "holding_cost": product.holding_cost})
    return ({"results": "error"})

# ADD NEW PRODUCT
@views.route("/add", methods=["POST"])
def add_entry():
    name = request.form.get('name')
    unit_price = request.form.get('unit_price')
    qty_in_stock = request.form.get('qty_in_stock')
    reorder_point = request.form.get('reorder_point')
    reorder_quantity = request.form.get('reorder_quantity')
    restock_date_str = request.form.get('restock_date')
    if restock_date_str:
        restock_date = datetime.strptime(restock_date_str, '%Y-%m-%d').date()
    else:
        restock_date = datetime.now(timezone.utc).date()

    lead_time = request.form.get('lead_time')
    setup_cost = request.form.get('setup_cost')
    ordering_cost = request.form.get('ordering_cost')
    holding_cost = request.form.get('holding_cost')

    new_entry = Product(name=name, 
                        unit_price=unit_price, 
                        qty_in_stock=qty_in_stock, 
                        reorder_point=reorder_point, 
                        reorder_quantity=reorder_quantity, 
                        restock_date=restock_date, 
                        lead_time=lead_time,
                        setup_cost=setup_cost,
                        ordering_cost=ordering_cost,
                        holding_cost=holding_cost)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('views.dashboard'))

# UPDATE PRODUCT (save changes)
@views.route('/update', methods=['POST'])
def update():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        product_name = data.get('name')
        price = float(data.get('price'))
        stock = int(data.get('stock'))
        rop = int(data.get('rop'))
        roq = int(data.get('roq'))
        setup_cost = float(data.get('setup_cost')) if 'setup_cost' in data else None
        ordering_cost = float(data.get('ordering_cost')) if 'ordering_cost' in data else None
        holding_cost = float(data.get('holding_cost')) if 'holding_cost' in data else None
        lead_time = int(data.get('lead_time')) if 'lead_time' in data else None

        # Update product in the database
        product = Product.query.get(product_id)
        if product:
            product.name = product_name
            product.unit_price = price
            product.qty_in_stock = stock
            product.reorder_point = rop
            product.reorder_quantity = roq
            if setup_cost is not None:
                product.setup_cost = setup_cost
            if ordering_cost is not None:
                product.ordering_cost = ordering_cost
            if holding_cost is not None:
                product.holding_cost = holding_cost
            if lead_time is not None:
                product.lead_time = lead_time

            db.session.commit()
            return jsonify({'message': 'Product updated successfully'})

        else:
            return jsonify({'error': 'Product not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE PRODUCT
@views.route("/delete/<int:id>", methods=["DELETE"])
def delete_entry(id):
    entry = Product.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return ({"results": "success"})
    return ({"results": "error"})

# OPTIMIZE PRODUCT (uses hill climb and ROP)
@views.route("/optimize", methods=["POST"])
def optimize_product():
    try:
        data = request.get_json()
        demand = int(data.get('total_demand'))
        setup_cost = float(data.get('setup_cost'))
        ordering_cost = float(data.get('ordering_cost'))
        holding_cost = float(data.get('holding_cost'))
        lead_time = int(data.get('lead_time'))
        reorder_point = int(data.get('updateROP'))
        reorder_quantity = int(data.get('updateROQ'))
        
        print(data)

        product_id = int(data.get('product_id'))
        product = Product.query.get(product_id)
        if product is None:
            raise ValueError(f"Product with id {product_id} not found.")

        # Calculate Standard Reorder Point Formula
        start_date = product.restock_date
        end_date = datetime.now(timezone.utc).date()
        last_restock = (end_date - start_date).days 
        if demand == 0:
            demand = 1

        if last_restock == 0:
            last_restock = 1

        reorder_point = ceil(get_reorder_point(demand, lead_time, last_restock))

        # Run Steepest-Hill Climb Algorithm
        optimized_quantity, optimized_cost, order_quantities, costs, iterations = hill_climb(
            initial_solution=reorder_quantity,
            setup_cost=setup_cost,
            holding_cost=holding_cost,
            demand=demand,
            step_size=5,
            product_cost=ordering_cost,
            discounts_included=True,
            maximum=1000
        )

        # For data visualization
        # plot_points(order_quantities, costs)

        result = {
            'optimized_quantity': optimized_quantity,
            'optimized_rop': reorder_point,
            'optimized_cost': optimized_cost,
            'iterations': iterations
        }
        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# VERIFY LOGIN INFORMATION
@views.route("/verify", methods=["POST"])
def verify_login():
    email = request.form.get('emailLogin')
    password = request.form.get('passwordLogin')

    if email == "admin@gmail.com" and password == "password":
        return redirect(url_for('views.dashboard'))
    else:
        return redirect(url_for('views.login'))
    
# SEARCH PRODUCTS FROM DATABASE
@views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        products = Product.query.filter(
            or_(
                Product.name.ilike(f'%{query}%')
            )
        ).all()
    else:
        products = Product.query.all()

    results = [{'id': product.id, 'name': product.name, 'unit_price': product.unit_price, 
                'qty_in_stock': product.qty_in_stock, 'reorder_point': product.reorder_point,
                'reorder_quantity': product.reorder_quantity, 'restock_date': product.restock_date} 
               for product in products]
    return jsonify(results)