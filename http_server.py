

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
#@website_authorization.requires_auth
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
@website_authorization.requires_auth
def cart_page(product_id):
    try:
        return website.cart_page()
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/new_product", methods=['GET', 'POST'])
@website_authorization.requires_auth
def add_product():
    try:
        return render_template('addProduct.html', \
                               product = Product())

    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/save_product", methods=['GET', 'POST'])
@website_authorization.requires_auth
def save_product():
    try:
        print type(request.files['images'])
        uploaded_files = request.files.getlist("images")
        print uploaded_files
        image_bytes = uploaded_files[0].read()
        return send_file(io.BytesIO(image_bytes),
                         attachment_filename='product_picture.png',
                     mimetype='image/png')
    except Exception, e:
        print traceback.format_exc()
        print e





        
@http_server.route("/employee/<int:employee_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth
def edit_employee_page(employee_id):
    return website.edit_employee_page(employee_id)

@http_server.route("/new_employee", methods=['GET', 'POST'])
@website_authorization.requires_auth
def new_employee_page():
    try:
        res =  website.edit_employee_page(-1, new_employee = True)
        return res
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/save_employee", methods=['GET', 'POST'])
@website_authorization.requires_auth
def save_employee_page():
    try:
        values = request.form
        return website.save_employee(values)
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/delete_employee", methods=['GET', 'POST'])
@website_authorization.requires_auth
def delete_employee():
    try:
        id = request.form.get('id')
        return website.delete_employee(id)
    except Exception, e:
        print traceback.format_exc()
        print e


@http_server.route("/save_employee_password", methods=['GET', 'POST'])
@website_authorization.requires_auth
def save_employee_password():
    try:
        id = request.form.get('id')
        password = request.form.get('password')
        return website.save_employee_password(id, password)
    except Exception, e:
        print traceback.format_exc()
        print e



@http_server.route("/employees", methods=['GET', 'POST'])
@website_authorization.requires_auth
def employees_page():
    try:

        month = request.form.get('month') or utils.current_month()
        print '!!!!!!!!', month
        sorting = int(request.form.get('sorting') or 1)
        sorting_dir = int(request.form.get('sorting_dir') or 1)
        if sorting_dir == 2:
            sorting = -sorting
        filters = request.form.to_dict()
        if 'month' in filters:
            del filters['month']
        if 'sorting' in filters:
            del filters['sorting']
        if 'sorting_dir' in filters:
            del filters['sorting_dir']
        for key in filters.keys():
            if filters[key].strip() == '':
                del filters[key]
        return website.employees_page(filters, month, sorting)
    except Exception, e:
        print traceback.format_exc()
        print e

    

@http_server.route("/add_working_seconds", methods=['POST'])
def add_working_seconds():
    try:
        print request.form.to_dict()
        employee_id = int(request.form.get('employee_id'))
        password = request.form.get('password')
        working_seconds = int(request.form.get('working_seconds'))
        return api.add_working_seconds(employee_id, working_seconds, password)
    except Exception, e:
        print traceback.format_exc()
        print e
        return str(e)
