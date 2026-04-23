from FlagEmbedding import BGEM3FlagModel
_model = None

def get_model():
    global _model
    if _model is None:
        _model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)
    return _model

def check_vectors_dim(points: list[dict]):
    vector = points[0]["vector"]
    return len(vector)