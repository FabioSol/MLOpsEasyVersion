from flask import Flask, request, jsonify
import os
import subprocess

model_repo = 'https://github.com/FabioSol/AidsModel.git'
repo_path = '/app/model'

app = Flask(__name__)

def start_up():
    subprocess.run(['git', 'clone', model_repo, repo_path])

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Handle the webhook payload
        data = request.json
        # Verify the event type
        if data.get('ref') == 'refs/heads/main':  # Adjust branch as needed
            # Pull the latest code
            if os.path.exists(repo_path):
                subprocess.run(['git', '-C', repo_path, 'pull'])
            else:
                subprocess.run(['git', 'clone', model_repo, repo_path])
        return jsonify({'status': 'success'})


if __name__ == '__main__':
    start_up()
    app.run(host='0.0.0.0', port=5000)
