def format_history_text(messages):
    history_text = "📜 <b>Ваша история сообщений:</b>\n"

    for msg in messages:
        date_str = msg.created_at.strftime('%d/%m/%Y')
        history_text += (
            '\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n'
            f"<b>{date_str} | {msg.category.title}</b>"
            f"   <blockquote>{msg.content}</blockquote>\n"
        )

    return history_text
