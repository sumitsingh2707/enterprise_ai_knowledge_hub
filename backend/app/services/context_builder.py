def build_context(results) -> str:
    context_parts = []

    for document, score in results:
        metadata = document.metadata

        context_parts.append(
            f"""
Source:
Document: {metadata.get("file_name")}
Page: {metadata.get("page")}
Relevance Score: {score}

Content:
{document.page_content}
"""
        )

    return "\n\n".join(context_parts)