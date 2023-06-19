from qdrant_client import QdrantClient
from qdrant_client.models import PointIdsList
from dotenv import load_dotenv
import os

# 加载 .env 文件中的配置信息
load_dotenv()

qdrant_url = os.getenv('QDRANT_URL', default='localhost')
qdrant_port = os.getenv('QDRANT_PORT', default=6333)
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

client = QdrantClient(host=qdrant_url, port=qdrant_port)


def delete_vector(vector_id):
    result = client.delete(collection_name=COLLECTION_NAME, points_selector=PointIdsList(points=[vector_id]))
    print(result)


if __name__ == '__main__':
    delete_vector("aa0b466f-86b0-4734-9c54-9f77f6fc64e3")
