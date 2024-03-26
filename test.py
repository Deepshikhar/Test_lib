from unstructured.cleaners.core import clean
from unstructured.cleaners.core import replace_unicode_quotes
from unstructured.documents.elements import Text
from unstructured.cleaners.core import bytes_string_to_string
from unstructured.cleaners.core import bytes_string_to_string
from unstructured.partition.html import partition_html
import re
from unstructured.cleaners.core import clean_bullets




class Stepni():

    def __init__(self):
        pass

    def cleanIt(self, x:str):
        out = clean(x, bullets=True, lowercase=True,extra_whitespace=True, dashes=True,trailing_punctuation=True)
        out = clean_bullets(out)
        return out
    

inp = "[1] ● An excellent point! I love Morse Code! ●●● Geolocated combat footage has confirmed Russian gains in the Dvorichne area northwest of Svatove."


fun = Stepni()

print(fun.cleanIt(inp))