from indexer import Indexer
from embedder import Embedder

def test_index_and_query():
    idx = Indexer(collection_name='test_tmp')
    emb = Embedder()
    texts = ['def foo():\n    return 1', 'class Bar: pass']
    vecs = emb.embed_batch(texts)
    metas = [{'chunk_id':'t1','path':'a.py'},{'chunk_id':'t2','path':'b.py'}]
    idx.upsert(texts, vecs, metas)
    res = idx.retrieve_by_text('what returns 1', emb, n_results=2)
    assert len(res['documents'][0]) >= 1
