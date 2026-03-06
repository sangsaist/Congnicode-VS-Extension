import * as vscode from 'vscode';

export class CognicodeViewProvider implements vscode.WebviewViewProvider {

    public static readonly viewType = 'cognicodeView';

    private _view?: vscode.WebviewView;

    constructor(private readonly _extensionUri: vscode.Uri) { }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview();

        webviewView.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'analyze':
                    vscode.commands.executeCommand('cognicode.analyze');
                    return;
            }
        });
    }

    public updateResults(data: any) {
        if (!this._view) {
            return;
        }

        const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            padding: 10px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-sideBar-background);
        }
        .section {
            background: #1e1e1e;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid var(--vscode-button-background);
        }
        .section.success {
            border-left-color: #4caf50;
        }
        .section.warning {
            border-left-color: #ff9800;
        }
        .impact-container {
            margin-bottom: 20px;
            text-align: center;
        }
        .progress-bar {
            background: #333;
            height: 12px;
            border-radius: 6px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            transition: width 0.5s ease-out;
        }
        .complexity-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 10px;
        }
        .complexity-card {
            background: #252526;
            padding: 8px;
            border-radius: 4px;
            text-align: center;
        }
        .complexity-card small {
            display: block;
            color: var(--vscode-descriptionForeground);
            font-size: 0.7rem;
            text-transform: uppercase;
        }
        .complexity-card span {
            font-size: 0.85rem;
            font-weight: bold;
            color: var(--vscode-charts-blue);
        }
        h3 {
            margin-top: 0;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: var(--vscode-descriptionForeground);
            text-transform: uppercase;
        }
        p {
            margin: 0;
            line-height: 1.4;
            font-size: 0.95rem;
        }
        pre {
            background: #111;
            padding: 10px;
            overflow-x: auto;
            border-radius: 4px;
            font-family: var(--vscode-editor-font-family);
            font-size: 0.85rem;
            margin-top: 8px;
            white-space: pre-wrap;
        }
        button {
            width: 100%;
            padding: 8px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            cursor: pointer;
            font-weight: bold;
            margin-bottom: 20px;
        }
        button:hover { background: var(--vscode-button-hoverBackground); }
    </style>
</head>
<body>
    <button onclick="analyze()">Analyze Code</button>

    <div class="impact-container">
        <h3>Optimization Impact: ${data.optimization_impact || 'None'}</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${(data.speedup_score || 0) * 10}%; background: ${(data.speedup_score || 0) > 7 ? '#4caf50' :
                (data.speedup_score || 0) > 4 ? '#ff9800' :
                    '#f44336'
            }"></div>
        </div>
        <p style="font-size: 0.8rem; color: var(--vscode-descriptionForeground); margin-top: 5px;">
            Score: ${data.speedup_score || 0}/10 ${data.theoretical_speedup ? `| Est. Speedup: <b>${data.theoretical_speedup}</b>` : ''}
        </p>
    </div>

    <div class="section">
        <h3>Algorithm Detected</h3>
        <p>${data.algorithm_detected || 'N/A'}</p>
    </div>

    <div class="complexity-grid">
        ${data.best_time_complexity && !['N/A', 'NA', 'Unknown', ''].includes(data.best_time_complexity) ? `
        <div class="complexity-card">
            <small>Best Time</small>
            <span>${data.best_time_complexity}</span>
        </div>` : ''}
        ${data.worst_time_complexity && !['N/A', 'NA', 'Unknown', ''].includes(data.worst_time_complexity) ? `
        <div class="complexity-card">
            <small>Worst Time</small>
            <span>${data.worst_time_complexity}</span>
        </div>` : ''}
        ${data.space_complexity && !['N/A', 'NA', 'Unknown', ''].includes(data.space_complexity) ? `
        <div class="complexity-card" style="grid-column: span 2;">
            <small>Space Complexity</small>
            <span>${data.space_complexity}</span>
        </div>` : ''}
    </div>

    <div class="section ${data.problem === 'No major issue detected' ? 'success' : 'warning'}">
        <h3>Problem</h3>
        <p>${data.problem === 'No major issue detected' ? '✅ ' : '⚠️ '}${data.problem || 'No specific issue detected'}</p>
    </div>

    ${data.explanation ? `
    <div class="section">
        <h3>Explanation</h3>
        <p>${data.explanation}</p>
    </div>` : ''}

    <div class="section">
        <h3>Suggested Algorithm</h3>
        <p>${data.suggested_algorithm || 'N/A'}</p>
    </div>

    ${data.suggested_algorithm !== 'No improvement required' ? `
    <div class="section">
        <h3>Improved Complexity</h3>
        <p>${data.improved_complexity || 'N/A'}</p>
    </div>

    <div class="section">
        <h3>Improved Code</h3>
        <pre>${data.improved_code || 'No improvements suggested.'}</pre>
    </div>
    ` : `
    <div class="section success">
        <p>🎉 Your code is already optimal!</p>
    </div>
    `}

    <script>
        const vscode = acquireVsCodeApi();
        function analyze() {
            vscode.postMessage({ command: 'analyze' });
        }
    </script>
</body>
</html>`;

        this._view.webview.html = html;
    }

    private _getHtmlForWebview() {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            padding: 10px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-sideBar-background);
            text-align: center;
        }
        button {
            width: 100%;
            padding: 8px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background: var(--vscode-button-hoverBackground); }
        .idle-text {
            margin-top: 20px;
            color: var(--vscode-descriptionForeground);
            font-style: italic;
        }
    </style>
</head>
<body>
    <button onclick="analyze()">Analyze Code</button>
    <div class="idle-text">Open a file and click analyze to see results.</div>
    <script>
        const vscode = acquireVsCodeApi();
        function analyze() {
            vscode.postMessage({ command: 'analyze' });
        }
    </script>
</body>
</html>`;
    }
}
