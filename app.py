#!/usr/bin/env python3
"""
perf-test-assistant Web UI (Flask)
"""

from flask import Flask, render_template_string, request, jsonify
from tester import generate_locust_script, generate_test_strategy, analyze_perf_results

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perf Test Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5rem; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        .tabs { display: flex; gap: 10px; margin-bottom: 25px; }
        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            background: #f5f5f5;
            transition: all 0.2s;
            font-weight: 500;
        }
        .tab.active { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .step { margin-bottom: 20px; }
        .step-title { font-size: 1.1rem; font-weight: bold; color: #333; margin-bottom: 10px; }
        textarea, input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
        }
        textarea { min-height: 100px; resize: vertical; }
        textarea:focus, input:focus { outline: none; border-color: #f5576c; }
        button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
            border-radius: 8px;
            white-space: pre-wrap;
            display: none;
            line-height: 1.6;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
        }
        .result.show { display: block; }
        .loading { text-align: center; display: none; padding: 20px; }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #f5576c;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .row { display: flex; gap: 15px; }
        .row > div { flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Perf Test Assistant</h1>
        
        <div class="card">
            <div class="tabs">
                <div class="tab active" onclick="switchTab('locust')">Locust脚本生成</div>
                <div class="tab" onclick="switchTab('strategy')">测试策略设计</div>
                <div class="tab" onclick="switchTab('analyze')">结果分析</div>
            </div>

            <div id="locust" class="tab-content active">
                <div class="step">
                    <div class="step-title">接口信息</div>
                    <textarea id="api_info" placeholder="例如：登录接口 POST https://api.example.com/login，参数 username/password，返回token"></textarea>
                </div>
                <div class="row">
                    <div class="step">
                        <div class="step-title">并发用户数</div>
                        <input type="number" id="users" value="100">
                    </div>
                    <div class="step">
                        <div class="step-title">压测时长</div>
                        <input type="text" id="duration" value="60s">
                    </div>
                </div>
                <button onclick="generateLocust()">生成Locust脚本</button>
            </div>

            <div id="strategy" class="tab-content">
                <div class="step">
                    <div class="step-title">业务场景描述</div>
                    <textarea id="scenario" placeholder="例如：电商首页，预计峰值QPS 500，日常QPS 100，大促期间预计10倍流量"></textarea>
                </div>
                <button onclick="generateStrategy()">生成测试策略</button>
            </div>

            <div id="analyze" class="tab-content">
                <div class="step">
                    <div class="step-title">压测结果数据</div>
                    <textarea id="metrics" placeholder="例如：TPS: 300, P50: 200ms, P95: 800ms, P99: 1500ms, 错误率: 2%, CPU: 85%, 内存: 70%"></textarea>
                </div>
                <button onclick="analyzeResults()">分析结果</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI 正在处理中...</p>
            </div>

            <div class="result" id="result"></div>
        </div>
    </div>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function showLoading() {
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
        }

        function hideLoading() {
            document.getElementById('loading').classList.remove('show');
        }

        async function callApi(endpoint, data) {
            showLoading();
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await response.json();
            hideLoading();
            document.getElementById('result').textContent = result.result;
            document.getElementById('result').classList.add('show');
        }

        function generateLocust() {
            callApi('/api/locust', {
                api: document.getElementById('api_info').value,
                users: document.getElementById('users').value,
                duration: document.getElementById('duration').value
            });
        }

        function generateStrategy() {
            callApi('/api/strategy', {
                scenario: document.getElementById('scenario').value
            });
        }

        function analyzeResults() {
            callApi('/api/analyze', {
                metrics: document.getElementById('metrics').value
            });
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/locust', methods=['POST'])
def api_locust():
    data = request.json
    result = generate_locust_script(data.get('api', ''), data.get('users', 100), data.get('duration', '60s'))
    return jsonify({'result': result})


@app.route('/api/strategy', methods=['POST'])
def api_strategy():
    data = request.json
    result = generate_test_strategy(data.get('scenario', ''))
    return jsonify({'result': result})


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    result = analyze_perf_results(data.get('metrics', ''))
    return jsonify({'result': result})


if __name__ == '__main__':
    print("⚡ Perf Test Assistant 启动中...")
    print("📖 访问 http://localhost:5005")
    app.run(debug=True, port=5005)
