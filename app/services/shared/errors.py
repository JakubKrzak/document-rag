class RagBaseError(Exception):
    def __init__(self, file_name:str=None):
        super().__init__(file_name)
        self.file_name = file_name

class DocumentError(RagBaseError):
    pass

class DataBaseError(RagBaseError):
    pass

class ChunkingError(RagBaseError):
    pass

class EmbeddingError(RagBaseError):
    pass

class DocumentNotFoundError(DocumentError):
    def __init__(self, file_name:str):
        super().__init__(f"Document {file_name} not found")

class PathNotFoundError(DocumentError):
    def __init__(self, path:str):
        super().__init__(f"Path ({path}) not found")

class AddFileToDataBaseError(DataBaseError):
    def __init__(self, file_name:str):
        super().__init__(f"Failed to add info file {file_name} to database")

class ChunksEmptyError(ChunkingError):
    def __init__(self, file_name:str):
        super().__init__(f"Chunks from file {file_name} are empty")

class EmptyVectorsError(EmbeddingError):
    def __init__(self, file_name:str):
        super().__init__(f"Vectors from file {file_name} are empty")

class WrongVectorsDimError(EmbeddingError):
    def __init__(self, file_name:str, current_vector_dim:int, excepted_vector_dim:int):
        super().__init__(f"The dimensions of the vectors from {file_name} are wrong, current_dim={current_vector_dim}, expected_vector_dim={excepted_vector_dim}")

class EmptyPointsError(DataBaseError):
    def __init__(self, file_name:str):
        super().__init__(f"Points from file {file_name} are empty")

class VectrDatabaseError(DataBaseError):
    def __init__(self, file_name):
        super().__init__(f"Failed upsert points from file {file_name} to vector database")