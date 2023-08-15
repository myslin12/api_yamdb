from pathlib import Path

from django.core.management.base import BaseCommand

import pandas as pd
from sqlalchemy import create_engine


class Command(BaseCommand):
    help = 'Upload CSV files to corresponding database tables'

    def handle(self, *args, **options):
        engine = create_engine('sqlite:///db.sqlite3')

        base_path = Path(__file__).resolve().parent.parent.parent.parent / 'static' / 'data'

        filename_to_table = {
            'category.csv': 'reviews_category',
            'comments.csv': 'reviews_comment',
            'genre_title.csv': 'reviews_title_genre',
            'genre.csv': 'reviews_genre',
            'review.csv': 'reviews_review',
            'titles.csv': 'reviews_title',
            'users.csv': 'reviews_user',
        }

        for key, value in filename_to_table.items():
            csv_file = base_path / key
            self.stdout.write(self.style.SUCCESS(f"Добавляю {csv_file}"))

            df = pd.read_csv(csv_file)
            df = df.drop_duplicates()
            df = df.dropna()

            df.to_sql(value, if_exists='append', con=engine, index=False)

            self.stdout.write(self.style.SUCCESS(f"Добавлено {len(df)} строк в таблицу '{value}'"))

        self.stdout.write(self.style.SUCCESS("Загрузка окончена"))
