

from flask import Flask, request, send_file
import traceback
import json
import io

import website_authorization
import website
import utils
import api

http_server = Flask(__name__, template_folder = 'html_templates', static_folder='')
http_server.debug = True




@http_server.route("/images/<filename>")
def get_image(filename):
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
        return http_server.send_static_file('frontend/js' + filename)
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


@http_server.route("/product_picture/<int:product_id>")
def get_product_picture(product_id):
    try:
        binary_image = 123
        return send_file(io.BytesIO(binary_image),
                         attachment_filename='product_picture.png',
                     mimetype='image/png')
    except Exception, e:
        print traceback.format_exc()
        print e


@http_server.route("/product/<int:product_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth
def product_page(product_id):
    try:
        res =  website.edit_employee_page(-1, new_employee = True)
        return res
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/categoty/<int:categoty_id>", methods=['GET', 'POST'])
@website_authorization.requires_auth
def categoty_page(categoty_id):
    try:
        res =  website.edit_employee_page(-1, new_employee = True)
        return res
    except Exception, e:
        print traceback.format_exc()
        print e

@http_server.route("/cart/", methods=['GET', 'POST'])
@website_authorization.requires_auth
def product_page(product_id):
    try:
        res =  website.edit_employee_page(-1, new_employee = True)
        return res
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
