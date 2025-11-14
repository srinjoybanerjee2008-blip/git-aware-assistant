from utils import chunk_text

def test_chunks():
    t = ' '.join(str(i) for i in range(2000))
    chunks = list(chunk_text(t, chunk_size=100, overlap=10))
    assert len(chunks) > 0
