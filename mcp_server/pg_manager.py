import logging
from typing import Optional
from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from pg_configuration import DatabaseConfig

class PostgresManager:
    """PostgreSQL 연결 풀 관리 클래스"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.pool: Optional[ConnectionPool] = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> None:
        """PostgreSQL 연결 풀 초기화"""
        if self.pool is None:
            try:
                self.pool = ConnectionPool(
                    conninfo=(
                        f"host={self.config.host} "
                        f"dbname={self.config.database} "
                        f"user={self.config.user} "
                        f"port={self.config.port} "
                        f"password={self.config.password}"
                    ),
                    min_size=1,
                    max_size=10
                )
                self.logger.info("PostgreSQL 연결 풀이 생성되었습니다")
            except Exception as e:
                self.logger.error(f"연결 풀 초기화 실패: {e}")
                raise

    @contextmanager
    def get_db_connection(self):
        """데이터베이스 연결을 관리하는 컨텍스트 매니저"""
        conn = None
        try:
            conn = self.get_connection()
            yield conn
            conn.commit()
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.release_connection(conn)

    def get_connection(self):
        if self.pool is None:
            self.connect()
        return self.pool.getconn()

    def release_connection(self, conn) -> None:
        if self.pool:
            self.pool.putconn(conn)
