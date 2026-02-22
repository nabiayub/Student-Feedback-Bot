from src.schemas.messages import MessageRead


def format_history_text(messages: list[MessageRead], page: int, limit: int) -> str:
    """
    Formats the history text for display
    :return:
    """
    if not messages:
        return '<b>History Empty</b> ✍️ Start by sending some feedback!'

    history_text = "📜 <b>Your messages history:</b>\n"
    feedback_count = ((page - 1) * limit) + 1

    for msg in messages:
        date_str = msg.created_at.strftime('%d-%m-%Y')
        history_text += (
            '\n'
            f'<b>💬 Feedback #{feedback_count}</b>\n'
            f"{date_str} | {msg.category.title}\n"
            f"<blockquote expandable><i>{msg.content}</i></blockquote>\n"
        )
        feedback_count += 1

    return history_text
