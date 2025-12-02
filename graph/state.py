import operator
from typing import List, TypedDict, Annotated


class GraphState(TypedDict):
    """
    Represents the state of our graph

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    # question: str
    question: Annotated[str, lambda x, y: y]
    generation: str
    web_search: bool
    # documents: List[str]
    documents: Annotated[List[str], operator.add]
