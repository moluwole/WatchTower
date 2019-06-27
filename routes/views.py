from routes import api
from flask import jsonify, request

from controllers.Watcher import Watcher


@api.route('/')
def index():
    return jsonify({'name': "Hello World"})


@api.route('/save', methods=['GET', 'POST'])
def save():
    data = request.args

    client_ip = data['clientIp']
    service = data['service']
    error_message = data['errorMessage']
    stack_trace = data['stackTrace']
    client_id = data['clientId']

    watcher = Watcher()
    result = watcher.save(client_ip, service, error_message, stack_trace, client_id)
    return jsonify({'message': result})


@api.route('/search', methods=['GET', 'POST'])
def search():
    data = request.args

    query = data['query']

    watcher = Watcher()
    result = watcher.search(query)
    return jsonify({'message': result})