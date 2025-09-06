from typing import Dict, Any, List
from ..agents_prompts.rag_prompt import RAG_PROMPT
from ..utils.embedder import Embedder
from ..utils.chroma_client import ChromaClient
import yaml

class RAGAgent:
    """Handles document retrieval and context augmentation"""

    def __init__(self):
        self.prompt = RAG_PROMPT
        self.config = self._load_config()
        self.embedder = Embedder(self.config.get("embedding", {}).get("model_name", ""))
        self.chroma = ChromaClient(
            persist_directory=self.config.get("retrieval", {}).get("persist_directory", "db/chroma"),
            collection_name=self.config.get("retrieval", {}).get("chroma_collection", "org_docs_v1")
        )

    def _load_config(self):
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return {}

    async def retrieve(self, query: str, top_k: int = None) -> Dict[str, Any]:
        if top_k is None:
            top_k = self.config.get("retrieval", {}).get("top_k", 5)

        query_embedding = self.embedder.embed_text(query)
        # defensive handling
        if hasattr(query_embedding, "__len__") and len(query_embedding) > 0:
            query_vec = query_embedding[0].tolist() if hasattr(query_embedding[0], "tolist") else list(query_embedding[0])
        else:
            query_vec = []

        results = self.chroma.search(query_vec, top_k=top_k)

        threshold = self.config.get("retrieval", {}).get("score_threshold", 0.3)
        filtered_docs = [
            doc for doc, dist in zip(results.get("documents", []), results.get("distances", []))
            if dist <= threshold
        ]

        return {
            "documents": filtered_docs,
            "count": len(filtered_docs),
            "query": query
        }

    def rerank_documents(self, documents: List[str], query: str) -> List[str]:
        return documents
