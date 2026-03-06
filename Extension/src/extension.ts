import * as vscode from 'vscode';
import { CognicodeViewProvider } from './CognicodeViewProvider';

export function activate(context: vscode.ExtensionContext) {

    const provider = new CognicodeViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            CognicodeViewProvider.viewType,
            provider
        )
    );

    const disposable = vscode.commands.registerCommand("cognicode.analyze", async () => {

        const editor = vscode.window.activeTextEditor;

        if (!editor) {
            vscode.window.showErrorMessage("No file open.");
            return;
        }

        const code = editor.document.getText();
        const language = editor.document.languageId;

        try {
            const response = await fetch("http://localhost:5000/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    code: code,
                    language: language
                })
            });

            if (!response.ok) {
                throw new Error("Failed to connect to backend");
            }

            const result = await response.json();
            provider.updateResults(result);

        } catch (error) {
            vscode.window.showErrorMessage("Cognicode backend error: " + (error instanceof Error ? error.message : "Unknown error"));
        }

    });

    context.subscriptions.push(disposable);
}

export function deactivate() { }