import asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

from mcp import StdioServerParameters
from converse_agent import ConverseAgent
from converse_tools import ConverseToolManager
from mcp_client import MCPClient
from dotenv import load_dotenv

load_dotenv()
class Colors:
    """터미널 출력을 위한 ANSI 색상 코드"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class UIManager:
    """사용자 인터페이스 관리 클래스"""

    @staticmethod
    def clear_screen() -> None:
        """터미널 화면을 지우는 메서드"""
        print('\033[2J\033[H', end='')

    @staticmethod
    def print_welcome() -> None:
        """환영 메시지 출력"""
        UIManager.clear_screen()
        print(f"{Colors.HEADER}{Colors.BOLD}Welcome to AI Assistant!{Colors.END}")
        print(f"{Colors.CYAN}I'm here to help you with any questions or tasks.{Colors.END}")
        print(f"{Colors.CYAN}Type 'quit' to exit.{Colors.END}\n")

    @staticmethod
    def print_tools(tools: List[Dict[str, Any]]) -> None:
        """사용 가능한 도구들을 출력
        Args:
            tools: 도구 정보가 담긴 dictionary list
        """
        print(f"{Colors.CYAN}사용 가능 Tools:{Colors.END}")
        for tool in tools:
            print(f"  • {Colors.GREEN}{tool['name']}{Colors.END}: {tool['description']}")
        print()

    @staticmethod
    def format_message(role: str, content: str) -> str:
        """메시지 형식화
        Args:
            role: 메시지 작성자 역할 ('user' 또는 'assistant')
            content: 메시지 내용
        Returns:
            형식화된 메시지 문자열
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        if role == "user":
            return f"{Colors.BLUE}[{timestamp}] You: {Colors.END}{content}"
        return f"{Colors.GREEN}Assistant: {Colors.END}{content}"


class AIAssistant:
    """AI 어시스턴트 메인 클래스"""

    def __init__(self, model_id: str):
        """
        Args:
            model_id: 사용할 AI 모델 ID
        """
        self.model_id = model_id
        self.agent = ConverseAgent(model_id)
        self.agent.tools = ConverseToolManager()
        self.ui = UIManager()

    async def handle_resource_update(self, uri: str) -> None:
        """리소스 업데이트 처리

        Args:
            uri: 업데이트된 리소스의 URI
        """
        print(f"{Colors.YELLOW}Resource updated: {uri}{Colors.END}")

    async def setup_mcp_client(self) -> None:
        """MCP 클라이언트 설정 및 도구 등록"""

        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server/mcp_server.py"],
            env=None
        )

        async with MCPClient(server_params) as mcp_client:
            mcp_client.on_resource_update(self.handle_resource_update)
            tools = await mcp_client.get_available_tools()

            # 에이전트에 도구 등록
            for tool in tools:
                self.agent.tools.register_tool(
                    name=tool['name'],
                    func=mcp_client.call_tool,
                    description=tool['description'],
                    input_schema={'json': tool['inputSchema']}
                )

            await self.run_interactive_loop(tools)

    async def run_interactive_loop(self, tools: List[Dict[str, Any]]) -> None:
        """대화형 프롬프트 루프 실행
        Args:
            tools: 사용 가능한 도구 목록
        """
        self.ui.print_welcome()
        self.ui.print_tools(tools)

        while True:
            try:
                user_prompt = input(f"\n{Colors.BOLD}User: {Colors.END}")
                if user_prompt.lower() in ['quit', 'exit', 'q']:
                    print(f"\n{Colors.CYAN}Goodbye! Thanks for chatting!{Colors.END}")
                    break

                if not user_prompt.strip():
                    continue

                print(f"\n{Colors.YELLOW}Thinking...{Colors.END}")
                response = await self.agent.invoke_with_prompt(user_prompt)
                print(f"\n{self.ui.format_message('assistant', response)}")

            except KeyboardInterrupt:
                print(f"\n{Colors.CYAN}Goodbye! Thanks for chatting!{Colors.END}")
                break
            except Exception as e:
                print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")


async def main():
    try:
        model_id = os.getenv('LLM_MODEL')
        assistant = AIAssistant(model_id)
        await assistant.setup_mcp_client()
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {str(e)}{Colors.END}")