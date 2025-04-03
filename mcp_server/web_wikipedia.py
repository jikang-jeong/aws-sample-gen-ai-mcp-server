import logging
from typing import Dict, Any
import requests
from dataclasses import dataclass


@dataclass
class WikipediaConfig:
    """Wikipedia API 설정"""
    base_url: str = "https://en.wikipedia.org/w/api.php"
    user_agent: str = "MyWikipediaApp/1.0"


class WikipediaService:
    """Wikipedia 검색 서비스"""

    def __init__(self, config: WikipediaConfig = WikipediaConfig()):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:

        headers = {"User-Agent": self.config.user_agent}
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "format": "json",
            "utf8": "",
            "origin": "*"
        }

        try:
            response = requests.get(
                self.config.base_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()

            data = response.json()
            results = [
                {
                    "title": item["title"],
                    "snippet": item["snippet"],
                    "pageid": item["pageid"],
                    "timestamp": item["timestamp"]
                }
                for item in data.get("query", {}).get("search", [])
            ]

            return {"results": results}

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Wikipedia API 요청 실패: {e}")
            return {"error": f"API 요청 실패: {str(e)}"}
        except KeyError as e:
            self.logger.error(f"Wikipedia API 응답 형식 오류: {e}")
            return {"error": "API 응답 형식 오류"}
