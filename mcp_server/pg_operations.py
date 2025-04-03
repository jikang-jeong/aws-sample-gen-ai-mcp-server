import logging
from typing import Dict, List, Any
from pg_manager import PostgresManager

class DatabaseOperations:
    """데이터베이스 작업을 처리하는 클래스"""

    def __init__(self, postgres_manager: PostgresManager):
        self.postgres_manager = postgres_manager
        self.logger = logging.getLogger(__name__)

    def fetch_table_list(self) -> Dict[str, List[Dict[str, str]]]:
        """public 스키마의 테이블 목록 조회"""
        try:
            with self.postgres_manager.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public';"
                    )
                    tables = [{"tablename": row[0]} for row in cursor.fetchall()]
                    return {"tables": tables}
        except Exception as e:
            self.logger.error(f"테이블 목록 조회 실패: {e}")
            return {"error": str(e)}

    def execute_query(self, sql: str) -> Dict[str, Any]:
        """SQL 쿼리 실행 및 결과 반환"""
        try:
            with self.postgres_manager.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    results = [dict(zip(columns, row)) for row in rows]
                    return {"data": results}
        except Exception as e:
            self.logger.error(f"쿼리 실행 실패: {e}")
            return {"error": str(e)}
