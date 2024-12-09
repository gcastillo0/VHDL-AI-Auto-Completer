// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as child_process from 'child_process';
import { getVHDLCompletion } from './languageModelService';


let serverProcess: child_process.ChildProcess | null = null;

function startServer(){
	const command = './Documents/ECE465/test-hello-world/src/local-server/server_env/bin/python ./Documents/ECE465/test-hello-world/src/local-server/local-server.py';
	try{
		serverProcess = child_process.spawn(command, { shell: true });
		if(serverProcess.stdout){
			serverProcess.stdout.on('data', (data) => {
			    console.log('server stdout: ',data.toString());
			});
		}
		if(serverProcess.stderr){
			serverProcess.stderr.on('data', (data) => {
			    console.log('server stderr: ',data.toString());
			});
		}
		serverProcess.on('close', (code) => {
		    if (code !== 0) {
		        console.error('Python server process exited with code', code);
		    }
		});
		console.log('Python server started');
	    } catch (error) {
		console.error('Failed to start Python server:', error);
	    }
}
function stopServer(){
	if (serverProcess) {
		console.log('Stopping Server...');
		serverProcess.kill('SIGINT');
		serverProcess = null;
	} else {
		console.log('No server process to stop.');
	}
}
export function activate(context: vscode.ExtensionContext) {
	
	//startServer();
	console.log('Your AI VHDL autocompletion extension is know active');
	
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('test-hello-world.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World AI from test Hello World!');
	});
	const provider = vscode.languages.registerCompletionItemProvider(
		{ scheme: 'file', language: 'plaintext' },
		{
			async provideCompletionItems(document, position) {
				const triggerCharacters = [' ','.', ':',';', '_', '(','\n'];
				const charBeforeCursor = document.getText(new vscode.Range(position.translate(0, -1), position));
	
				// Only trigger if the character before the cursor is a trigger character
				if (!triggerCharacters.includes(charBeforeCursor)) {
					return undefined;
				}
				const max_input = 64;
				let aux;
				if (position.character>max_input){
					aux = position.translate(0,-max_input);
				} else {
				 	aux = new vscode.Position(0,0);
				}
				const lineText = document.getText(new vscode.Range(aux,position))
				//const lineText = document.lineAt(position).text.substring(0,position.character);
				if (!lineText.trim()){
					return undefined;
				}
				const suggestions = await getVHDLCompletion(lineText);
				// const startPos = new vscode.Position(position.line, 0);
				// const replaceRange = new vscode.Range(startPos, position);
				// const completionItems = suggestions.map((suggestion: vscode.CompletionItem) => {
				// 	suggestion.range = replaceRange;
				// 	return suggestion;
			    // 	});
				// return new vscode.CompletionList(completionItems,false);
				return new vscode.CompletionList(suggestions,false);
			}
		},
		' ','.',':',';','_','('
	);

	context.subscriptions.push(disposable);
	context.subscriptions.push(provider);
}

// This method is called when your extension is deactivated
export function deactivate() {
	stopServer();
}
