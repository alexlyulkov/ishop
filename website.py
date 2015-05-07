from flask import render_template, redirect, make_response, request
import json
from classes import *

db = None

def save_images(files):
    images_ids = []
    for f in files:
        image = Image()
        image.bytes = f.read()
        image_id = db.add_image(image)
        images_ids.append(image_id)
    return images_ids
    
def edit_ad_page(ad_id = None):
    ad = Ad()
    if ad_id != None:
        ad = db.load_ad(ad_id)

    ads = db.load_ads()
        
    return render_template("addAd.html",
                           ad = ad,
                           categories = db.load_categories(),
                           ads = ads)

def save_ad(values, images):
    values['id'] = int(values['id'])
    print images
    values['image_id'] = save_images(images)[0]
    ad = Ad(values)
    if ad.id == -1:
        db.add_ad(ad)
    else:
        db.update_ad(ad)

    return redirect("/new_ad")
    
def delete_ad(ad_id):
    ad = db.load_ad(ad_id)
    db.delete_image(ad.image_id)
    db.delete_ad(ad_id)
    return redirect("/new_ad")


def edit_product_page(product_id = None):
    product = Product()
    if product_id != None:
        product = db.load_product(product_id)
        
    return render_template("addProduct.html",
                           product = product,
                           categories = db.load_categories())

def save_product(values, images):
    values['id'] = int(values['id'])
    values['category'] = int(values['category'])
    values['images_ids'] = save_images(images)
    product = Product(values)
    if product.id == -1:
        db.add_product(product)
    else:
        db.update_product(product)

    return redirect("/")

def delete_product(product_id):
    product = db.load_product(product_id)
    for img_id in product.images_ids:
        db.delete_image(img_id)
    db.delete_product(product_id)
    return redirect("/")

def edit_category_page(category_id = None):
    category = Category()
    if category_id != None:
        category = db.load_category(category_id)
        
    return render_template("addCategory.html",
                           category = category,
                           categories = db.load_categories())
def save_category(values):
    values['id'] = int(values['id'])
    category = Category(values)
    print 'save category:', category.to_dict()
    if category.id == -1:
        db.add_category(category)
    else:
        db.update_category(category)

    return redirect("/new_category")

def delete_category(category_id):
    products = db.load_category_products(category_id)
    for product in products:
        db.delete_product(product.id)
    db.delete_category(category_id)
    
    return redirect("/new_category")

'''def save_order(values):
    order = Order(values)
    if order.id == -1:
        db.add_order(category)
    else:
        db.update_order(categoty)

    return redirect("/")'''




def index_page():
    categories = db.load_categories()
    print categories
    randomProducts = db.get_random_products(10)
    ads = db.load_ads()
    
    return render_template('index.html',
                           categories = categories,
                           ads = ads,
                           productItemsAds = randomProducts)


def category_page(category_id, values):
    print values
    sorting = 1
    brands = {}
    all_brands = db.get_category_brands(category_id)
    selected_brands = []
    for b in all_brands:
        brands[b] = 0
    for key in values.keys():
        if key.startswith('b_'):
            brands[key[2:]] = 1
            selected_brands.append(key[2:])
    if values.get('sorting'):
        sorting = int(values['sorting'])

    sort_by = 'id'
    order = 'ASC'
    if sorting == 1:
        sort_by = 'price'
        order = 'ASC'
    if sorting == 2:
        sort_by = 'price'
        order = 'DESC'

    #selected_brands = []
    #    if values.get('brands'):
    #    for
        
    categories = db.load_categories()
    products = db.load_category_products(category_id,
                                         sort_by = sort_by,
                                         order = order,
                                         brands_filter = selected_brands)

    return render_template('category.html',
                           categories = categories,
                           filteredProducts = products,
                           brands = brands,
                           category_id = category_id,
                           sorting = sorting)

def product_page(product_id):
    categories = db.load_categories()
    product = db.load_product(product_id)

    return render_template('product.html',
                           categories = categories,
                           productItem = product)

def contact_us_page():
    categories = db.load_categories()
    return render_template('contactUs.html',
                           categories = categories)

def delivery_page():
    categories = db.load_categories()
    return render_template('delivery.html',
                           categories = categories)

def ordering_page():
    categories = db.load_categories()
    return render_template('ordering.html',
                           categories = categories)

def make_order(values):
    cart = json.loads(request.cookies.get('cart'))
    order = Order(values)
    order.products = cart
    order_id = db.add_order(order)
    order.id = order_id
    resp = make_response(render_template('orderSuccess.html',
                                         categories = db.load_categories(),
                                         order = order))
    resp.set_cookie('cart', expires = 0)
    return resp

def order_page(order_id):
    order = db.load_order(order_id)
    products = []
    for id in order.products:
        products.append(db.load_product(id))
	cost = 0
	for p in products:
		cost += p.price
    return render_template('order.html',
                           categories = db.load_categories(),
                           order = order,
                           products = products,
						   priceSum = cost)

def delete_order(order_id):
    db.delete_order(order_id)
    return redirect("/orders")


def orders_page():
    orders = db.load_orders()
    return render_template('orders.html',
                           categories = db.load_categories(),
                           orders = orders)

    

def add_to_cart(product_id):
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = []
    cart.append(product_id)
    cart = json.dumps(cart)
    
    resp = make_response(redirect('/cart'))
    resp.set_cookie('cart', cart)
    return resp

def delete_from_cart(product_id):
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = []
    cart.remove(product_id)
    cart = json.dumps(cart)
    
    resp = make_response(redirect('/cart'))
    resp.set_cookie('cart', cart)
    return resp

def cart_page():
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = []
    products = [db.load_product(product_id) for product_id in cart]
    cost = 0
    for p in products:
        cost += p.price
    return render_template('basket.html',
                           categories = db.load_categories(),
                           boughtItems = products,
                           priceSum = cost)


                           
    



