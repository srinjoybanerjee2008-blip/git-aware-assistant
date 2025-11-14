import os
from typing import Iterable

TEXT_FILE_EXTS = {'.py','.js','.ts','.java','.go','.c','.cpp','.rs','.md','.txt','.json','.yaml','.yml','.html'}

def is_text_file(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in TEXT_FILE_EXTS

def read_file(path: str, max_bytes: int = 5_000_000) -> str:
    with open(path, 'rb') as f:
        raw = f.read(max_bytes)
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return raw.decode('latin-1')
        except Exception:
            return ''

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> Iterable[str]:
    words = text.split()
    if not words:
        return
    start = 0
    n = len(words)
    while start < n:
        end = min(n, start + chunk_size)
        yield ' '.join(words[start:end])
        start = end - overlap if (end - overlap) > start else end
