from unstructured.cleaners.core import clean
from unstructured.cleaners.core import replace_unicode_quotes
from unstructured.documents.elements import Text
from unstructured.cleaners.core import bytes_string_to_string
from unstructured.cleaners.core import bytes_string_to_string
from unstructured.partition.html import partition_html
import re
from unstructured.cleaners.core import clean_bullets
import re
import string
import html
import unidecode
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

stemmer = nltk.stem.PorterStemmer()
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

class Stepni():

    def __init__(self):
        pass

    def preprocess_text(self, x:str):
        # Lowercase
        x = x.lower()

        # Remove punctuation
        x = ''.join(ch for ch in x if ch not in set(string.punctuation))

        # Remove emojis
        regrex_pattern = re.compile(
            pattern="["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE)
        x = regrex_pattern.sub(r'', x)

        # Remove duplicate words
        words = x.split()
        x = ' '.join(sorted(set(words), key=words.index))

        # Remove repeating words
        x = re.sub(r"\b(\w+)(?:\W\1\b)+", r"\1", x, flags=re.IGNORECASE)

        # Remove accents
        x = unidecode.unidecode(x)

        # Remove non-alphanumeric characters
        x = re.sub(r'\W+', ' ', x)

        # Remove non-ASCII characters
        x = re.sub(r'[^\x00-\x7F]', ' ', x)

        # Remove emails
        x = re.sub(r"\S*@\S*\s?", "", x)

        # Remove HTML tags
        x = re.sub('<.*?>', '', x)

        # Remove URLs
        x = re.sub(r"http\S+|www.\S+", "", x)

        # Remove stopwords
        x = ' '.join([word for word in x.split() if word not in set(stopwords.words('english'))])

        # Lemmatize
        lemmatizer = nltk.stem.WordNetLemmatizer()
        w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        x = ' '.join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(x)])

        # Stemming
        stemmer = nltk.stem.PorterStemmer()
        x = ' '.join([stemmer.stem(w) for w in w_tokenizer.tokenize(x)])

        return x


    def cleanIt(self, x:str):
        out = self.preprocess_text(x)
        out = clean(out, bullets=True, lowercase=True,extra_whitespace=True, dashes=True,trailing_punctuation=True)
        out = clean_bullets(out)
        return out

# inp = "[1] ● An excellent point! I love Morse Code! ●●● Geolocated combat footage has confirmed Russian gains in the Dvorichne area northwest of Svatove."


inp= "Hello World! 🌎 This is a sample text for testing the data preprocessing code. It contains some punctuation, emojis 😊, and repeated words. Let's see how the code handles them. Feel free to add or modify this text for additional testing."
func = Stepni()

print(func.cleanIt(inp))