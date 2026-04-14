
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse

documents = SimpleDirectoryReader("/home/kuba/Desktop/rag/llama_index_disc").load_data()

print(len(documents))