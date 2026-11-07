import streamlit as st
from groq import APIError

from config.settings import SettingsError
from graph.workflow import blog_workflow


st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 750px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .main h1 {
        text-align: center;
    }

    .blog-subtitle {
        color: #a7b0be;
        font-size: 1.05rem;
        margin: -0.5rem 0 1.5rem;
        text-align: center;
    }

    .stMarkdown h1 {
        font-size: 2.25rem;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    .stMarkdown h2 {
        font-size: 1.65rem;
        line-height: 1.3;
        margin-top: 2rem;
    }

    .stMarkdown h3 {
        font-size: 1.3rem;
        line-height: 1.35;
    }

    .stMarkdown p,
    .stMarkdown li {
        font-size: 1.05rem;
        line-height: 1.7;
    }

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #ff4949;
        border: 1px solid #ff4949;
        color: #ffffff;
        font-weight: 600;
        min-height: 2.8rem;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #e63e3e;
        border-color: #e63e3e;
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✍️ AI Blog Generator")
st.markdown(
    '<p class="blog-subtitle">Generate blogs on any topic using Agentic AI.</p>',
    unsafe_allow_html=True,
)
st.divider()

languages = [
    "English",
    "Spanish",
    "French",
    "German",
    "Hindi",
    "Italian",
    "Japanese",
    "Portuguese",
]

with st.form("blog_generator"):
    topic = st.text_input("Enter your blog topic")
    language = st.selectbox("Select blog language", languages)
    submitted = st.form_submit_button(
        "Generate Blog",
        type="primary",
        width="stretch",
    )

if submitted:
    st.session_state.pop("generated_blog", None)
    if not topic.strip():
        st.error("Enter a topic before generating a blog.")
    else:
        try:
            with st.spinner("Writing your blog..."):
                result = blog_workflow.invoke(
                    {"topic": topic.strip(), "language": language}
                )

            if result.get("error"):
                st.error(result["error"])
            elif result.get("blog"):
                st.session_state["generated_blog"] = result["blog"]
            else:
                st.error("The blog workflow returned no content.")
        except (APIError, SettingsError) as error:
            st.error(f"Unable to generate the blog: {error}")

generated_blog = st.session_state.get("generated_blog")
if generated_blog:
    st.success("Blog generated successfully!")
    st.markdown(generated_blog)
    st.download_button(
        "Download blog",
        data=generated_blog,
        file_name="generated-blog.md",
        mime="text/markdown",
        width="stretch",
    )
