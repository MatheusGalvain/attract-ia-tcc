# Importações de arquivos e bibliotecas
from flask import Flask
from config import SECRET_KEY
from flask_session import Session
from routes import configure_routes

app = Flask(__name__)
# Definições da sessao do usuario através do flask session
# Ele basicamente cria uma sessao unica pro usuario
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.secret_key = SECRET_KEY

# Configura as rotas
configure_routes(app)

# Reccarega automatico "Quando em ambiente teste"
if __name__ == '__main__':
    app.run(debug=True)

# Carrega as telas simultaeamente, em vez de rodar uma por uma "Dimuindo
# o tempo de carregamento"
# app.run(thread=True)
