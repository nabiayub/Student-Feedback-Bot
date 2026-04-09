import pandas as pd
from src.database.models import Message

class ExportService:
    @staticmethod
    def _prepare_data(messages: list[Message]) -> list[dict]:
        """
        Helper to convert Message objects into a list of dictionaries for Pandas.
        """
        return [
            {
                'Category': msg.category.title if msg.category else 'N/A',
                'Date': msg.created_at.strftime('%d.%m.%Y %H:%M'),
                'Content': msg.content
            }
            for msg in messages
        ]

    @staticmethod
    def generate_csv(messages: list[Message], file_path: str) -> str:
        """
        Generates a CSV file from a list of messages.
        Using ';' as separator for better compatibility with Excel.
        """
        data = ExportService._prepare_data(messages)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, sep=';', encoding='utf-8-sig')
        return file_path

    @staticmethod
    def generate_excel(messages: list[Message], file_path: str) -> str:
        """
        Generates an Excel (.xlsx) file from a list of messages.
        """
        data = ExportService._prepare_data(messages)
        df = pd.DataFrame(data)
        # Note: requires openpyxl to be installed
        df.to_excel(file_path, index=False, engine='openpyxl')
        return file_path
