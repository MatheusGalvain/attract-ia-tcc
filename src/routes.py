from flask import render_template, request, redirect, url_for, session, flash
from config import db_config

cursor = db_config.cursor(dictionary=True)


def configure_routes(app):
    # Rota da index
    @app.route('/')
    def home():
        return render_template('editfavorites.html')

    # Rota do login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')  # Aqui acontece um with, onde ele conecta com o banco pra
            # verificar se o usuario é cadastrado

            # fazendo um select no usuario e na senha
            cursor.execute("SELECT id, user, name, last_name FROM users WHERE user = %s AND password = %s",
                           (username, password))
            user = cursor.fetchone()

            # Se o login for bem-sucedido, crie uma sessão
            if user:
                session['user_id'] = user['id']
                session['username'] = user['user']
                session['name'] = user['name']
                session['last_name'] = user['last_name']

                return redirect(url_for('welcome'))

            else:
                flash('Usuário ou senha incorreta', 'user_exist')
                return redirect(url_for('login'))

        return render_template('login.html')

    # Rota do Registro
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user = request.form.get('user')
            name = request.form.get('name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            birth_date = request.form.get('birth_date')
            password = request.form.get('password')

            # Verifica se o usuário já existe
            cursor.execute("SELECT id FROM users WHERE user = %s", (user,))
            existing_user = cursor.fetchone()

            if existing_user:
                # Plugin de mensagens de erro
                flash('Usuário já existente.', 'user_exist_error')
                return redirect(url_for('register'))
            # Insere o novo usuário no banco de dados
            else:
                cursor.execute("INSERT INTO users (user, password, email, birth_date, last_name, name) \
                                VALUES (%s, %s, %s, %s, %s, %s)",
                               (user, password, email, birth_date, last_name, name))
                db_config.commit()
                cursor.execute("SELECT * FROM users WHERE user = %s", (user, ))
                users = cursor.fetchone()
                # cursor.execute("SELECT * FROM has_seen_first_card WHERE user_id = %s", (users['id']))
                # has = cursor.fetchone()
                cursor.execute("INSERT INTO has_seen_first_card (seen_card, user_id) \
                                VALUES (%s, %s)",
                               (False, users['id'], ))
                db_config.commit()

            cursor.close()
            # Redireciona para a página de login após o registro bem-sucedido
            return redirect(url_for('login'))
        return render_template('register.html')

    # Rota da Alteração de senha
    @app.route('/reset-password')
    def resetpassword():
        return render_template('resetpassword.html')

    # Rota do primeiro quadro
    @app.route('/welcome', methods=['GET', 'POST'])
    def welcome():
        user_id = session['user_id']
        username = session['username']
        username = username.capitalize()

        cursor.execute("SELECT * FROM has_seen_first_card WHERE user_id = %s", (user_id,))
        has_seen_first_card = cursor.fetchone()

        if user_id:
            if has_seen_first_card['seen_card']:
                return redirect(url_for('profile'))
            else:
                usuario = {'username': username}  # Crie um dicionário com o nome de usuário
                cursor.execute("UPDATE has_seen_first_card SET seen_card = True WHERE user_id = %s",
                               (user_id, ))
                db_config.commit()
                return render_template('welcome.html', usuario=usuario)
        else:
            return render_template('login.html', error="Credenciais inválidas")

    # Rota do Perfil
    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        user_id = session['user_id']
        username = session['username']
        name = session.get('name')
        name = name.capitalize()  # Primeira letra maiscula do nome
        last_name = session.get('last_name')  # Ultimo Nome
        last_name = last_name.capitalize()  # Primeira letra maiscula do sobrenome

        if user_id:
            return render_template('profile.html', username=username, name=name, last_name=last_name)
        else:
            return render_template('login.html', error="Credenciais inválidas")

    # Rota do Perfil
    @app.route('/editprofile', methods=['GET', 'POST'])
    def editprofile():
        user_id = session['user_id']

        if request.method == 'GET':
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            return render_template('editprofile.html', user=user, user_id=user_id)

        if request.method == 'POST':
            name = request.form['name']
            last_name = request.form['last_name']
            email = request.form['email']
            birth_date = request.form['birth_date']
            password = request.form['password']

            cursor.execute("UPDATE users SET name = %s, email = %s, birth_date = %s, last_name = %s, \
                            password = %s WHERE id = %s",
                           (name, email, birth_date, last_name, password, user_id))
            db_config.commit()

            return redirect(url_for('editprofile'))

    @app.route('/editfavorites')
    def editfavorites():
        return render_template('editfavorites.html')
    return app
