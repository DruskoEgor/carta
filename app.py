from flask import Flask, render_template, redirect, url_for
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('index.html', data=data)

@app.route('/update_benzin', methods=['POST'])
def update_benzin():
    subprocess.run(['python', 'benzin.py'])
    return redirect(url_for('home'))

@app.route('/update_electric', methods=['POST'])
def update_electric():
    subprocess.run(['python', 'electricity.py'])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

