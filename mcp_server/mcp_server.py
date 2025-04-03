import logging
import os
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pg_configuration import DatabaseConfig
from pg_manager import PostgresManager
from pg_operations import DatabaseOperations
from tool_registry import ToolRegistry


@staticmethod
def initialize_logging(
        log_file: str = 'mcp_server.log',
        log_level: int = logging.INFO
) -> logging.Logger:
    """로깅 초기화 및 설정"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stderr)
        ]
    )
    return logging.getLogger(__name__)


def initialize_server() -> tuple[FastMCP, DatabaseOperations]:
    """서버 및 데이터베이스 초기화"""
    load_dotenv()
    initialize_logging()

    db_config = DatabaseConfig(
        host=os.getenv('PG_HOST', ''),
        database=os.getenv('PG_DATABASE', ''),
        user=os.getenv('PG_USER', ''),
        password=os.getenv('PG_PASSWORD', ''),
        port=os.getenv('PG_PORT', '5432')
    )

    postgres_manager = PostgresManager(db_config)
    db_ops = DatabaseOperations(postgres_manager)
    mcp = FastMCP("MCP Demo Server")

    return mcp, db_ops


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.info("MCP 데모 서버 시작 중...")

    try:
        mcp, db_ops = initialize_server()

        # 도구 등록
        tool_registry = ToolRegistry(mcp, db_ops)
        tool_registry.register_all()

        mcp.run()
    except Exception as e:
        logger.error(f"서버 오류: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
