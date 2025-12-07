from flask import Flask, request, redirect, url_for, session, render_template_string, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# -----------------------
# Base de datos
# -----------------------
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -----------------------
# Funciones de usuarios
# -----------------------
def get_user(username):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password, is_admin FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# -----------------------
# Rutas
# -----------------------

# Página principal
@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    conn.close()
    index_html = '''
    <h1>Mi Blog</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul>
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    {% if 'username' in session %}
        <p>Hola {{ session['username'] }}! <a href="{{ url_for('logout') }}">Salir</a></p>
        {% if session['is_admin'] %}
            <p><a href="{{ url_for('admin') }}">Panel de Administración</a></p>
        {% endif %}
    {% else %}
        <p><a href="{{ url_for('login') }}">Login</a> | <a href="{{ url_for('register') }}">Registrarse</a></p>
    {% endif %}
    <hr>
    {% for post in posts %}
        <div class="post">
            <h2>{{ post[1] }}</h2>
            <p>{{ post[2] }}</p>
            {% if 'username' in session and session['is_admin'] %}
                <p>
                    <a href="{{ url_for('edit_post', post_id=post[0]) }}">Editar</a> | 
                    <a href="{{ url_for('delete_post', post_id=post[0]) }}" onclick="return confirm('¿Seguro que quieres eliminar este post?');">Eliminar</a>
                </p>
            {% endif %}
        </div>
        <hr>
    {% endfor %}
    '''
    return render_template_string(index_html, posts=posts)

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        is_admin = 1 if request.form.get('is_admin') == 'on' else 0
        try:
            conn = sqlite3.connect('blog.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                      (username, password, is_admin))
            conn.commit()
            conn.close()
            flash('Usuario registrado correctamente. Puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El usuario ya existe.', 'danger')
    register_html = '''
    <h1>Registro</h1>
    <form method="post">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        Administrador: <input type="checkbox" name="is_admin"><br>
        <input type="submit" value="Registrar">
    </form>
    <p>Ya tienes cuenta? <a href="{{ url_for('login') }}">Login</a></p>
    '''
    return render_template_string(register_html)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['is_admin'] = user[3]
            flash('Login exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    login_html = '''
    <h1>Login</h1>
    <form method="post">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>Si eres administrador y no hay cuenta, usa <a href="{{ url_for('register') }}">/register</a></p>
    <p><a href="{{ url_for('reset_password') }}">Restablecer contraseña</a></p>
    '''
    return render_template_string(login_html)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Panel de administración
@app.route('/admin')
def admin():
    if 'username' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    admin_html = '''
    <h1>Panel de Administración</h1>
    <p><a href="{{ url_for('create_post') }}">Crear Post</a></p>
    <p><a href="{{ url_for('manage_users') }}">Administrar Usuarios</a></p>
    <p><a href="{{ url_for('index') }}">Volver al inicio</a></p>
    '''
    return render_template_string(admin_html)

# Crear post
@app.route('/admin/create', methods=['GET', 'POST'])
def create_post():
    if 'username' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    create_html = '''
    <h1>Crear Post</h1>
    <form method="post">
        Título: <input type="text" name="title"><br>
        Contenido:<br>
        <textarea name="content" rows="5" cols="40"></textarea><br>
        <input type="submit" value="Crear">
    </form>
    <p><a href="{{ url_for('admin') }}">Volver al panel</a></p>
    '''
    return render_template_string(create_html)

# Editar post
@app.route('/admin/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM posts WHERE id=?", (post_id,))
    post = c.fetchone()
    if request.method == 'POST':
        c.execute("UPDATE posts SET title=?, content=? WHERE id=?",
                  (request.form['title'], request.form['content'], post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    edit_html = '''
    <h1>Editar Post</h1>
    <form method="post">
        Título: <input type="text" name="title" value="{{ post[1] }}"><br>
        Contenido:<br>
        <textarea name="content" rows="5" cols="40">{{ post[2] }}</textarea><br>
        <input type="submit" value="Actualizar">
    </form>
    <p><a href="{{ url_for('admin') }}">Volver al panel</a></p>
    '''
    return render_template_string(edit_html, post=post)

# Eliminar post
@app.route('/admin/delete/<int:post_id>')
def delete_post(post_id):
    if 'username' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()
    flash('Post eliminado correctamente.', 'success')
    return redirect(url_for('index'))

# -----------------------
# Restablecer contraseña
# -----------------------
@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = generate_password_hash(request.form['new_password'])
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()
        flash('Contraseña actualizada.', 'success')
        return redirect(url_for('login'))
    reset_html = '''
    <h1>Restablecer Contraseña</h1>
    <form method="post">
        Usuario: <input type="text" name="username"><br>
        Nueva Contraseña: <input type="password" name="new_password"><br>
        <input type="submit" value="Restablecer">
    </form>
    <p><a href="{{ url_for('login') }}">Volver al login</a></p>
    '''
    return render_template_string(reset_html)

# -----------------------
# Administrar usuarios
# -----------------------
@app.route('/admin/users')
def manage_users():
    if 'username' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT id, username, is_admin FROM users")
    users = c.fetchall()
    conn.close()
    return render_template_string('''
        <h1>Administrar Usuarios</h1>
        <p><a href="{{ url_for('admin') }}">Volver al panel</a></p>
        <table border="1" cellpadding="5">
            <tr><th>Usuario</th><th>Administrador</th><th>Acciones</th></tr>
            {% for user in users %}
                <tr>
                    <td>{{ user[1] }}</td>
                    <td>{{ 'Sí' if user[2] else 'No' }}</td>
                    <td>
                        <a href="{{ url_for('change_user_password', user_id=user[0]) }}">Cambiar contraseña</a>
                    </td>
                </tr>
            {% endfor %}
        </table>
    ''', users=users)

@app.route('/admin/users/<int:user_id>/change_password', methods=['GET', 'POST'])
def change_user_password(user_id):
    if 'username' not in session or not session['is_admin']:
        return redirect(url_for('login'))
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    if not user:
        conn.close()
        return "Usuario no encontrado."
    if request.method == 'POST':
        new_password = generate_password_hash(request.form['new_password'])
        c.execute("UPDATE users SET password=? WHERE id=?", (new_password, user_id))
        conn.commit()
        conn.close()
        flash(f"Contraseña de {user[1]} actualizada correctamente.", "success")
        return redirect(url_for('manage_users'))
    conn.close()
    return render_template_string('''
        <h1>Cambiar contraseña de {{ user[1] }}</h1>
        <form method="post">
            Nueva contraseña: <input type="password" name="new_password"><br>
            <input type="submit" value="Actualizar">
        </form>
        <p><a href="{{ url_for('manage_users') }}">Volver a administrar usuarios</a></p>
    ''', user=user)

# -----------------------
# Ejecutar app
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
