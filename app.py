from flask import Flask, render_template, redirect, url_for, request, jsonify
import subprocess
import json
import requests

app = Flask(__name__)

# Параметры для GitHub API
GITHUB_REPO = "1leidark/carta"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"

# Ваш токен
GITHUB_TOKEN = "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"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def trigger_github_action(repo_name, workflow_file, ref="main"):
    url = f"https://api.github.com/repos/{repo_name}/actions/workflows/{workflow_file}/dispatches"
    data = {
        "ref": ref
    }
    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 204:
        print(f"Workflow {workflow_file} запущен успешно!")
    else:
        print(f"Ошибка запуска workflow: {response.status_code}")
        print(response.json())


@app.route('/')
def home():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('index.html', data=data)

@app.route('/update_benzin', methods=['POST'])
def update_benzin():
    # Локальный запуск парсера
    subprocess.run(['python', 'benzin.py'])
    return redirect(url_for('home'))

@app.route('/update_electric', methods=['POST'])
def update_electric():
    # Локальный запуск парсера
    subprocess.run(['python', 'electricity.py'])
    return redirect(url_for('home'))

@app.route('/run_parser', methods=['POST'])
def run_parser():
    # Запуск парсеров через GitHub Actions
    parser_type = request.form.get("parser_type")

    if parser_type == "benzin":
        event_type = "run-benzin-parser"
    elif parser_type == "electricity":
        event_type = "run-electricity-parser"
    else:
        return jsonify({"error": "Invalid parser type"}), 400

    response = requests.post(
        GITHUB_API_URL,
        json={"event_type": event_type}
    )

    if response.status_code == 204:
        return jsonify({"success": f"Parser '{parser_type}' triggered successfully"}), 200
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
