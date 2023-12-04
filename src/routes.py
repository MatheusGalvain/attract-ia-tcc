from flask import render_template, request, redirect, url_for, flash, session
from config import db_config
import smtplib
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
from config import API_CHAT_GPT, ID_MODEL, API_KEY
import requests

cursor = db_config.cursor(dictionary=True)


def configure_routes(app):
    # Rota da index
    @app.route('/')
    def home():
        return render_template('index.html')

    # Rota do login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')  # Aqui acontece um with, onde ele conecta com o banco pra
            # verificar se o usuario é cadastrado

            # fazendo um select no usuario e na senha
            cursor.execute("SELECT id, user, name, last_name FROM users WHERE user = %s AND password = %s",
                           (username, password,))
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
    @app.route('/reset-password', methods=['GET', 'POST'])
    def resetpassword():
        if request.method == 'POST':
            email = request.form.get('email')

            # Enviar e-mail
            sender_email = "matheusgalvain@gmail.com"  # Seu e-mail
            receiver_email = email
            password = "your_password"  # Sua senha de e-mail

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = 'Redefinição de senha'

            mail_content = '''Olá,
            Para redefinir sua senha, clique neste link: http://www.example.com/reset-password
            Obrigado.
            '''

            message.attach(MIMEText(mail_content, 'plain'))

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as session:
                    session.login(sender_email, password)
                    session.send_message(message)
            except Exception as e:
                print(f"Erro ao enviar e-mail: {e}")

            # Renderizar a página de confirmação de e-mail enviado
            return render_template('resetpassword.html', email_sent=True)

        return render_template('resetpassword.html', email_sent=False)

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
        if user_id:
            return render_template('profile.html', username=username, name=name)
        else:
            return render_template('login.html', error="Credenciais inválidas")

    # Rota de Editar o Perfil
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

            # Processar o upload da imagem
            if 'profile_image' in request.files:
                profile_image = request.files['profile_image']
                if profile_image.filename != '':
                    # Salvar a imagem em algum diretório, por exemplo, 'static/uploads'
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', secure_filename(profile_image.filename))
                    profile_image.save(image_path)
                    # Armazenar o caminho da imagem na sessão do Flask
                    session['profile_image'] = image_path

            cursor.execute("UPDATE users SET name = %s, email = %s, birth_date = %s, last_name = %s, \
                            password = %s WHERE id = %s",
                           (name, email, birth_date, last_name, password, user_id))
            db_config.commit()

            return redirect(url_for('editprofile'))

    # Rota de Editar os favoritos
    @app.route('/editfavorites')
    def editfavorites():
        return render_template('editfavorites.html')

    # Rota de Editar os favoritos
    @app.route('/about')
    def about():
        return render_template('about.html')

    # Limpa a sessão, deslogando o usuário
    @app.route('/logout')
    def logout():
        session.clear()
        flash('Você foi desconectado com sucesso.', 'logout')
        return redirect(url_for('login'))

    # Rota Home dos quadros
    @app.route('/boards')
    def boards():
        user_id = session['user_id']
        session['username']
        name = session.get('name')  # Obtendo o nome do usuário da sessão
        cursor.execute("SELECT * FROM boards WHERE user_id = %s ORDER BY id DESC LIMIT 5", (user_id,))
        boards = cursor.fetchall()
        return render_template('boards.html', boards=boards, user_name=name)  # Passando o nome do usuário para o template

    # Faz um filtro de apenas 15 caracteres para aparecer na lista dos quadros
    @app.template_filter('limit_length')
    def limit_length(s, max_length):
        print(s)
        if len(s) <= max_length:
            return s
        else:
            return s[:max_length] + '...'

    # Rota que ira trazer a lista dos quadros completa
    @app.route('/boards/all')
    def all_boards():
        user_id = session['user_id']
        cursor.execute("SELECT * FROM boards WHERE user_id = %s", (user_id,))
        boards = cursor.fetchall()
        return render_template('listboards.html', boards=boards)

    # Rota que ira criar um quadro novo
    @app.route('/createboard', methods=['GET', 'POST'])
    def createboard():
        if request.method == 'POST':
            name = request.form.get('name')
            print('NOME')
            print(name)
            user_id = session['user_id']

            # Insira o novo quadro no banco de dados
            cursor.execute("INSERT INTO boards (name, user_id) VALUES (%s, %s)",
                           (name, user_id))
            db_config.commit()

            # Redirecione para alguma página de sucesso ou para a lista de quadros
            return redirect(url_for('boards'))
        return render_template('createboard.html')

    # Rota de Editar os favoritos
    @app.route('/boards/inside/<id>', methods=['GET', 'POST'])
    def boardinside(id):
        session['user_id']
        session['username']
        name = session.get('name')

        cursor.execute("SELECT * FROM boards WHERE id = %s", (id, ))
        board = cursor.fetchone()

        cursor.execute("SELECT * FROM cards WHERE board_id = %s", (id,))
        cards = cursor.fetchall()

        # PUXA AS SUBATIVIDADES DESSE ID
        id_card = 80
        cursor.execute("SELECT * FROM sub_cards WHERE card_id = %s", (id_card,))
        sub_activites = cursor.fetchall()
        return render_template('inboard.html', cards=cards, board=board, user_name=name, sub_activites=sub_activites)

    @app.route('/savecard/<board_id>', methods=['GET', 'POST'])
    def savecard(board_id):
        if request.method == 'POST':
            card_name = request.form.get('cardName')
            # status = request.form.get('status')
            user_id = session['user_id']

            cursor.execute("INSERT INTO cards (name, status, progress, user_id, board_id) VALUES (%s, %s, %s, %s, %s)",
                           (card_name, None, 0, user_id, board_id))
            db_config.commit()

        return redirect(url_for('boardinside', id=board_id))

    @app.route('/deletecard/<board_id>/<card_id>', methods=['GET', 'POST'])
    def deletecard(board_id, card_id):

        cursor.execute("DELETE FROM cards WHERE id = %s", (card_id,))
        db_config.commit()

        return redirect(url_for('boardinside', id=board_id))

    @app.route('/movecard/<status>/<card_id>/<board_id>', methods=['GET', 'POST'])
    def movecard(status, card_id, board_id):

        cursor.execute("UPDATE cards SET status = %s WHERE id = %s",
                       (status, card_id))
        db_config.commit()

        return redirect(url_for('boardinside', id=board_id))

    @app.route('/save-description-card/<card_id>/<board_id>', methods=['GET', 'POST'])
    def savedescriptioncard(card_id, board_id):
        card_description = request.args.get('card_description')
        print('entrou')
        print(card_description)
        cursor.execute("UPDATE cards SET description = %s WHERE id = %s",
                       (card_description, card_id))
        db_config.commit()

        return redirect(url_for('boardinside', id=board_id))

    @app.route('/save-new-sub-activites/<response_user>/<card_id>', methods=['GET', 'POST'])
    def savenewsubactivites(response_user, card_id):
        user_id = session['user_id']
        cursor.execute("INSERT INTO sub_cards (title, sub_title, progress, user_id, card_id) VALUES (%s, %s, %s, %s, %s)",
                       (response_user, None, 0, user_id, card_id))
        db_config.commit()

        cursor.execute("SELECT * FROM sub_cards WHERE card_id = %s", (card_id,))
        sub_cards = cursor.fetchall()
        return sub_cards

    @app.route('/delete-sub-activite/<sub_card_id>/<board_id>', methods=['GET', 'POST'])
    def deletesubactivite(sub_card_id, board_id):
        cursor.execute("DELETE FROM sub_cards WHERE id = %s", (sub_card_id,))
        db_config.commit()
        return redirect(url_for('boardinside', id=board_id))

    @app.route('/sub-activites/chat-gpt/<response_user>/<card_id>', methods=['GET', 'POST'])
    def subactivechatgpt(response_user, card_id):
        user_id = session['user_id']

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        body_message = {
            "model": ID_MODEL,
            "messages": [{"role": "user", "content": f"Me de 5 ideias para implementar em um quadro de gerenciamento \
                           com título e subtítulo, só estes dois itens: {response_user}"}]
        }
        body_message = json.dumps(body_message)
        request = requests.post(API_CHAT_GPT, headers=headers, data=body_message)
        response_data = json.loads(request.text)

        mensagem = response_data['choices'][0]['message']['content']
        linhas = mensagem.split('\n')
        last_card_id = None

        for linha in linhas:
            if 'Título' in linha:
                cursor.execute("INSERT INTO sub_cards (title, sub_title, progress, user_id, card_id) VALUES (%s, %s, %s, %s, %s)",
                               (None, None, 0, user_id, card_id))
                cursor.execute("SELECT id FROM sub_cards ORDER BY id DESC LIMIT 1")
                select_last_card_id = cursor.fetchone()
                last_card_id = select_last_card_id['id']
                title = str(linha.split(': ', 1)[1].replace('"', ''))
                cursor.execute("UPDATE sub_cards SET title = %s WHERE id = %s",
                               (title, last_card_id))
            elif 'Subtítulo' in linha:
                subtitle = str(linha.split(': ', 1)[1].replace('"', ''))
                cursor.execute("UPDATE sub_cards SET sub_title = %s WHERE id = %s",
                               (subtitle, last_card_id))

        # Commit apenas uma vez no final de todas as operações
        db_config.commit()

        cursor.execute("SELECT * FROM sub_cards WHERE card_id = %s", (card_id,))
        sub_cards = cursor.fetchall()

        print(sub_cards)

        return sub_cards

    return app
