from qdrant_client import QdrantClient


client = QdrantClient(host="localhost", port=6333)


def delete_vector(vector_id):
    client.delete_vectors("")
    return None