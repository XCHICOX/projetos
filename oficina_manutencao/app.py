import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'manutencoes.json'

def load_data():
    try:
        with open(DATABASE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(data):
    with open(DATABASE, 'w') as f:
        json.dump(data, f, indent=4)

@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

@app.route('/', methods=['GET', 'POST'])
def manutencoes():
    if request.method == 'POST':
        if 'add' in request.form:
            new_manutencao = {
                'data': request.form['data'],
                'placa': request.form['placa'],
                'informacoes': request.form['informacoes'],
                'usuario': request.form['usuario'],
                'valor': request.form['valor']
            }
            data = load_data()
            data.append(new_manutencao)
            save_data(data)
        elif 'edit' in request.form:
            index = int(request.form['edit'])
            data = load_data()
            data[index] = {
                'data': request.form['data'],
                'placa': request.form['placa'],
                'informacoes': request.form['informacoes'],
                'usuario': request.form['usuario'],
                'valor': request.form['valor']
            }
            save_data(data)
        elif 'delete' in request.form:
            index = int(request.form['delete'])
            data = load_data()
            data.pop(index)
            save_data(data)
        return redirect(url_for('manutencoes'))
    
    data = load_data()
    return render_template('manutencoes.html', manutencoes=data)

if __name__ == '__main__':
    app.run(debug=True)
