import spacy

text = """ Arthur Smith bought a Samsung phone in Macau . It
was cheaper than in his own country . """
nlp = spacy.load("en_core_web_sm")
doc = nlp (text)