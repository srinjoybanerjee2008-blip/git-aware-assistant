// Minimal VS Code extension that runs the CLI and returns output into an output channel.
// Build with `npm install` then `npm run build` in the vscode-extension folder.

import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('gitAwareAssistant.ask', async () => {
        const query = await vscode.window.showInputBox({ prompt: 'Ask the Git-Aware Assistant' });
        if (!query) { return; }
        const workspace = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : undefined;
        const cliPath = path.join(workspace || '.', 'cli.py');

        const channel = vscode.window.createOutputChannel('Git-Aware Assistant');
        channel.show(true);
        channel.appendLine(`Running: python ${cliPath} "${query}"`);
        const cmd = `python "${cliPath}" "${query}" --collection default`;

        const p = exec(cmd, { cwd: workspace });
        p.stdout?.on('data', (data) => channel.append(data.toString()));
        p.stderr?.on('data', (data) => channel.append(data.toString()));
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
