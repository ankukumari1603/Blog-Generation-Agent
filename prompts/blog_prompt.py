def build_blog_prompt(topic: str, language: str) -> str:
    return f"""Write a complete, engaging blog post about the topic below.

Write the entire blog in {language}.

Topic: {topic}

Structure the post in Markdown with:
- A catchy, specific title as the main heading.
- An engaging introduction that frames the topic.
- Multiple detailed sections with clear headings.
- Practical, concrete examples that help readers apply the ideas.
- A concise conclusion that reinforces the main takeaways.

Keep the writing accurate, useful, and easy to follow. Do not invent statistics,
quotes, or sources. If a claim is uncertain, qualify it rather than presenting
it as fact."""
