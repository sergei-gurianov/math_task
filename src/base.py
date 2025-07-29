from abc import ABC, abstractmethod
from typing import Any, Optional

from src.models import Response


class BaseSolver(ABC):
    """
    Base solver class with must parse and solve methods
    """

    @abstractmethod
    def _parse(question: str) -> Optional[Any]:
        """
        Method for custom question parsing
        """
        pass

    @staticmethod
    @abstractmethod
    def _solve(input_data: Any) -> str:
        """
        Method performs custom calculations
        """
        pass

    def get_answer(self, question: str) -> Optional[Response]:
        """
        Method retrieves input data and makes further calculations
        :param question: input text data
        :return answer with Response format
        """
        input_data = self._parse(question)
        if not input_data:
            return None
        answer = {"answer": self._solve(input_data)}
        return Response(**answer)
