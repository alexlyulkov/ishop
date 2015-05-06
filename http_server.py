

from flask import Flask, request, send_file, render_template
import traceback
import json
import io
from classes import *

import website_authorization
import website

http_server = Flask(__name__, template_folder = 'frontend/', static_folder='')
http_server.debug = True

# This is the path to the upload directory
http_server.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
http_server.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

db = None


@http_server.route("/images/<filename>")
def get_images(filename):
    try:
        return http_server.send_static_file('frontend/images/' + filename)
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/css/<filename>")
def get_css(filename):
    try:
        return http_server.send_static_file('frontend/css/' + filename)
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/fonts/<filename>")
def get_font(filename):
    try:
        return http_server.send_static_file('frontend/fonts/' + filename)
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/js/<filename>")
def get_js(filename):
    try:
        return http_server.send_static_file('frontend/js/' + filename)
    except Exception, e:
        print traceback.format_exc()
        print e


@http_server.route("/")
def index_page():
    try:
        return website.index_page()
    except Exception, e:
        print traceback.format_exc()
        print e
        return traceback.format_exc() + '\n\n' + str(e)


@http_server.route("/image/<int:image_id>")
def get_image(image_id):
    try:
        if image_id == 1:
            return http_server.send_static_file('frontend/images/product1.jpg')
        if image_id == 2:
            return http_server.send_static_file('frontend/images/ad1.jpg')

        image = db.get_image(image_id)
        return send_file(io.BytesIO(image.bytes),
                         attachment_filename='product_picture.png',
                     mimetype='image/png')
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product_page(product_id):
    try:
        res =  website.product_page(product_id)
        return res
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/category/<int:category_id>", methods=['GET', 'POST'])
def categoty_page(category_id):
    try:
        res =  website.category_page(category_id)
        return res
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/cart", methods=['GET', 'POST'])
def cart_page():
    try:
        return website.cart_page()
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/add_to_cart/<int:product_id>", methods=['GET', 'POST'])
def add_to_cart(product_id):
    try:
        return website.add_to_cart(product_id)
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/delete_from_cart/<int:product_id>", methods=['GET', 'POST'])
def delete_from_cart(product_id):
    try:
        return website.delete_from_cart(product_id)
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/ordering", methods=['GET', 'POST'])




@http_server.route("/new_product", methods=['GET', 'POST'])
@website_authorization.requires_auth
def add_product():
    try:
        return render_template("addProduct.html", product = Product())

    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/modify_product/<int:product_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth

@http_server.route("/save_product", methods=['GET', 'POST'])
@website_authorization.requires_auth
def save_product():
    try:
        print type(request.files['images'])
        uploaded_files = request.files.getlist("images")
        print uploaded_files
        image_bytes = uploaded_files[0].read()
        print type(image_bytes)
        return send_file(io.BytesIO(image_bytes),
                         attachment_filename='product_picture.png',
                     mimetype='image/png')
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/new_category", methods=['GET', 'POST'])
@website_authorization.requires_auth

@http_server.route("/modify_category/<int:category_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth

@http_server.route("/save_category", methods=['GET', 'POST'])
@website_authorization.requires_auth

@http_server.route("/orders", methods=['GET', 'POST'])
@website_authorization.requires_auth

@http_server.route("/order/<int:order_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth

@http_server.route("/delete_order/<int:order_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth




@http_server.route("/contatcs", methods=['GET', 'POST'])

@http_server.route("/delivery", methods=['GET', 'POST'])
