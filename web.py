"""Panel local de control: una extracción por vez, con progreso consultable."""
from pathlib import Path
from threading import Thread, Lock
from flask import Flask, jsonify, render_template, request, send_from_directory
from instagram_lab.config import RESULTS_DIR
from instagram_lab.service import normalize_profile, run_scrape

app = Flask(__name__)
app.json.ensure_ascii = False
app.config['MAX_CONTENT_LENGTH'] = 4096
lock = Lock()
state = {'status': 'idle', 'events': [], 'file': None, 'error': None}


def worker(target, count):
    def progress(event):
        with lock:
            state['events'].append(event)
    try:
        output = run_scrape(target, count, progress)
        with lock:
            state.update(status='complete', file=output.name)
    except Exception as exc:
        with lock:
            state.update(status='error', error=str(exc))


@app.get('/')
def home():
    return render_template('index.html')


@app.post('/api/jobs')
def start():
    body = request.get_json(silent=True) or {}
    try:
        target = normalize_profile(str(body.get('profile', '')))
        count = int(body.get('posts', 2))
        if not 1 <= count <= 100:
            raise ValueError('Selecciona entre 1 y 100 publicaciones')
    except (ValueError, TypeError) as exc:
        return jsonify(error=str(exc)), 400
    with lock:
        if state['status'] == 'running':
            return jsonify(error='Ya existe una extracción en curso'), 409
        state.update(status='running', events=[], file=None, error=None)
    Thread(target=worker, args=(target, count), daemon=True).start()
    return jsonify(status='running'), 202


@app.get('/api/jobs')
def status():
    with lock:
        return jsonify(state.copy())


@app.get('/downloads/<path:filename>')
def download(filename):
    # Solo nombres de archivos planos .json; no exponemos .env ni cookies.
    if Path(filename).name != filename or not filename.endswith('.json'):
        return jsonify(error='Archivo no permitido'), 404
    return send_from_directory(RESULTS_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    # Exclusivamente local: no abrir este panel a Internet sin autenticación.
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
