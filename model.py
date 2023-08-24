from app import mycursor, mysql, mydb

class User:
    def register(self, first_name, last_name, username, email, mobile, password):
        if not first_name:
            return "Please provide a valid first name"
        if not last_name:
            return "Please provide a valid last name"
        if not username:
            return "Please provide a valid username"
        elif not email:
            return "Please provide a valid email"
        elif not mobile:
            return "Please provide a valid mobile number"
        elif not password:
            return "Please provide a valid password"
        elif self.email_exists(email):
            return "Email already registered"
        elif self.username_exists(username):
            return "Username already taken"
        sql = "INSERT INTO users (first_name, last_name, username, email,mobile, password) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (first_name, last_name, username, email, mobile, password)
        mycursor.execute(sql, val)
        mydb.commit()
        return None

    def login(self, email, password):
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        return user

    def email_exists(self, email):
        sql = "SELECT * FROM users WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        return user

    def username_exists(self, username):
        sql = "SELECT * FROM users WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        return user

    def get_user_by_id(self, user_id):
        sql = "SELECT * FROM users WHERE id = %s"
        val = (user_id,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        return user

    def get_all(self, limit=None, offset=None):
        sql = "SELECT * FROM users ORDER BY id DESC"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql, (limit, offset))
        else:
            mycursor.execute(sql)
        users = mycursor.fetchall()
        return users

    def change_password(self, newpassword, userid):
        sql = "update users set `password` = %s where id = %s;"
        val = (newpassword, userid)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except:
            mysql.rollback()
            return False

    def delete(self, id):
        sql = "DELETE FROM users WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def role(self, id, role):
        sql = "UPDATE users set role=%s WHERE id = %s"
        val = (
            role,
            id,
        )
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def get_messages(self):
        sql = "SELECT * FROM ( SELECT messages.*, users.username, users.role FROM messages JOIN users ON messages.user_id=users.id ORDER BY id DESC LIMIT 10 ) AS t ORDER BY id ASC;"
        mycursor.execute(sql)
        messages = mycursor.fetchall()
        return messages

    def send_message(self, message, userid):
        sql = "INSERT INTO messages (message,user_id) VALUES (%s,%s)"
        val = (message, userid)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except:
            mydb.rollback()
            return False

    def change_status(self, id, status):
        sql = "update users set status = %s where id = %s;"
        val = (status, id)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except:
            mydb.rollback()
            return False


class Dashboard:
    def get_count(self, field, table):
        sql = "SELECT count(%s) as cnt FROM `%s`" % (field, table)
        mycursor.execute(sql)
        result = mycursor.fetchone()
        count = result.get('cnt')
        return count

    def get_count_by_user(self, field, table, user_id):
        sql = "SELECT count(%s) as cnt FROM `%s`  where user_id=%i;" % (
            field,
            table,
            user_id,
        )
        mycursor.execute(sql)
        result = mycursor.fetchone()
        count = result.get('cnt')
        return count

    def settings(self, request=None):
        if request is None:
            sql = "SELECT * FROM settings"
            mycursor.execute(sql)
            settings = mycursor.fetchone()
            return settings
        else:
            sql = "update settings set `material_per_page` = %s, `approval_required` = %s;"
            material_per_page = request.get("material_per_page")
            approval_required = 1 if "approval_required" in request else 0
            val = (material_per_page, approval_required)
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                return True
            except:
                mydb.rollback()
                return False


class Category:
    def add(self, category_name, category_status):
        sql = "INSERT INTO categories (category_name,status) VALUES (%s,%s)"
        val = (
            category_name,
            category_status,
        )
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def delete(self, id):
        sql = "DELETE FROM categories WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def get_all(self, limit=None, offset=None):
        sql = "SELECT * FROM categories ORDER BY id DESC"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql, (limit, offset))
        else:
            mycursor.execute(sql)
        categories = mycursor.fetchall()
        return categories

    def get_by_id(self, id):
        sql = "SELECT * FROM categories WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        category = mycursor.fetchone()
        return category

    def change_status(self, id, status):
        sql = "update categories set status = %s where id = %s;"
        val = (status, id)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except:
            mydb.rollback()
            return False


class Course:
    def add(self, course_name, course_status):
        sql = "INSERT INTO courses (course_name,status) VALUES (%s,%s)"
        val = (
            course_name,
            course_status,
        )
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def delete(self, id):
        sql = "DELETE FROM courses WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def get_all(self, limit=None, offset=None):
        sql = "SELECT * FROM courses ORDER BY id DESC"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql, (limit, offset))
        else:
            mycursor.execute(sql)
        courses = mycursor.fetchall()
        return courses

    def get_by_id(self, id):
        sql = "SELECT * FROM courses WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        course = mycursor.fetchone()
        return course

    def change_status(self, id, status):
        sql = "update courses set status = %s where id = %s;"
        val = (status, id)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except:
            mydb.rollback()
            return False


class Material:
    def add(
        self,
        title,
        description,
        type,
        ext,
        pickup,
        category_id,
        course_id,
        user_id,
        status,
    ):
        sql = "INSERT INTO materials (title, description, type, ext, pickup, category_id, course_id, user_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            title,
            description,
            type,
            ext,
            pickup,
            category_id,
            course_id,
            user_id,
            status,
        )
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            inserted_id = mycursor.lastrowid
            return inserted_id
        except:
            mydb.rollback()
            return False

    def get_all(self, limit=None, offset=None):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id where materials.status=1 ORDER by materials.id desc"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql % (limit, offset))
        else:
            mycursor.execute(sql)
        materials = mycursor.fetchall()
        return materials

    def get_all_backend(self, limit=None, offset=None):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id ORDER by materials.id desc"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql % (limit, offset))
        else:
            mycursor.execute(sql)
        materials = mycursor.fetchall()
        return materials

    def get_by_user(self, userid, limit=None, offset=None):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id WHERE materials.user_id=%s ORDER by materials.id desc"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql % (userid, limit, offset))
        else:
            mycursor.execute(sql % (userid,))
        materials = mycursor.fetchall()
        return materials

    def get_by_category(self, category_id, limit=None, offset=None):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id WHERE materials.category_id = %s and materials.status=1 order by materials.id desc"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql % (category_id, limit, offset))
        else:
            mycursor.execute(sql % (category_id,))
        materials = mycursor.fetchall()
        return materials

    def get_by_course(self, course_id, limit=None, offset=None):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id WHERE materials.course_id = %s and materials.status=1 order by materials.id desc"
        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            mycursor.execute(sql % (course_id, limit, offset))
        else:
            mycursor.execute(sql % (course_id,))
        materials = mycursor.fetchall()
        return materials

    def get_by_id(self, id):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id WHERE materials.id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        materials = mycursor.fetchone()
        return materials

    def change_status(self, id, status):
        sql = "update materials set status = %s where id = %s;"
        val = (status, id)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            return True
        except:
            mydb.rollback()
            return False

    def delete(self, id):
        sql = "DELETE FROM materials WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def search(self, query, limit, offset):
        sql = "SELECT materials.*, categories.category_name AS category, courses.course_name AS course, users.username AS user FROM materials JOIN categories ON materials.category_id = categories.id JOIN courses ON materials.course_id = courses.id JOIN users ON materials.user_id = users.id WHERE materials.title LIKE %s OR materials.description LIKE %s OR materials.ext LIKE %s OR categories.category_name LIKE %s OR courses.course_name LIKE %s ORDER BY materials.id DESC LIMIT %s OFFSET %s"
        val = (
            "%" + query + "%",
            "%" + query + "%",
            "%" + query + "%",
            "%" + query + "%",
            "%" + query + "%",
            limit,
            offset,
        )
        mycursor.execute(sql, val)
        materials = mycursor.fetchall()
        return materials