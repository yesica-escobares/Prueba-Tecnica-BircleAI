from typing import Generator


def sse_event_generator(response) -> Generator[str, None, None]:

    for token in response.response_gen:
        yield f"data: {token}\n\n"

    yield "data: [DONE]\n\n"
