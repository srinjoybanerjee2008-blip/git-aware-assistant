import os
import requests
from typing import List
from rich.console import Console
console = Console()

PROMPT_TEMPLATE = """
You are an AI coding assistant with access to selected source code snippets and optional git metadata.
Answer concisely and cite the source chunks after each factual claim using this format: [path:chunk_id].
If a claim is unsupported by the provided snippets, say "I don't know — missing evidence.".

Question:
{question}

Context snippets:
{snippets}

Answer:
"""

class Llama4Client:
    """Simple HTTP adapter for a Llama 4-like API. Configure LLAMA4_API_URL and LLAMA4_API_KEY in env.
    The implementation below is generic: adjust headers and JSON payload to your provider's spec.
    """
    def __init__(self, api_url: str = None, api_key: str = None, timeout: int = 60):
        self.api_url = api_url or os.getenv('LLAMA4_API_URL')
        self.api_key = api_key or os.getenv('LLAMA4_API_KEY')
        self.timeout = timeout
        if not self.api_url or not self.api_key:
            console.print('[yellow]Warning:[/yellow] LLAMA4_API_URL or LLAMA4_API_KEY not set. LLM calls will fail until configured.')

    def call(self, prompt: str) -> str:
        """Sends a prompt and returns the assistant text. Synchronous implementation.
        Modify this to support streaming if your provider offers SSE/Chunked responses.
        """
        if not self.api_url:
            return 'LLAMA4_API_URL not configured.'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'prompt': prompt,
            'max_tokens': 1024,
            # adjust fields as required by provider
        }
        try:
            r = requests.post(self.api_url, headers=headers, json=payload, timeout=self.timeout)
        except Exception as e:
            return f'LLM request failed: {e}'
        if r.status_code != 200:
            return f'LLM request failed: {r.status_code} {r.text}'
        try:
            data = r.json()
            # Provider-specific: try to find text in common keys
            if 'text' in data:
                return data['text']
            if 'choices' in data and len(data['choices'])>0 and 'text' in data['choices'][0]:
                return data['choices'][0]['text']
            # fallback: return full JSON
            return str(data)
        except Exception as e:
            return f'Failed to parse LLM response: {e} | raw: {r.text}'


def compose_prompt(question: str, results: List[dict]) -> str:
    snippets = []
    for doc, meta, dist in results:
        snippets.append(f"[Source: {meta['path']} | id: {meta['chunk_id']} | dist:{dist}]\n{doc}\n")
    return PROMPT_TEMPLATE.format(question=question, snippets='\n---\n'.join(snippets))
