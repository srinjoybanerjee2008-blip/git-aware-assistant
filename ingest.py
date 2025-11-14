import argparse
import os
from pathlib import Path
from tqdm import tqdm
from utils import is_text_file, read_file, chunk_text
from embedder import Embedder
from indexer import Indexer

def traverse_repo(repo_path: str):
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        # skip .git by default
        if '.git' in root.split(os.sep):
            continue
        for fn in filenames:
            p = Path(root) / fn
            if is_text_file(str(p)):
                files.append(p)
    return files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True)
    parser.add_argument('--collection', default='default')
    parser.add_argument('--chunk-size', type=int, default=800)
    parser.add_argument('--overlap', type=int, default=100)
    parser.add_argument('--batch-size', type=int, default=128)
    args = parser.parse_args()

    files = traverse_repo(args.repo)
    print(f'Found {len(files)} text files to ingest.')
    embedder = Embedder()
    indexer = Indexer(collection_name=args.collection)

    docs = []
    for p in tqdm(files, desc='Files'):
        text = read_file(str(p))
        if not text.strip():
            continue
        chunks = list(chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap))
        for i, c in enumerate(chunks):
            meta = {
                'path': str(p.relative_to(args.repo)),
                'abs_path': str(p),
                'chunk_id': f"{p.name}::chunk::{i}",
            }
            docs.append((c, meta))

    # embed in batches
    texts = [d[0] for d in docs]
    metas = [d[1] for d in docs]
    for i in tqdm(range(0, len(texts), args.batch_size), desc='Embedding batches'):
        batch_texts = texts[i:i+args.batch_size]
        batch_metas = metas[i:i+args.batch_size]
        vectors = embedder.embed_batch(batch_texts)
        indexer.upsert(batch_texts, vectors, batch_metas)

    print('Ingest complete.')

if __name__ == '__main__':
    main()
