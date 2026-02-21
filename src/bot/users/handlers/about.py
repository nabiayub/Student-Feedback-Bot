from aiogram import Router, F
from aiogram.types import Message

from src.bot.lexicon import MainMenuButtons
from src.schemas.messages import MessageRead

router = Router()

@router.message(F.text == MainMenuButtons.ABOUT)
async def about_handler(message: Message):
    about_text = (
        "<b>🎓 AUT Feedback Portal</b>\n\n"
        # "────────────────────\n"
        "Welcome to the official <b>AUT</b> bot. This platform is "
        "designed for students and staff to help improve our university.\n\n"

        "<b>What can you do here?</b>\n"
        "• 📝 <b>Feedbacks:</b> General experiences.\n"
        "• ⚠️ <b>Complaints:</b> Report urgent issues.\n"
        "• 💡 <b>Suggestions:</b> Propose new ideas.\n\n"

        "<blockquote expandable>"
        "<b>🔒 Your Privacy Matters</b>\n"
        "For every submission, you choose between <b>Named</b> or <b>Anonymous</b>. "
        "If you choose Anonymous, your identity is fully protected."
        "</blockquote>\n"
        "<i>Your voice shapes our university's future.</i>"
    )

    await message.answer(text=about_text)
