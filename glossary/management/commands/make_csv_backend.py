import csv
from glossary.models import Term

with open('glossary.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        term = Term(
            term=row['Term'],
            definition=row['Definition'],
            url=row.get('URL', ''),
        )
        term.save()
