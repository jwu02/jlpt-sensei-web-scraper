# JLPT Sensei Grammar and Vocabulary List Web Scraper
## Commands to run
1. `pip install pipenv` for creating virtual environment if haven't installed already
2. `pipenv shell` for activating virtual environment
3. `pipenv install --dev` to install project dependencies
4. `python jlptsensei_scraper.py` to obtain list of all grammar and vocabulary for all the JLPT levels stored in the `data` directory
    - NOTE: vocabulary lists for N1 and N2 are incomplete
5. `python ankideck_generator.py` to generate Anki decks in `data/decks` directory
6. Consider donating to the authors' Patreon for their hardwork

## Todo
- generate decks for grammar
