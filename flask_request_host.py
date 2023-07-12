from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import threading
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/enviar', methods=['GET'])
def enviar():
    data = request.headers.get('Data')
    dados_filtrados = filtrar_dados_por_data(data)
    return jsonify(dados_filtrados)

@app.route('/last_update', methods=['GET'])
def last_update():
    data = get_last_update()
    if data is None:
        return jsonify(None)
    return jsonify(data)

@app.route('/range', methods=['GET'])
def range_data():
    data = request.headers.get('Data')
    range = request.headers.get('Range')
    dados_filtrados = filtrar_dados_por_range(data, range)
    return jsonify(dados_filtrados)

def get_last_update():
    now = datetime.now()
    with open('dados.txt', 'r') as arquivo_txt:
        lines = arquivo_txt.readlines()
        for line in reversed(lines):
            dado = json.loads(line)
            data_hora = datetime.strptime(dado['data_hora'], "%Y-%m-%d %H:%M:%S:%f%Z")
            diff = now - data_hora
            if diff.total_seconds() <= 3:
                return dado
    return None

def filtrar_dados_por_range(data, range):
    range_inicio, range_fim = range.split('-')
    data_inicio = f"{data} {range_inicio}"
    data_fim = f"{data} {range_fim}"

    dados_filtrados = []
    with open('dados.txt', 'r') as arquivo_txt:
        for linha in arquivo_txt:
            dado = json.loads(linha)
            if data_inicio <= dado['data_hora'] <= data_fim:
                dados_filtrados.append(dado)
    return dados_filtrados

def adicionar_data_hora(dado):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f%Z")
    dado['data_hora'] = str(data_hora)
    print("-----------", str(data_hora))
    return dado

def filtrar_dados_por_data(data):
    dados_filtrados = []
    with open('dados.txt', 'r') as arquivo_txt:
        for linha in arquivo_txt:
            dado = json.loads(linha)
            if dado['data_hora'].startswith(data):
                dados_filtrados.append(dado)
    return dados_filtrados

def salvar_dados_em_txt(dado):
    with open('dados.txt', 'a') as arquivo_txt:
        json_str = json.dumps(dado)
        arquivo_txt.write(json_str + '\n')

def handle_client(conexao, endereco_cliente):
    while True:
        dados_recebidos = conexao.recv(1024).decode('utf-8')

        if not dados_recebidos:
            break
        dado = {}

        pulsos_str = dados_recebidos.split(" ")[1]
        pulsos_num = re.findall('\d+', pulsos_str)
        if pulsos_num:
            dado['pulsos'] = int(pulsos_num[0])

        dado = adicionar_data_hora(dado)
        dado['endereco_cliente'] = endereco_cliente

        salvar_dados_em_txt(dado)

    conexao.close()

def iniciar_servidor_socket():
    endereco = '192.168.0.7'
    porta = 60000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((endereco, porta))
    sock.listen(1)

    while True:
        conexao, endereco_cliente = sock.accept()
        print("Nova conexão aceita:", endereco_cliente)

        client_thread = threading.Thread(target=handle_client, args=(conexao, endereco_cliente))
        client_thread.start()

def iniciar_servidor_flask():
    endereco = '192.168.0.7'
    app.run(host=endereco, port=5500)

if __name__ == '__main__':
    socket_thread = threading.Thread(target=iniciar_servidor_socket)
    socket_thread.start()

    flask_thread = threading.Thread(target=iniciar_servidor_flask)
    flask_thread.start()