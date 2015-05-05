from flask import render_template, redirect, make_response, request
import json
from classes import *

db = None

def save_images(files):
    images_ids = []
    for f in files:
        image = db.add_image(f.read())
        images_ids.append(image.id)
    return image_ids
    

def save_ad(values, images):
    values['image_id'] = save_images(values['files'])[0]
    ad = Ad(values)
    if ad.id == -1:
        db.add_ad(ad)
    else:
        db.update_ad(ad)

    return render_template('index.html',
                           categories = db.get_categories,
                           productItemsAds = db.get_random_products)

def save_product(values, images):
    values['images_ids'] = save_images(values['files'])
    product = Product(values)
    if product.id == -1:
        db.add_product(product)
    else:
        db.update_product(product)

    return render_template('index.html',
                           categories = db.get_categories,
                           productItemsAds = db.get_random_products)

def save_category(values):
    category = Category(values)
    if category.id == -1:
        db.add_category(categoty)
    else:
        db.update_category(categoty)

    return render_template('index.html',
                           categories = db.get_categories,
                           productItemsAds = db.get_random_products)

def save_order(values):
    order = Order(values)
    if order.id == -1:
        db.add_order(categoty)
    else:
        db.update_order(categoty)

    return render_template('index.html',
                           categories = db.get_categories,
                           productItemsAds = db.get_random_products)




def index_page():
    categories = db.get_categories()
    randomProducts = db.get_random_products(10)
    ads = db.get_all_ads()
    
    return render_template('index.html',
                           categories = categories,
                           ads = ads,
                           productItemsAds = randomProducts)


def category_page(category_id):
    categories = db.get_categories()
    products = db.load_category(categoty_id)

    return render_template('category.html',
                           categories = categories,
                           products = products)

def product_page(product_id):
    categories = db.get_categories()
    product = db.load_product(product_id)

    return render_template('product.html',
                           categories = categories,
                           product = product)

def Contact_us_page():
    categories = db.get_categories()
    return render_template('contactUs.html',
                           categories = categories)

def ordering_page():
    categories = db.get_categories()
    return render_template('ordering.html',
                           categories = categories)

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
    return render_template('basket.html',
                           categories = db.get_categories,
                           boughtItems = products)


                           
    



