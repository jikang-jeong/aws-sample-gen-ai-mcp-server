from typing import Dict, List, Any
from mcp.server.fastmcp import FastMCP
from pg_operations import DatabaseOperations
from web_wikipedia import WikipediaService

class ToolRegistry:
    """MCP 도구 등록 관리"""

    def __init__(self, mcp: FastMCP, db_ops: DatabaseOperations):
        self.mcp = mcp
        self.db_ops = db_ops
        self.wiki_service = WikipediaService()

    def register_all(self) -> None:
        """모든 도구 등록"""
        self.register_database_tools()
        self.register_wikipedia_tools()

    def register_database_tools(self) -> None:
        """데이터베이스 관련 도구 등록"""
        @self.mcp.tool()
        def fetch_tableList() -> Dict[str, List[Dict[str, str]]]:
            """public 스키마 테이블 목록 조회"""
            return self.db_ops.fetch_table_list()

        @self.mcp.tool()
        def execute_query(sql: str) -> Dict[str, Any]:
            """SQL 쿼리 실행"""
            return self.db_ops.execute_query(sql)

    def register_wikipedia_tools(self) -> None:
        """Wikipedia 관련 도구 등록"""
        @self.mcp.tool()
        def search_wikipedia(query: str, limit: int = 10) -> dict:
            """Wikipedia 검색 결과 조회"""
            return self.wiki_service.search(query, limit)
