import math
from typing import Optional

import numpy as np

from src.base import BaseSolver
from src.llm import get_llm_answer
from src.models import ParsedCylinder, ParsedVectors, Response, Topic


class CylinderSurfaceSquareSolver(BaseSolver):
    """
    Class for handling the cylinder surface area problems
    """

    system_prompt = """
        You are an AI that extracts entities from questions. 
        You are given a cylinder surface area square problem.
        You have to extract cylinder's height and radius as float numbers in meters.
        Your output must be json format like this:
        {'height': ..., 'radius': ...}
    """

    def _parse(self, question: str) -> Optional[dict[str, float]]:
        """
        Method gets height and radius parameters using llm system prompt and question
        :param question: question that contains cylinder parameters
        :return dict with parameters
        """
        llm_output = get_llm_answer(question, self.system_prompt)
        if not llm_output:
            return None
        return ParsedCylinder.parse_raw(llm_output).model_dump()

    @staticmethod
    def _solve(input_data: dict[str, float]) -> str:
        """
        Method calculates surface square of the cylinder
        Formula: 2 * pi * radius * (height + radius)
        :param input_data: dict with keys - height: parsed height of cylinder, radius: parsed radius of cylinder
        :return surface are square of cylinder
        """
        height, radius = input_data.get("height"), input_data.get("radius")
        if not height or not radius:
            return None
        square = int(2 * math.pi * radius * (height + radius))
        return f"{square} m^2"


class VectorCrossProductSolver(BaseSolver):
    """
    Class for handling the vector cross product problems
    """

    system_prompt = """
        You are an AI that extracts entities from questions. 
        You are given a problem about vector cross product.
        You have to extract vectors as list of floats.
        Your output must be json format like this:
        {"vec1": ..., "vec2": ...}
    """

    def _parse(self, question: str) -> Optional[tuple[int]]:
        """
        Method gets vectors using llm system prompt and question
        :param question: question that contains info about vectors
        :return dict with vectors' coordinates
        """
        llm_output = get_llm_answer(question, self.system_prompt)
        if not llm_output:
            return None
        return ParsedVectors.parse_raw(llm_output).model_dump()

    @staticmethod
    def _solve(input_data: dict[str, list[float]]) -> str:
        """
        Method calculates cross product of two vectors
        :param dict with vectors
        :return cross product of two vectors
        """
        vec1, vec2 = input_data.get("vec1"), input_data.get("vec2")
        return str(np.cross(vec1, vec2))


class CommonSolver:

    system_prompt = """
        You are an AI that solves mathematical tasks given by users. 
        You have to understand what you are asked for and give certain answer as string.
        Your output must be json format like this:
        Example:
        {"answer": "..."}
    """

    def get_answer(self, question: str) -> Optional[Response]:
        """
        Method generates llm answer for the question
        :param question: any input question
        :return llm aswer for the user question
        """
        llm_output = get_llm_answer(question, self.system_prompt)
        answer = Response.parse_raw(llm_output)
        if not answer:
            return None
        return answer


class TopicDispatcher:

    system_prompt = """
        You are an AI that extracts topic from the input text. 
        If the text is about a cylinder surface area, return:
        topic: "Surface area cylinder" 
        If the text is about a vector cross product, return:
        topic: "Vector cross product" 
        If the text if about another topic, return:
        topic: ""
        Your output must be json format like this:
        Example:
        {"topic": "..."}
    """

    def get_topic(self, question):
        """
        Method generates llm answer for the question
        :param question: any input question
        :return llm aswer for the user question
        """
        llm_output = get_llm_answer(question, self.system_prompt)
        topic = Topic.parse_raw(llm_output).model_dump()
        if not topic:
            return None
        return topic.get("topic")
