from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import os
from pathlib import Path
from src.jlptsensei_scraper import JLPTSenseiScraper


class GrammarScraper(JLPTSenseiScraper):
    def __init__(self, level: str) -> None:
        super().__init__(level)

        self.LESSON_TYPE = 'grammar'

        column_names = ['#', 'Grammar', 'Reading', 'Meaning', 'Source']
        self.scraped_df = pd.DataFrame(columns=column_names)


    def scrape(self) -> None:
        page_number = 1

        while True:
            try:
                html = urlopen(f'https://jlptsensei.com/jlpt-{self.jlpt_level}-grammar-list/page/{page_number}')
            except HTTPError as e:
                print(e)
                break
            except URLError as e:
                print(e)
                break
            
            print(f"Scraping {self.jlpt_level.capitalize()} grammar, page {page_number}...", end='\r')

            bs = BeautifulSoup(html, 'lxml')

            try:
                table_element = bs.find('table', {'id': 'jl-grammar'})

                # get table rows
                tr_elements = table_element.tbody.find_all('tr', {'class': 'jl-row'})
                # get table data in rows
                for tr in tr_elements:
                    row_data = []
                    for td_element in tr.find_all('td'):
                        if td_element['class'][0] == 'jl-td-gj':
                            splitted_td = td_element.string.split('（')
                            row_data.append(splitted_td[0])
                            if len(splitted_td) == 2:
                                row_data.append(f'{splitted_td[1].split("）")[0]}')
                            else:
                                row_data.append('')
                        elif td_element['class'][0] == 'jl-td-gr':
                            # skip the romaji readings from grammar table
                            pass
                        else:
                            row_data.append(td_element.string)

                    # append grammar lesson source link for more details
                    row_data.append(tr.find('a', href=True)['href'])

                    # insert row data into dataframe
                    self.scraped_df.loc[len(self.scraped_df)] = row_data
            except AttributeError as e:
                print("No more table pages...", end='\r')
                break

            # increment variable to scrape next table page
            page_number += 1

        self.df_to_csv()
        print(f"Finished scraping {self.jlpt_level.capitalize()} grammar tables.")

        # # get more data from each grammar point link
        for index, df_row in self.scraped_df.iterrows():
            self.scrape_images(df_row)

        print(f"Finished scraping {self.jlpt_level.capitalize()} grammar flashcard images.")


    def scrape_images(self, df_row) -> None:
        """
        Scrape grammar point links to obtain futher data
        """
        try:
            html = urlopen(df_row['Source'])
        except HTTPError as e:
            print(e)
        except URLError as e:
            print(e)

        bs = BeautifulSoup(html, 'lxml')

        try:
            img_element = bs.find('img', {'id': 'header-image'})
        except URLError as e:
            print(f"{e}. No flashcard image found for {df_row['Grammar Lesson']}")
        
        outdir = f'./data/grammar/flashcard_images/{self.jlpt_level}'
        Path(outdir).mkdir(parents=True, exist_ok=True)
        filename = f'flashcard{df_row["#"]}.jpg'
        fullpath = os.path.join(outdir, filename)

        # save flashcard image
        urlretrieve(img_element['src'], fullpath)

        print(f"Saved {df_row['#']}/{len(self.scraped_df.index)} grammar flashcards.", end='\r')
