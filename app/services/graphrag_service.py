import os
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import tiktoken

from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.query.indexer_adapters import (
    read_indexer_entities,
    read_indexer_communities,
    read_indexer_reports,
    read_indexer_text_units,
    read_indexer_relationships,
)
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.base import SearchResult
from graphrag.query.structured_search.drift_search.drift_context import DRIFTSearchContextBuilder
from graphrag.query.structured_search.drift_search.search import DRIFTSearch
from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext
from graphrag.query.structured_search.global_search.search import GlobalSearch, GlobalSearchResult
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.vector_stores.lancedb import LanceDBVectorStore
from dotenv import load_dotenv

class GraphRAGService:
    def __init__(self):
        # 加载环境变量
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../docs/mcp_rag_agent_graphrag_demo/.env'))
        
        # 配置常量
        self.ENTITY_NODES_TABLE = 'create_final_nodes'
        self.ENTITY_EMBEDDING_TABLE = 'create_final_entities'
        self.COMMUNITIES_TABLE = 'create_final_communities'
        self.COMMUNITY_REPORT_TABLE = 'create_final_community_reports'
        self.TEXT_UNIT_TABLE = 'create_final_text_units'
        self.RELATIONSHIP_TABLE = 'create_final_relationships'
        self.COMMUNITY_LEVEL = 2
        
        # API配置
        self.api_type = OpenaiApiType.OpenAI
        self.api_key = os.getenv('API_KEY')
        self.api_base = os.getenv('BASE_URL')
        self.llm_model = os.getenv('MODEL')
        self.embedding_model = 'text-embedding-v2'
        self.llm_temperature = 0.0
        self.json_mode = False
        
        # 数据目录和LanceDB URI
        self.DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../docs/mcp_rag_agent_graphrag_demo/doupocangqiong/output')
        self.LANCEDB_URI = f'{self.DATA_DIR}/lancedb'
        
        # 初始化LLM、嵌入模型和token编码器
        self.llm = self._init_llm()
        self.text_embedder = self._init_embedder()
        self.token_encoder = tiktoken.get_encoding('cl100k_base')
        
        # 上下文和LLM参数
        self.local_context_params = {
            'text_unit_prop': 0.5,
            'community_prop': 0.1,
            'conversation_history_max_turns': 5,
            'conversation_history_user_turns_only': True,
            'top_k_mapped_entities': 10,
            'top_k_relationships': 10,
            'include_entity_rank': True,
            'include_relationship_weight': True,
            'include_community_rank': False,
            'return_candidate_context': False,
            'embedding_vectorstore_key': EntityVectorStoreKey.ID,
            'max_tokens': 12_000
        }
        
        self.global_context_params = {
            'use_community_summary': False,
            'shuffle_data': True,
            'include_community_rank': True,
            'min_community_rank': 0,
            'community_rank_name': 'rank',
            'include_community_weight': True,
            'community_weight_name': 'occurrence weight',
            'normalize_community_weight': True,
            'max_tokens': 12_000,
            'context_name': 'Reports'
        }
        
        self.llm_params = {
            'max_tokens': 2_000,
            'temperature': self.llm_temperature
        }
        
        self.map_llm_params = {
            'max_tokens': 1000,
            'temperature': self.llm_temperature,
            'response_format': {'type': 'json_object'}
        }
        
        self.reduce_llm_params = {
            'max_tokens': 2000,
            'temperature': self.llm_temperature
        }
    
    def _init_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            api_key=self.api_key,
            api_type=self.api_type,
            api_base=self.api_base,
            api_version='2024-02-15-preview',
            model=self.llm_model,
            max_retries=20
        )
    
    def _init_embedder(self) -> OpenAIEmbedding:
        return OpenAIEmbedding(
            api_key=self.api_key,
            api_type=self.api_type,
            api_base=self.api_base,
            api_version='2024-02-15-preview',
            model=self.embedding_model,
            deployment_name=self.embedding_model,
            max_retries=20
        )
    
    def build_local_context_builder(self) -> LocalSearchMixedContext:
        entity_df = pd.read_parquet(f'{self.DATA_DIR}/{self.ENTITY_NODES_TABLE}.parquet')
        entity_embedding_df = pd.read_parquet(f'{self.DATA_DIR}/{self.ENTITY_EMBEDDING_TABLE}.parquet')
        
        entities = read_indexer_entities(entity_df, entity_embedding_df, self.COMMUNITY_LEVEL)
        
        description_embedding_store = LanceDBVectorStore(
            collection_name='default-entity-description',
        )
        description_embedding_store.connect(db_uri=self.LANCEDB_URI)
        
        relationship_df = pd.read_parquet(f'{self.DATA_DIR}/{self.RELATIONSHIP_TABLE}.parquet')
        relationships = read_indexer_relationships(relationship_df)
        
        report_df = pd.read_parquet(f'{self.DATA_DIR}/{self.COMMUNITY_REPORT_TABLE}.parquet')
        reports = read_indexer_reports(report_df, entity_df, self.COMMUNITY_LEVEL)
        
        text_unit_df = pd.read_parquet(f'{self.DATA_DIR}/{self.TEXT_UNIT_TABLE}.parquet')
        text_units = read_indexer_text_units(text_unit_df)
        
        context_builder = LocalSearchMixedContext(
            community_reports=reports,
            text_units=text_units,
            entities=entities,
            relationships=relationships,
            entity_text_embeddings=description_embedding_store,
            embedding_vectorstore_key=EntityVectorStoreKey.ID,
            text_embedder=self.text_embedder,
            token_encoder=self.token_encoder
        )
        
        return context_builder
    
    def build_local_search_engine(self) -> LocalSearch:
        return LocalSearch(
            llm=self.llm,
            context_builder=self.build_local_context_builder(),
            token_encoder=self.token_encoder,
            llm_params=self.llm_params,
            context_builder_params=self.local_context_params,
            response_type='multiple paragraphs'
        )
    
    def build_global_search_engine(self) -> GlobalSearch:
        community_df = pd.read_parquet(f'{self.DATA_DIR}/{self.COMMUNITIES_TABLE}.parquet')
        entity_df = pd.read_parquet(f'{self.DATA_DIR}/{self.ENTITY_NODES_TABLE}.parquet')
        report_df = pd.read_parquet(f'{self.DATA_DIR}/{self.COMMUNITY_REPORT_TABLE}.parquet')
        entity_embedding_df = pd.read_parquet(f'{self.DATA_DIR}/{self.ENTITY_EMBEDDING_TABLE}.parquet')
        
        communities = read_indexer_communities(community_df, entity_df, report_df)
        reports = read_indexer_reports(report_df, entity_df, self.COMMUNITY_LEVEL)
        entities = read_indexer_entities(entity_df, entity_embedding_df, self.COMMUNITY_LEVEL)
        
        context_builder = GlobalCommunityContext(
            community_reports=reports,
            communities=communities,
            entities=entities,
            token_encoder=self.token_encoder
        )
        
        return GlobalSearch(
            llm=self.llm,
            context_builder=context_builder,
            token_encoder=self.token_encoder,
            max_data_tokens=12_000,
            map_llm_params=self.map_llm_params,
            reduce_llm_params=self.reduce_llm_params,
            allow_general_knowledge=False,
            json_mode=self.json_mode,
            context_builder_params=self.global_context_params,
            concurrent_coroutines=32,
            response_type='multiple paragraphs'
        )
    
    def embed_community_reports(self):
        input_path = Path(self.DATA_DIR) / f'{self.COMMUNITY_REPORT_TABLE}.parquet'
        output_path = Path(self.DATA_DIR) / f'{self.COMMUNITY_REPORT_TABLE}_with_embeddings.parquet'
        
        if not Path(output_path).exists():
            report_df = pd.read_parquet(input_path)
            
            if 'full_content' not in report_df.columns:
                raise ValueError(f"'full_content' column not found in {input_path}")
            
            report_df['full_content_embeddings'] = report_df.loc[:, 'full_content'].apply(
                lambda x: self.text_embedder.embed(x)
            )
            
            report_df.to_parquet(output_path)
            return report_df
        return pd.read_parquet(output_path)
    
    def build_drift_search_engine(self) -> DRIFTSearch:
        entity_df = pd.read_parquet(f'{self.DATA_DIR}/{self.ENTITY_NODES_TABLE}.parquet')
        entity_embedding_df = pd.read_parquet(f'{self.DATA_DIR}/{self.ENTITY_EMBEDDING_TABLE}.parquet')
        
        entities = read_indexer_entities(entity_df, entity_embedding_df, self.COMMUNITY_LEVEL)
        
        description_embedding_store = LanceDBVectorStore(
            collection_name='default-entity-description',
        )
        description_embedding_store.connect(db_uri=self.LANCEDB_URI)
        
        relationship_df = pd.read_parquet(f'{self.DATA_DIR}/{self.RELATIONSHIP_TABLE}.parquet')
        relationships = read_indexer_relationships(relationship_df)
        
        text_unit_df = pd.read_parquet(f'{self.DATA_DIR}/{self.TEXT_UNIT_TABLE}.parquet')
        text_units = read_indexer_text_units(text_unit_df)
        
        report_df = self.embed_community_reports()
        reports = read_indexer_reports(
            report_df,
            entity_df,
            self.COMMUNITY_LEVEL,
            content_embedding_col='full_content_embeddings'
        )
        
        context_builder = DRIFTSearchContextBuilder(
            chat_llm=self.llm,
            text_embedder=self.text_embedder,
            entities=entities,
            relationships=relationships,
            reports=reports,
            entity_text_embeddings=description_embedding_store,
            text_units=text_units
        )
        
        return DRIFTSearch(
            llm=self.llm,
            context_builder=context_builder,
            token_encoder=self.token_encoder
        )
    
    async def local_asearch(self, query: str) -> SearchResult:
        search_engine = self.build_local_search_engine()
        return await search_engine.asearch(query)
    
    async def global_asearch(self, query: str) -> GlobalSearchResult:
        search_engine = self.build_global_search_engine()
        return await search_engine.asearch(query)
    
    async def drift_asearch(self, query: str) -> SearchResult:
        search_engine = self.build_drift_search_engine()
        return await search_engine.asearch(query)
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "local_search",
                "description": "为斗破苍穹小说提供相关的知识补充",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询字符串"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "global_search",
                "description": "全局搜索斗破苍穹小说的主题和核心内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询字符串"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "drift_search",
                "description": "基于上下文的动态搜索",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询字符串"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
