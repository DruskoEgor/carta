from flask import Flask, render_template, redirect, url_for, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

# Параметры для GitHub API
GITHUB_REPO = "1leidark/carta"
GITHUB_TOKEN = "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"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def trigger_github_action(repo_name, workflow_file, ref="main"):
    url = f"https://api.github.com/repos/{repo_name}/actions/workflows/{workflow_file}/dispatches"
    data = {"ref": ref}
    response = requests.post(url, headers=HEADERS, json=data)
    return response

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

@app.route('/run_parser', methods=['POST'])
def run_parser():
    parser_type = request.form.get("parser_type")

    if parser_type == "benzin":
        workflow_file = "benzin.yml"
    elif parser_type == "electricity":
        workflow_file = "electricity.yml"
    else:
        return jsonify({"error": "Invalid parser type"}), 400

    response = trigger_github_workflow(workflow_file)
    if response.status_code == 204:
        return jsonify({"success": f"Parser '{parser_type}' triggered successfully"}), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
