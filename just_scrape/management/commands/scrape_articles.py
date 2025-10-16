from django.core.management.base import BaseCommand
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
from just_scrape.models import Article
import os


#Słownik z datami
dates = {'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4,
    'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
    'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12,}

urls = ["https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie", 
       "https://galicjaexpress.pl/bmw-e9-30-cs-szczegolowe-informacje-o-osiagach-i-historii-modelu", 
       "https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa", 
       "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow" ]

class Command(BaseCommand):
    help = 'Scrapes articles'

    def parse_date(self, date_str):
        
        # Zamiana polskich nazw miesięcy na liczby
        for month_name, month_number in dates.items():
            if month_name in date_str:
                date_str = date_str.replace(month_name, str(month_number))
                break

        # Obsługa dat (ago)
        if 'ago' in date_str:
            parts = date_str.split()
            value = int(parts[0])
            unit = parts[1]
            
            if 'second' in unit:
                date_str = (datetime.now() - timedelta(seconds=value)).strftime('%d.%m.%Y, %H:%M:%S')
            elif 'minute' in unit:
                date_str = (datetime.now() - timedelta(minutes=value)).strftime('%d.%m.%Y, %H:%M:%S')
            elif 'hour' in unit:
                date_str = (datetime.now() - timedelta(hours=value)).strftime('%d.%m.%Y, %H:%M:%S')
            elif 'day' in unit:
                date_str = (datetime.now() - timedelta(days=value)).strftime('%d.%m.%Y, %H:%M:%S')
            elif 'week' in unit:
                date_str = (datetime.now() - timedelta(weeks=value)).strftime('%d.%m.%Y, %H:%M:%S')
            elif 'month' in unit:
                date_str = (datetime.now() - timedelta(days=30*value)).strftime('%d.%m.%Y, %H:%M:%S')
            elif 'year' in unit:
                date_str = (datetime.now() - timedelta(days=365*value)).strftime('%d.%m.%Y, %H:%M:%S')
        else:
            # Obsługa dat w formacie "5 02 2023" lub 5.02.2023"
            if '.' not in date_str:
                date_str = date_str.replace(' ', '.') + ', 00:00:00'
            elif ',' not in date_str:
                date_str = date_str + ', 00:00:00'
            
        # Parsowanie daty
        date_obj = datetime.strptime(date_str, '%d.%m.%Y, %H:%M:%S')
        print(date_obj)
        return date_obj
        
    def handle(self, *args, **options):
        i = 0
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        with sync_playwright() as playwright:
            browser = playwright.firefox.launch(headless=True)  
            page = browser.new_page()

            for url in urls:
                page.goto(url)
                # Tytuł
                title = page.title()
                # Artykuł z tagami html
                orginal_article = page.inner_html('article')
                # Artykuł bez tagów html
                text_article = page.inner_text('article')
                # Data publikacji
                date_article = page.inner_text('time') if page.locator('time').count() > 0 else page.inner_text('article div p')
                # Parsowanie daty
                date_article = self.parse_date(date_article)
                # Zapis do bazy / Walidacja
                if not Article.objects.filter(url=url).exists():
                    Article.objects.create(
                                title=title,
                                content=text_article,
                                content_html=orginal_article,
                                url=url,
                                published_date=date_article
                            )
                    i+=1
                    self.stdout.write(self.style.SUCCESS(f'Pomyślnie zapisano {i}/{len(urls)}: {title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Artykuł już istnieje: {title}'))
        
            browser.close()
    
    
    