from flask import render_template, redirect
from employee import Employee
import user_authorization
import json

db = None

def index_page(info_text = ''):
    return render_template('index.html', \
                           info_text = info_text)

def employees_page(filters, month, sorting):
    employees = db.load_employees(filters = filters)
    table = []
    for employee in employees:
        hours = employee.get_working_hours(month)
        salary = hours * employee.salary_per_hour
        table.append([employee.id, employee.name, employee.age, employee.department, hours, employee.salary_per_hour, salary])
    if sorting != None:
        if sorting > 0:
            table = sorted(table, key = lambda x: x[sorting-1])
        else:
            table = sorted(table, key = lambda x: x[-sorting-1], reverse = True)
    month_str = month
    return render_template('table.html',
                           employees = table, filters = filters, month = month_str)



def edit_employee_page(employee_id, new_employee = False, info_text = ''):
    if new_employee:
        employee = db.add_employee(Employee())
        return redirect("/employee/" + str(employee.id))
        values = employee.to_dict()
        for key in values.keys():
            if key != 'id':
                values[key] = ''
        values['working_months'] = {}
    else:
        employee = db.load_employees(filters = {'id':employee_id})[0]
        values = employee.to_dict()
        print values
        
        values['working_months'] = json.loads(values['working_months'])
        for key in values['working_months'].keys():
            values['working_months'][key] /= 3600
            
    return render_template('edit_employee.html',
                           values = values, info_text = info_text)

def save_employee(form_values):
    values = form_values.to_dict()
    try:
        values['age'] = int(values['age'])
    except:
        values['age'] = 0
    try:
        values['salary_per_hour'] = int(values['salary_per_hour'])
    except:
        values['salary_per_hour'] = 0
    if values['id'] == '':
        values['id'] = 0
        employee = Employee(values)
        db.add_employee(employee)
    else:
        values['id'] = int(values['id'])
        employee = db.load_employees(filters = {'id':values['id']})[0]
        for key, value in values.items():
            setattr(employee, key, value)
        db.save_employee(employee)
    return redirect("/employee/" + str(employee.id))

def delete_employee(id):
    db.delete_employee(id)
    return redirect("/")

def save_employee_password(id, password):
    employee = db.load_employees(filters = {'id':id})[0]
    user_authorization.set_password(employee, password)
    db.save_employee(employee)
    return redirect("/employee/" + str(id))
