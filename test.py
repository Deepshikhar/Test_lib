from unstructured.cleaners.core import (
    replace_unicode_quotes,
    bytes_string_to_string,
    clean,
    clean_bullets,
    clean_dashes,
    clean_extra_whitespace,
    clean_non_ascii_chars,
    clean_ordered_bullets,
    clean_postfix,
    clean_prefix,
    clean_trailing_punctuation,
    group_broken_paragraphs,
    remove_punctuation,
    replace_unicode_quotes,
)
from unstructured.partition.html import partition_html
from unstructured.cleaners.translate import translate_text
from unstructured.documents.elements import Text
import re
import string
import html
import unidecode
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter



class TextCleaner():

    def __init__(self):
        pass

    def preprocess_text(self, text:str):
        # Lowercase
        stemmer = nltk.stem.PorterStemmer()
        w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        lemmatizer = nltk.stem.WordNetLemmatizer()
        text = text.lower()

        # Remove punctuation
        text = ''.join(ch for ch in text if ch not in set(string.punctuation))

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
        text = regrex_pattern.sub(r'', text)

        # Remove duplicate words
        words = text.split()
        for i in range(0, len(words)):
            words[i] = ''.join(words[i])
        UniqW = Counter(words)
        text = ' '.join(UniqW.keys())
        # text = ' '.join(sorted(set(words), key=words.index))

        # Remove repeating words
        text = re.sub(r"\b(\w+)(?:\W\1\b)+", r"\1", text, flags=re.IGNORECASE)

        # Remove accents
        text = unidecode.unidecode(text)

        # Remove non-alphanumeric characters
        text = re.sub(r'\W+', ' ', text)

        # Remove non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]', ' ', text)

        # Remove emails
        text = re.sub(r"\S*@\S*\s?", "", text)

        # Remove HTML tags
        text = re.sub('<.*?>', '', text)

        # Remove URLs
        text = re.sub(r"http\S+|www.\S+", "", text)

        # Remove stopwords
        text = ' '.join([word for word in text.split() if word not in set(stopwords.words('english'))])

        # Stemming
        stemmer = nltk.stem.PorterStemmer()
        text = ' '.join([stemmer.stem(w) for w in w_tokenizer.tokenize(text)])

        # Lemmatize
        lemmatizer = nltk.stem.WordNetLemmatizer()
        w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
        text = ' '.join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)])

        return text

    @staticmethod
    def unstructured_text(text, translation_source=None, translation_target=None):
        # Creating an element from the text
        element = Text(text)

        # Applying all available operations
        element.apply(replace_unicode_quotes)
        # element.apply(bytes_string_to_string)
        element.apply(clean)
        element.apply(clean_bullets)
        element.apply(clean_dashes)
        element.apply(clean_extra_whitespace)
        element.apply(clean_non_ascii_chars)
        element.apply(clean_ordered_bullets)
        element.apply(lambda text: clean_postfix(text, r"(END|STOP)", ignore_case=True))
        element.apply(lambda text: clean_prefix(text, r"(SUMMARY|DESCRIPTION):", ignore_case=True))
        element.apply(clean_trailing_punctuation)
        element.text = group_broken_paragraphs(element.text)
        element.text = remove_punctuation(element.text)
        elements = partition_html(text=element.text)
        if elements:
            element = elements[0]  # Considering only the first element
        # if translation_source and translation_target:
        #     element.text = translate_text(element.text, translation_source, translation_target)

        return element.text

    
    

# Example usage:
text = """1.1 This is a very important point
 ●The big brown fox
was walking down the lane.

At the end of the lane, the

fox met a bear. """

processor = TextCleaner()
processed_text = processor.unstructured_text(text)
print(processed_text)

processor = TextCleaner()
processed_text = processor.preprocess_text(processed_text)
print(processed_text)

