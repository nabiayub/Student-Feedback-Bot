from src.schemas.messages import MessageRead


def format_history_text(messages: list[MessageRead], page: int, limit: int) -> str:
    """
    Formats the history text for display
    :return:
    """
    if not messages:
        return 'Your history is empty.'

    history_text = "📜 <b>Ваша история сообщений:</b>\n"
    feedback_count = ((page - 1) * limit) + 1

    for msg in messages:
        date_str = msg.created_at.strftime('%d-%m-%Y')
        history_text += (
            '\n'
            f'<b>💬 Feedback #{feedback_count}</b>\n'
            f"{date_str} | {msg.category.title}\n"
            f"<i>{msg.content}</i>\n"
        )
        feedback_count += 1

    return history_text
