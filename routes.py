from flask import render_template, request, session, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from flask_paginate import Pagination
from model import User, Category, Course, Material, Dashboard
import os
from app import app

user_model = User()
category_model = Category()
course_model = Course()
material_model = Material()
dashboard_model = Dashboard()

# ~~~~~~~~~~~~~~~~~~~~~~~~~
#        Frontend         #
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# index


@app.route('/')
def index():
    categories = category_model.get_all()
    courses = course_model.get_all()
    if 'user_id' in session:
        user = user_model.get_user_by_id(session['user_id'])
        return render_template('index.html', title='Home', user=user, categories=categories, courses=courses)
    else:
        return render_template('index.html', title='Home', categories=categories, courses=courses)

# get materials html


@app.route('/getmaterials', methods=['POST'])
def get_materials():
    settings = dashboard_model.settings()
    limit = settings.get('material_per_page')
    catid = courseid = False
    if 'catid' in request.form:
        catid = request.form.get('catid')
    if 'courseid' in request.form:
        courseid = request.form.get('courseid')
    offset = int(request.form.get('offset'))*limit
    if catid:
        materials = material_model.get_by_category(catid, limit, offset)
    elif courseid:
        materials = material_model.get_by_course(courseid, limit, offset)
    else:
        materials = material_model.get_all(limit, offset)
    return render_template('materials_ajax.html', materials=materials)


# register


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['fname']
        username = request.form['fname']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        error = user_model.register(
            first_name, last_name, username, email, mobile, password)
        if error:
            flash(error, 'danger')
        else:
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Registration')

# login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = user_model.login(email, password)

        if user:
            if user['status'] == 0:
                flash('Your account is blocked, please contact administrator.', 'danger')
                return redirect(url_for('login'))
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password, please try again.', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Login')

# logout


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# category view


@app.route('/category/<int:id>')
def category_view(id):
    category = category_model.get_by_id(id)
    if 'user_id' in session:
        user = user_model.get_user_by_id(session['user_id'])
        return render_template('category.html', title="Materials in "+category.get('category_name'), category=category, user=user)
    return render_template('category.html', title="Materials in "+category.get('category_name'), category=category)

# course view


@app.route('/course/<int:id>')
def course_view(id):
    course = course_model.get_by_id(id)
    if 'user_id' in session:
        user = user_model.get_user_by_id(session['user_id'])
        return render_template('course.html', title="Materials in "+course.get('course_name'), course=course, user=user)
    return render_template('course.html', title="Materials in "+course.get('course_name'), course=course)

# material view


@app.route('/material/<int:id>')
def material_view(id):
    material = material_model.get_by_id(id)
    contact_no = user_model.get_user_by_id(
        material['user_id']).get('mobile')
    if 'user_id' in session:
        user = user_model.get_user_by_id(session['user_id'])
        return render_template('material.html', title=material.get('title'), material=material, user=user, contact_no=contact_no)
    return render_template('material.html', title=material.get('title'), material=material, contact_no=contact_no)

# material download


@app.route('/material/<int:id>/download')
def download(id):
    material = material_model.get_by_id(id)
    if 'user_id' not in session:
        redirect(url_for('index'))
    folder = 'upload\\files'
    name = secure_filename(material.get(
        'title').strip().replace(' ', '_').lower()+'_'+str(id))
    filepath = os.path.join(folder, name + '.' + material.get('ext'))
    customname = material.get('title')+'.'+material.get('ext')
    return send_file(filepath, as_attachment=True, download_name=customname)

# material search


@app.route('/material/search')
def material_search():
    query = request.args.get('query')
    if 'user_id' in session:
        user = user_model.get_user_by_id(session['user_id'])
        return render_template('search.html', title="Search", query=query, user=user)
    return render_template('search.html', query=query)


@app.route('/search')
def search():
    settings = dashboard_model.settings()
    query = request.args.get('query')
    limit = settings.get('material_per_page')
    offset = int(request.args.get('offset'))*limit
    materials = material_model.search(query, limit, offset)
    return render_template('materials_ajax.html', materials=materials, query=query)


# chatroom
@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if request.method == 'GET':
        action = request.args.get('action')
        if action == 'getmessages':
            messages = user_model.get_messages()
            return messages
    if request.method == 'POST':
        data = request.get_json()
        action = data['action']
        message = data['message']
        if action == 'sendmessage':
            user_model.send_message(message, session['user_id'])
            return {'success': True}
    return render_template('chatroom.html', title='Chatroom', user=user)

# ~~~~~~~~~~~~~~~~~~~~~~~~~
#        Backend          #
# ~~~~~~~~~~~~~~~~~~~~~~~~~

# dashboard


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    dashdata = {
        'total_users': dashboard_model.get_count('id', 'users'),
        'total_materials': dashboard_model.get_count('id', 'materials'),
        'total_categories': dashboard_model.get_count('id', 'categories'),
        'total_courses': dashboard_model.get_count('id', 'courses'),
        'user_materials': dashboard_model.get_count_by_user('id', 'materials', session['user_id']),
    }
    return render_template('dashboard/index.html', user=user, dashdata=dashdata, title='Dashboard')

# users


@app.route('/dashboard/users')
@app.route('/dashboard/users/page/<int:page>')
def dashboard_users(page=1):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if user['role'] != 'admin':
        return redirect(url_for('index'))
    per_page = 10  # Number of courses per page
    offset = (page - 1) * per_page
    users = user_model.get_all(limit=per_page, offset=offset)
    total_users = dashboard_model.get_count('id', 'users')
    pagination = Pagination(page=page, per_page=per_page, total=total_users,
                            css_framework='bootstrap5', alignment='center')
    return render_template('dashboard/users.html', title='Users', users=users, user=user, pagination=pagination)


# website settings

@app.route('/dashboard/settings', methods=['GET', 'POST'])
def dashboard_settings():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if user['role'] != 'admin':
        return redirect(url_for('index'))
    settings = dashboard_model.settings()
    if request.method == 'POST':
        success = dashboard_model.settings(request.form)
        if not success:
            flash('Error occured while updating the settings.', 'danger')
        else:
            flash('Settings updated successfully.', 'success')
        return redirect(url_for('dashboard_settings'))
    return render_template('dashboard/settings.html', title='Settings', user=user, settings=settings)

# user profile


@app.route('/dashboard/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if request.method == 'POST':
        oldpassword = request.form.get('old_password')
        newpassword = request.form.get('new_password')
        confirmpassword = request.form.get('confirm_password')
        if (not confirmpassword or not newpassword or not oldpassword):
            flash('All fields are required.', 'danger')
            return redirect(url_for('change_password'))
        if (oldpassword != user.get('password')):
            flash('Old password is incorrect.', 'danger')
            return redirect(url_for('change_password'))
        if (newpassword != confirmpassword):
            flash('Confirm password does not match.', 'danger')
            return redirect(url_for('change_password'))
        userid = session['user_id']
        success = user_model.change_password(newpassword, userid)
        if not success:
            flash('Error occured while updating the Password.', 'danger')
        else:
            flash('Password updated successfully.', 'success')
        return redirect(url_for('change_password'))
    return render_template('dashboard/password.html', title='Change Password', user=user)

# delete user


@app.route('/dashboard/user/delete', methods=['POST'])
def delete_user():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    userid = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    materials = material_model.get_by_user(userid)
    data = {}
    if user['role'] == 'admin':
        user_model.delete(userid)
        for material in materials:
            material_model.delete(material['id'])
            # delete files from storage
            if material['type'] == 1:
                folder = 'upload\\files'
                name = material['title'].strip().replace(
                    ' ', '_').lower()+'_'+str(material['id'])
                for filename in os.listdir(folder):
                    if filename.startswith(name):
                        os.remove(os.path.join(folder, filename))
        data['status'] = True
        data['message'] = 'User deleted successfully!'
    else:
        data['status'] = False
        data['message'] = 'You do not have permission to delete this user!'
    return (data)

# change status of user


@app.route('/dashboard/user/status', methods=['POST'])
def user_status():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    data = {}
    usersx = user_model.get_user_by_id(id)
    status = 1 if usersx['status'] == 0 else 0
    if user['role'] == 'faculty' or user['role'] == 'admin':
        user_model.change_status(id, status)
        data['status'] = status
        data['message'] = 'User status changed successfully!'
    else:
        data['status'] = status
        data['message'] = 'You do not have permission to perform this action!'
    return (data)


# change user role

@app.route('/dashboard/user/role', methods=['POST'])
def role_user():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    userid = request.form.get('id')
    userrole = request.form.get('role')
    user = user_model.get_user_by_id(session['user_id'])
    data = {}
    if user['role'] == 'admin':
        user_model.role(userid, userrole)
        data['status'] = True
        data['message'] = 'User role changed successfully!'
    else:
        data['status'] = False
        data['message'] = 'You do not have permission to perfomn this task!'
    return (data)

# add category


@app.route('/dashboard/add_category', methods=['GET', 'POST'])
def add_category():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if user['role'] not in ['admin', 'faculty']:
        return redirect(url_for('index'))
    if request.method == 'POST':
        category_name = request.form['category_name']
        category_status = 1 if 'category_status' in request.form else 0
        success = category_model.add(category_name, category_status)
        if not success:
            flash(success, 'danger')
        else:
            flash('Category added successfully.', 'success')
        return redirect(url_for('add_category'))
    return render_template('dashboard/categories_add.html', title='Add Category', user=user)

# category list


@app.route('/dashboard/categories')
@app.route('/dashboard/categories/page/<int:page>')
def dashboard_categories(page=1):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if user['role'] not in ['admin', 'faculty']:
        return redirect(url_for('index'))
    per_page = 10  # Number of categories per page
    offset = (page - 1) * per_page
    categories = category_model.get_all(limit=per_page, offset=offset)

    total_categories = dashboard_model.get_count('id', 'categories')
    pagination = Pagination(page=page, per_page=per_page, total=total_categories,
                            css_framework='bootstrap5', alignment='center')
    return render_template('dashboard/categories_list.html', title='Categories', categories=categories, user=user, pagination=pagination)

# get all categories as json


@app.route('/dashboard/categories/getalljson')
def get_all_categories_as_json():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    categories = category_model.get_all()
    return (categories)

# delete category


@app.route('/dashboard/categories/delete', methods=['POST'])
def delete_category():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    materials = material_model.get_by_category(id)
    data = {}
    if user['role'] == 'faculty' or user['role'] == 'admin':
        category_model.delete(id)
        for material in materials:
            material_model.delete(material['id'])
            # delete files from storage
            if material['type'] == 1:
                folder = 'upload\\files'
                name = material['title'].strip().replace(
                    ' ', '_').lower()+'_'+str(material['id'])
                for filename in os.listdir(folder):
                    if filename.startswith(name):
                        os.remove(os.path.join(folder, filename))
        data['status'] = True
        data['message'] = 'Category deleted successfully!'
    else:
        data['status'] = False
        data['message'] = 'You do not have permission to delete this category!'
    return (data)

# catgegory status


@app.route('/dashboard/categories/status', methods=['POST'])
def category_status():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    data = {}
    category = category_model.get_by_id(id)
    status = 1 if category['status'] == 0 else 0
    if user['role'] == 'faculty' or user['role'] == 'admin':
        category_model.change_status(id, status)
        data['status'] = status
        data['message'] = 'Category status changed successfully!'
    else:
        data['status'] = status
        data['message'] = 'You do not have permission to perform this action!'
    return (data)

# add course


@app.route('/dashboard/add_course', methods=['GET', 'POST'])
def add_course():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if user['role'] not in ['admin', 'faculty']:
        return redirect(url_for('index'))
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_status = 1 if 'course_status' in request.form else 0
        success = course_model.add(course_name, course_status)
        if not success:
            flash(success, 'danger')
        else:
            flash('Course added successfully.', 'success')
        return redirect(url_for('add_course'))
    return render_template('dashboard/courses_add.html', title='Add Course', user=user)

# course list


@app.route('/dashboard/courses')
@app.route('/dashboard/courses/page/<int:page>')
def dashboard_courses(page=1):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if user['role'] not in ['admin', 'faculty']:
        return redirect(url_for('index'))
    per_page = 10  # Number of courses per page
    offset = (page - 1) * per_page
    courses = course_model.get_all(limit=per_page, offset=offset)

    total_courses = dashboard_model.get_count('id', 'courses')
    pagination = Pagination(page=page, per_page=per_page, total=total_courses,
                            css_framework='bootstrap5', alignment='center')
    return render_template('dashboard/courses_list.html', title='Courses', courses=courses, user=user, pagination=pagination)

# get all course json


@app.route('/dashboard/courses/getalljson')
def get_all_courses_as_json():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    courses = course_model.get_all()
    return (courses)


@app.route('/dashboard/courses/delete', methods=['POST'])
def delete_course():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    materials = material_model.get_by_course(id)
    data = {}
    if user['role'] == 'faculty' or user['role'] == 'admin':
        course_model.delete(id)
        for material in materials:
            material_model.delete(material['id'])
            # delete files from storage
            if material['type'] == 1:
                folder = 'upload\\files'
                name = material['title'].strip().replace(
                    ' ', '_').lower()+'_'+str(material['id'])
                for filename in os.listdir(folder):
                    if filename.startswith(name):
                        os.remove(os.path.join(folder, filename))
        data['status'] = True
        data['message'] = 'Course deleted successfully!'
    else:
        data['status'] = False
        data['message'] = 'You do not have permission to delete this course!'
    return (data)

# course status


@app.route('/dashboard/courses/status', methods=['POST'])
def course_status():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    data = {}
    course = course_model.get_by_id(id)
    status = 1 if course['status'] == 0 else 0
    if user['role'] == 'faculty' or user['role'] == 'admin':
        course_model.change_status(id, status)
        data['status'] = status
        data['message'] = 'Course status changed successfully!'
    else:
        data['status'] = status
        data['message'] = 'You do not have permission to perform this action!'
    return (data)


@app.route('/dashboard/add_material', methods=['GET', 'POST'])
def add_material():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description'] if request.form['description'] else ''
        pickup = request.form['pickup'] if request.form['pickup'] else ''
        type = request.form['type']
        category_id = request.form['category_id']
        course_id = request.form['course_id']
        user_id = session['user_id']
        settings = dashboard_model.settings()
        ext = ''
        if settings['approval_required'] == 0 or user['role'] in ['admin', 'faculty']:
            status = 1 if 'material_status' in request.form else 0
        else:
            status = 0
        if not title:
            flash('Please enter a title.', 'danger')
            return redirect(url_for('add_material'))
        if not category_id:
            flash('Please select a category.', 'danger')
            return redirect(url_for('add_material'))
        if not course_id:
            flash('Please select a course.', 'danger')
            return redirect(url_for('add_material'))
        if type == '1':
            if 'file' in request.files and request.files['file'].filename != '':
                file = request.files['file']
                max_file_size = 1024*1024*5
                # check file size
                pos = file.tell()
                file.seek(0, 2)
                size = file.tell()
                file.seek(pos)
                # end
                ext = file.filename.split('.')[-1].lower()
                allowed_file_types = ['pdf', 'zip', 'mp4',
                                      'mkv', 'doc', 'docx', 'xlsx', 'pptx', 'ppt']
                if ext not in allowed_file_types:
                    flash('File type not allowed.', 'danger')
                    return redirect(url_for('add_material'))
                if size > max_file_size:
                    flash('File should not exceed 5 MB.', 'danger')
                    return redirect(url_for('add_material'))
            else:
                flash('Please upload a file.', 'danger')
                return redirect(url_for('add_material'))
        id = material_model.add(
            title, description, type, ext, pickup, category_id, course_id, user_id, status)
        if id != False:
            # handle file upload
            if type == '1':
                folder = 'upload\\files'
                name = secure_filename(title.strip().replace(
                    ' ', '_').lower()+'_'+str(id))
                filepath = os.path.join(folder, name + '.' + ext)
                file.save(filepath)
            if status == 0:
                flash(
                    'Material added successfully. Please wait for admin approval.', 'info')
            else:
                flash('Material added successfully.', 'success')
        else:
            flash('An unexpected error occured, please try again.', 'danger')
        return redirect(url_for('add_material'))
    else:
        categories = category_model.get_all()
        courses = course_model.get_all()
        return render_template('dashboard/materials_add.html', title='Add Material', categories=categories, courses=courses, user=user)


@app.route('/dashboard/materials')
@app.route('/dashboard/materials/page/<int:page>')
def dashboard_materials(page=1):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = user_model.get_user_by_id(session['user_id'])
    per_page = 10  # Number of categories per page
    offset = (page - 1) * per_page
    if (user['role'] == 'user'):
        materials = material_model.get_by_user(
            userid=session['user_id'], limit=per_page, offset=offset)
        total_materials = dashboard_model.get_count_by_user(
            'id', 'materials', session['user_id'])
    else:
        materials = material_model.get_all_backend(
            limit=per_page, offset=offset)
        total_materials = dashboard_model.get_count('id', 'materials')

    pagination = Pagination(page=page, per_page=per_page, total=total_materials,
                            css_framework='bootstrap5', alignment='center')
    return render_template('dashboard/materials_list.html', title='Materials', materials=materials, user=user, pagination=pagination)


@app.route('/dashboard/materials/status', methods=['POST'])
def material_status():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    data = {}
    material = material_model.get_by_id(id)
    status = 1 if material['status'] == 0 else 0
    if user['role'] == 'faculty' or user['role'] == 'admin':
        material_model.change_status(id, status)
        data['status'] = status
        data['message'] = 'Material status changed successfully!'
    else:
        data['status'] = status
        data['message'] = 'You do not have permission to perform this action!'
    return (data)

# delete material


@app.route('/dashboard/materials/delete', methods=['POST'])
def delete_material():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    id = request.form.get('id')
    user = user_model.get_user_by_id(session['user_id'])
    material = material_model.get_by_id(id)
    data = {}
    if user['role'] == 'faculty' or user['role'] == 'admin' or material['user_id'] == user['id']:
        material_model.delete(id)
        # delete file from storage
        if material['type'] == 1:
            folder = 'upload\\files'
            name = material['title'].strip().replace(
                ' ', '_').lower()+'_'+str(id)
            for filename in os.listdir(folder):
                if filename.startswith(name):
                    os.remove(os.path.join(folder, filename))
        data['status'] = True
        data['message'] = 'Material deleted successfully!'
    else:
        data['status'] = False
        data['message'] = 'You do not have permission to delete this material!'
    return (data)
