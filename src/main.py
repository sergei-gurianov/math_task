from typing import Optional

from cachetools import TTLCache
from fastapi import FastAPI

from src.models import Request, Response
from src.solvers import (
    CommonSolver,
    CylinderSurfaceSquareSolver,
    TopicDispatcher,
    VectorCrossProductSolver,
)

cache = TTLCache(maxsize=1000, ttl=60)


def process_request(request: Request) -> Optional[Response]:
    """
    Function takes request as the argument
    Based on it's topic, request' question will be forwarded to different solvers
    If question repeats within 60 seconds, it's answer will be taken from cache
    :param request: input request that contains question, topic and other metadata
    :return answer of the question in request
    """
    try:
        if request.question in cache:
            return cache[request.question]
        topic = TopicDispatcher().get_topic(request.question)
        print(topic)
        if topic == "Surface area cylinder":
            solver = CylinderSurfaceSquareSolver()
        elif topic == "Vector cross product":
            solver = VectorCrossProductSolver()
        else:
            solver = CommonSolver()
        answer = solver.get_answer(request.question)
        cache[request.question] = answer
        return answer
    except Exception as e:
        return Response()


app = FastAPI()


@app.post("/math_questions")
async def return_answer(request: Request) -> Response:
    """
    FastApi endpoint function
    :param Request with question
    :return Response with answer
    """
    answer = process_request(request)
    return answer
