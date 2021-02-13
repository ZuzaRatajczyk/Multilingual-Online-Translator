# Multilingual-Online-Translator

This is translator app which is connected to the online web service Reverso Context.
This program enable command-line argumment handling. It's also saves the translations to the file that has the name of the translated word.

# Creating HTTP request

```pip install requests```

```import requests```

HTTP request is formed in ```create_request()``` function and it uses GET method.
It takes word to be translated and diretion of translation as arguments.

```
def create_request(word, direction):
    return requests.get(f'https://context.reverso.net/translation/{direction.lower()}/{word.lower()}',
                        headers={'User-Agent': 'Mozilla/5.0'})
```

# Handling incoming data

This is possible with the BeautifulSoup package. To use it requests module also need to be installed!

```pip install beautifulsoup4```

```from bs4 import BeautifulSoup```

I've created `web_scraping()` function. It returns translated word and usage examples as lists. Usage examples are separated to two list, first in language
from which we trasnlate and second in language we translate into. 

First I've used BeautifulSoup() class to create a parse tree of our page.

`soup = BeautifulSoup(data.content, 'html.parser')`

Next to turn your tree into a formatted string.standard I've used
`soup.prettify()`

Next step is searching for tags by `find_all()` method which return list of all results.

# Get text data

Tranlator gives two types of data: words and usage examples.
There are two separated functions for this purposes: `extract_words()` and `extract_examples()`
Both functions enable to choose number of words/examples to show. 

`text()` method returns a text paragraph from the page.

