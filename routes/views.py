from routes import api
from flask import jsonify, request, render_template

from controllers.watcher import Watcher


@api.route('/')
def index():
    watcher = Watcher()
    result = watcher.search('*', offset=0, paginate=20)
    return render_template('index.html', data=result)
    # return jsonify({'name': "Hello World"})


@api.route('/save', methods=['POST'])
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
    offset = data['offset']
    page_num = data['pageNum']

    watcher = Watcher()
    result = watcher.search(query, offset=offset, paginate=page_num)
    return render_template('index.html', data=result)
    # return jsonify({'message': result})
