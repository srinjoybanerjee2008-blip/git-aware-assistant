import argparse
from embedder import Embedder
from indexer import Indexer
from agent import Llama4Client, compose_prompt
from rich import print
from git_tools import GitTools
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--collection', default='default')
    parser.add_argument('--topk', type=int, default=6)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--allow-git', action='store_true', help='Allow the agent to run limited git commands (diff/blame).')
    args = parser.parse_args()

    embedder = Embedder()
    indexer = Indexer(collection_name=args.collection)
    # retrieve
    res = indexer.retrieve_by_text(args.query, embedder, n_results=args.topk)
    docs = res['documents'][0]
    metas = res['metadatas'][0]
    dists = res['distances'][0]
    results = list(zip(docs, metas, dists))

    prompt = compose_prompt(args.query, results)
    client = Llama4Client()

    print('\n--- Prompt sent to LLM (truncated) ---\n')
    print(prompt[:2000])
    print('\n--- Answer ---\n')
    ans = client.call(prompt)
    print(ans)

    # optional: run git helpers if requested
    if args.allow_git:
        gt = GitTools(args.repo)
        print('\n--- Git diff (HEAD~1..HEAD) ---\n')
        print(gt.git_diff('HEAD~1','HEAD'))

if __name__ == '__main__':
    main()
