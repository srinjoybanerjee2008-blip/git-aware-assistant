# Git-Aware AI Coding Assistant

A local, privacy-first assistant that answers questions about your repository using retrieval-augmented generation (RAG).
This repo includes:
- Ingestion pipeline: traverse repository, chunk source files, create embeddings, store in Chroma.
- LLM integration: an adapter for Llama 4 (HTTP/API). Replace endpoint/key with your provider details.
- CLI that retrieves relevant code snippets and asks the LLM.
- Safe `git` helpers to let the agent run restricted git commands (diff, blame, log).
- A VS Code extension scaffold that calls the local CLI and streams results.

> **Security**: Never run this on untrusted repositories with `--allow-git` enabled. See `SECURITY.md` for more.

## Quick start (prototype)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Ingest your repo (example)
python ingest.py --repo . --collection main --chunk-size 800 --overlap 100



# Ask a question
python cli.py "Show the main file where the agent is initialized" --collection git-aware-agent --topk 6

```

## Llama 4 integration

This project contains a `Llama4Client` in `agent.py`. Configure:
- `LLAMA4_API_URL` — HTTP endpoint for your Llama 4 provider.
- `LLAMA4_API_KEY` — API key in env.

The client sends a prompt and expects a JSON response with `text`. Modify `agent.py` to match your provider's API if necessary.

## Files of interest

- `ingest.py` — traverses a repo, chunks files, creates embeddings, and upserts into Chroma.
- `embedder.py` — wrapper for `sentence-transformers` embeddings (code-friendly model).
- `indexer.py` — Chroma wrapper (local DuckDB+Parquet persist).
- `git_tools.py` — safe git wrappers using GitPython + subprocess for blame/diff.
- `agent.py` — prompt templates + Llama 4 client.
- `cli.py` — simple CLI for user queries.
- `vscode-extension/` — scaffold for a VS Code extension that runs the CLI.

## Notes

- This is a prototype intended for local use. It is not production hardened.
- See `SECURITY.md` for recommended sandboxing and usage guidelines.

