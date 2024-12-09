import * as vscode from 'vscode';

interface AIResponse {
    suggestions: string[];
}

export async function getVHDLCompletion(inputText: string): Promise<vscode.CompletionItem[]> {
    try {
        const response = await fetch('https://7756-34-125-148-182.ngrok-free.app/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input: inputText}),
        });
        if (!response.ok) {
            const servererror = 'Server error:' + response.statusText;
            throw new Error(servererror);
        }
        const data = await response.json() as AIResponse;
        const suggestions = data.suggestions || [];
        return suggestions.map((suggestion: string) => {
            return new vscode.CompletionItem(
                suggestion,
                vscode.CompletionItemKind.Text
            );
        });
    } catch (error) {
        console.error("Language Model Service Error:", error);
        return [];
    }
}
