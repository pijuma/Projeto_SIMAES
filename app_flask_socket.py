from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import threading
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def landing():
    return "<h1>vingadores dublado</h1>"

@app.route('/enviar', methods=['GET'])
def enviar():
    data = request.headers.get('Data')
    dados_filtrados = filtrar_dados_por_data(data)
    return jsonify(dados_filtrados)

@app.route('/last_update', methods=['GET'])
def last_update():
    try:
        data = get_last_data()[:-1]
        data = json.loads(data)
        return data

    except Exception as err:
        return f"Error: {err}", 200

@app.route('/range', methods=['GET'])
def range():
    data = request.headers.get("Data")
    data_filter = filtrar_dados_por_data(data)
    range_data = request.headers.get("Range")

    range_data = range_data.split("-")
    initial = range_data[0]
    final = range_data[1]

    actual_data = []
    # 'data_hora': '2023-07-12 10:01:38:761274'
    for datas in data_filter:
        if is_in_range(datas['data_hora'][11:19], initial, final):
            actual_data.append(datas)



    return str(f'{actual_data}')
    # return (data, range_data)
    # return json.loads('{"": "", "": "", "": ""}')
    # return jsonify(data)
    # return json.loads(data)
    # data = request.headers.get('Data')
    # dados_filtrados = filtrar_dados_por_data(data)
    # return jsonify(dados_filtrados)

def is_in_range(data, initial, final):
    """11:20:47 09:00:00 12:00:00
        Tipo de dados que sao chamados.
        Realizar filtro a partir disto
    """
    # Horas
    print (data, initial, final)
    if (int(data[0:2]) > int(initial[0:2]) and int(data[0:2]) < int(final[0:2])):
        return True
        # Minutos
    

 # TODO filtrar por minutos

    return False


def get_last_data():
    data = ''
    with open('dados.txt', 'r') as file:
        for lines in file:
            pass

        # pega a ultima linha do arquivo (ultimo dado)
        data = lines

    return data

    

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

        dado['pulsos'] = int(dados_recebidos.split(" ")[1])
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