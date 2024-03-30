#!/usr/bin/env python3
from datetime import datetime
import os
import subprocess
import tarfile
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/upload', methods=['GET', 'POST'])
def upload():
    dest = os.path.abspath(request.form.get('dest') or '.')
    compressed = bool(request.form.get('compressed'))
    file = request.files['file']
    if file and not compressed:
        file.save(os.path.join(dest, file.filename))
    elif file and compressed:
        if file.filename.endswith('.tar.xz'):
            tarfile.open(mode='r:xz', fileobj=file).extractall(dest)
        else:
            return {'status':'unsupported file'}
    return {'status':'success'}


@app.route('/api/shell', methods=['GET', 'POST'])
def shell():
    shell = request.form.get('shell') or request.args.get('shell')
    cp = subprocess.run(shell, capture_output=True, shell=True)
    return {
        'status':'success',
        'data':{
            'out':str(cp.stdout, 'utf-8'),
            'err': str(cp.stderr, 'utf-8')
        }
    }

@app.route('/api/clone', methods=['GET', 'POST'])
def clone():
    repo = request.form.get('repo') or request.args.get('repo')
    cp = subprocess.run(f'git clone {repr(repo)}', capture_output=True, shell=True)
    return {
        'status':'success',
        'data':{
            'out':str(cp.stdout, 'utf-8'),
            'err': str(cp.stderr, 'utf-8')
        }
    }

@app.route('/api/commit', methods=['GET', 'POST'])
def commit():
    path = request.form.get('path') or request.args.get('path')
    cp = subprocess.run(f'cd {repr(path)} && git add . && git commit -a -m {repr("Avatar Auto Commit @ "+str(datetime.now().isoformat()))} && git push --all', capture_output=True, shell=True)
    return {
        'status':'success',
        'data':{
            'out':str(cp.stdout, 'utf-8'),
            'err': str(cp.stderr, 'utf-8')
        }
    }



if __name__ == "__main__":
    app.run(host=os.environ.get('IP', '::'), port=os.environ.get('PORT', 10000), debug=False, use_reloader=False)
