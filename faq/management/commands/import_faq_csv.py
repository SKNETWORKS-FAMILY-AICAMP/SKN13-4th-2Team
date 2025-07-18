import csv
from django.core.management.base import BaseCommand
from faq.models import FAQ

class Command(BaseCommand):
    help = 'CSV 파일에서 FAQ 데이터를 불러옵니다.'

    def handle(self, *args, **kwargs):
        count = 0
        with open('faq.csv', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = row['Question'].strip()
                answer = row['Answer'].strip()

                FAQ.objects.create(question=question, answer=answer)
                count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ 총 {count}개의 FAQ가 성공적으로 저장되었습니다.'))