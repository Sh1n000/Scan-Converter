# core/shotgrid_link.py

from shotgun_api3 import Shotgun
from typing import Any, Dict, List, Optional, Union


class ShotGridLink:
    """Wrapper around the Shotgun API for basic CRUD operations."""

    def __init__(
        self,
        server_url: str,
        script_name: str,
        api_key: str,
        retry_count: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Args:
            server_url: ShotGrid 서버 URL
            script_name: 스크립트 로그인 이름
            api_key: 스크립트 API 키
            retry_count: 요청 실패 시 재시도 횟수
            retry_delay: 재시도 간 대기 시간(초)
        """
        self.sg = Shotgun(server_url, script_name, api_key)
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def find(
        self,
        entity_type: str,
        filters: List,
        fields: List[str],
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """엔티티 검색"""
        return self.sg.find(entity_type, filters, fields, limit=limit)

    def create(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """엔티티 생성"""
        return self.sg.create(entity_type, data)

    def update(
        self, entity_type: str, entity_id: int, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """엔티티 업데이트"""
        return self.sg.update(entity_type, entity_id, data)

    def delete(self, entity_type: str, entity_id: int) -> None:
        """엔티티 삭제"""
        self.sg.delete(entity_type, entity_id)

    # 필요하다면 batch, headline 등 추가 메서드 구현
