# Service for solving mathematical problems

This repository contains a FastAPI service that solves the mathematical problems.

Firstly, topic of is extracted from the input text using `TopicDispatcher`.
For some predefined topics custom solvers (`BaseSolver`) parse the questions in natural language using **DeepSeek R1** model:
- for **Cylinder square surface area** service extracts parameters like height and radius
- for **Vector cross product** service extracts directly coordinates of the vectors

The answer then is calculated using Python functions.

If the question is not in predefined topic list, the answer is gathered directly from the respone of LLM model.


## Architecture Overview

1. **FastAPI** controls requests.
2. **Solver classes** handle parsing parameters from the question, calculating and returning the answer.
3. The final answer is JSON-format (`{"answer": ... }`).
4. The service itself runs in isolated **Docker** container.


## Project tree
```
📦 
├─ Dockerfile                   # Instructions for the docker image
├─ README.md                    # Documentation
├─ requirements.txt             # Package dependencies
├─ run.sh                       # Docker container run script
└─ src
   ├─ base.py                   # Base solver class
   ├─ llm.py                    # LLM workaround
   ├─ main.py                   # Main script with request handling and FastAPI app
   ├─ models.py                 # Pydantic schemas
   └─ solvers.py                # Custom solvers
```

## Installation & Setup

1. Clone repository

    ```bash
    git clone https://github.com/sergei-gurianov/math_task.git
    cd math_task
    ```

2. Define the LLM model API key

    ```bash
    export LLM_MODEL_API_KEY="your_api_key"
    ```
  **Explore the model API key [[Link](https://platform.deepseek.com/)]**

Service uses **deepseek-chat** model. If you use another model you can modify it's credentials in `src/llm.py`.

3. Run the service

    ```bash
    sh run.sh
    ```

4. Test some requests

    ```bash
    curl -X 'POST' \
        'http://0.0.0.0:8008/math_questions' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "question": "Чему равен корень из 100",
    }'
    ```
    ```json
    {
      "answer": "10"
    }
    ```

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8008/math_questions' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "question": "What is the surface area of a cylinder with 10 cm height and 60 cm radius?"
    }'
    ```
    ```json
    {
      "answer": "2 m^2"
    }
    ```
  
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8008/math_questions' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "question": "What is the cross product of those vectors: [-9, -19, -14] ⨯ [-18, -16, 11]?"
    }'
    ```
    ```json
    {
      "answer": "[-433.  351. -198.]"
    }
    ```

## Improvements

- **Additional Topics**: Create new solvers for math or geometry tasks.
- **Optimization**: Reduce number of llm requests (dispatcher and parser)
- **Safety**: Implement authentication and authorization mechanisms to control access.
- **Testing**: Create Unit tests for calculation functions.