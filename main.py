import os

import requests
from flask import Flask, request, jsonify

from utils.logger import log_info, log_error
from retrieval_query import parse_retrieval_query
from retrieval_test import run_retrieval_test

app = Flask(__name__)

# GitHub 访问令牌和仓库信息
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
TRIGGER_WORD = 'trigger:run_retrieval_test'  # 触发词

# Headers for GitHub API requests
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    issue_url = data['issue']['url']

    if data['action'] == 'created' and 'issue' in data:
        comment = data['comment']['body']
        # issue_number = data['issue']['number']
        if TRIGGER_WORD in comment:
            error, retrieval_query = parse_retrieval_query(comment)
            if error:
                post_comment(issue_url, f"Error - fail to parse retrieval query: {error}")
            else:
                log_info(f"parsed query: {retrieval_query}")
                error, retrieval_result = run_retrieval_test(retrieval_query)
                if error:
                    post_comment(issue_url, f"Error - fail to run retrieval test: {error}")
                else:
                    post_comment(issue_url, retrieval_result)

    return jsonify({'message': 'OK'})


def post_comment(issue_url, comment):
    url = f'{issue_url}/comments'
    payload = {'body': comment}
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 201:
        log_info(f'Successfully posted comment to issue #{issue_url}')
    else:
        log_error(f'Failed to post comment to issue #{issue_url}: {response.content}')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9563, debug=True)
