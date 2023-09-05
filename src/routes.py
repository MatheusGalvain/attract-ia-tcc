from flask import render_template, request, redirect, url_for, session, flash
from config import db_config
import mysql.connector


def configure_routes(app):
    # Rota da index
    @app.route('/')
    def home():
        return render_template('editprofile.html')

    # Rota do login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Aqui acontece um with, onde ele conecta com o banco pra verificar se o usuario é cadastrado,
            # fazendo um select no usuario e na senha
            with mysql.connector.connect(**db_config) as db_connection:
                db_cursor = db_connection.cursor(dictionary=True)
                db_cursor.execute("SELECT id, user FROM users WHERE user = %s AND password = %s", (username, password))
                user = db_cursor.fetchone()
                db_cursor.close()

            # Se o login for bem-sucedido, crie uma sessão
            if user:
                session['user_id'] = user['id']
                session['username'] = user['user']  # Armazena o nome de usuário na sessão
                return redirect(url_for('welcome'))
            else:
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

            # Conexão com o banco de dados
            with mysql.connector.connect(**db_config) as db_connection:
                db_cursor = db_connection.cursor()

                # Verifica se o usuário já existe
                db_cursor.execute("SELECT id FROM users WHERE user = %s", (user,))
                existing_user = db_cursor.fetchone()

                if existing_user:
                    # Plugin de mensagens de erro
                    flash('Usuário já existente.', 'user_exist_error')
                    return redirect(url_for('register'))
                # Insere o novo usuário no banco de dados
                else:
                    db_cursor.execute("INSERT INTO users (user, password, email, birth_date, last_name, name) \
                                      VALUES (%s, %s, %s, %s, %s, %s)",
                                      (user, password, email, birth_date, last_name, name))
                    db_connection.commit()

                db_cursor.close()
                # Redireciona para a página de login após o registro bem-sucedido
                return redirect(url_for('login'))
        return render_template('register.html')

    # Rota da Alteração de senha
    @app.route('/reset-password')
    def resetpassword():
        return render_template('resetpassword.html')

    # Rota do primeiro quadro
    @app.route('/welcome')
    def welcome():
        user_id = session.get('user_id')
        username = session.get('username')  # Obtenha o nome de usuário da sessão
        # definir os dados do usuario pra no futuro para outros usos da sessão

        if user_id:
            usuario = {'username': username}  # Crie um dicionário com o nome de usuário
            return render_template('welcome.html', usuario=usuario)
        else:
            return render_template('login.html', error="Credenciais inválidas")

    # Rota do Perfil
    @app.route('/perfil')
    def profile():
        return render_template('profile.html')

    # Rota do Perfil
    @app.route('/editperfil')
    def editprofile():
        return render_template('editprofile.html')
    return app
