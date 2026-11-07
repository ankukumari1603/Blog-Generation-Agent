from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agents.blog_writer import generate_blog
from prompts.blog_prompt import build_blog_prompt


class BlogState(TypedDict, total=False):
    topic: str
    language: str
    prompt: str
    blog: str
    error: str


def _prepare_request(state: BlogState) -> BlogState:
    topic = state.get("topic", "").strip()
    language = state.get("language", "").strip()
    if not topic:
        return {"error": "Enter a topic before generating a blog."}
    if not language:
        return {"error": "Select a language before generating a blog."}

    return {
        "prompt": build_blog_prompt(topic=topic, language=language),
    }


def _route_after_prepare(state: BlogState) -> str:
    return "finish" if state.get("error") else "generate"


def _generate(state: BlogState) -> BlogState:
    prompt = state.get("prompt")
    if not prompt:
        return {"error": "The blog request could not be prepared."}
    return {"blog": generate_blog(prompt)}


def _validate_result(state: BlogState) -> BlogState:
    blog = state.get("blog", "").strip()
    if not blog:
        return {"error": "The model returned an empty blog. Please try again."}
    return {"blog": blog}


builder = StateGraph(BlogState)
builder.add_node("prepare_request", _prepare_request)
builder.add_node("generate", _generate)
builder.add_node("validate_result", _validate_result)
builder.add_edge(START, "prepare_request")
builder.add_conditional_edges(
    "prepare_request",
    _route_after_prepare,
    {
        "generate": "generate",
        "finish": END,
    },
)
builder.add_edge("generate", "validate_result")
builder.add_edge("validate_result", END)

blog_workflow = builder.compile()
