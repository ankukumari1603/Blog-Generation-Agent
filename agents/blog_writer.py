from groq import APIError, Groq, NotFoundError

from config.settings import get_settings


def generate_blog(prompt: str) -> str:
    settings = get_settings()
    client = Groq(
        api_key=settings.groq_api_key,
        timeout=90.0,
        max_retries=2,
    )
    try:
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert blog writer. Follow the user's requested "
                        "language and structure. Return only the finished blog in "
                        "Markdown, without an introductory note or code fence."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
    except APIError as error:
        body = error.body
        error_details = body.get("error", body) if isinstance(body, dict) else {}
        error_code = (
            error_details.get("code") if isinstance(error_details, dict) else None
        )
        if isinstance(error, NotFoundError) or error_code == "model_not_found":
            raise APIError(
                f"The configured Groq model '{settings.groq_model}' is unavailable "
                "or your account does not have access. Check GROQ_MODEL and your "
                "Groq model access.",
                error.request,
                body=error.body,
            ) from error
        raise

    content = completion.choices[0].message.content
    return content.strip() if content else ""
