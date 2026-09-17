from ast import Or

import spacy

text = """ Arthur Smith bought a Samsung phone in Macau . It
was cheaper than in his own country . """
nlp = spacy.load("en_core_web_sm")
doc = nlp (text)

# example 1.1
print("Tokens:")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_,token.dep_)

# example 1.2 
#python -m spacy download pt_core_news_sm
sentence = """ O Artur Mendes comprou um telefone Samsung em
Macau . """

nlp = spacy.load("pt_core_news_sm")
doc = nlp ( sentence )
for token in doc :
    print ( token.text , token.lemma_ , token.pos_ , token.tag_ ,
            token.ent_type_ ,
            token.dep_ , token.shape_ , token.is_alpha , token.is_stop )

# example 1.3
sentence = """ O Artur Mendes comprou um telefone Samsung em
Macau . """
nlp = spacy.load ("pt_core_news_sm")
doc = nlp ( sentence )

for ent in doc . ents :
    print ( ent.text , ent.start_char ,ent.end_char , ent.label_ )

# example 1.4
#from spacy import displacy
#displacy.serve(doc , style = "ent" )
#displacy.serve(doc , style = "dep" )

#Exercise 1.1
# Obtain the lemmas of all content words (i.e., those that are
# not stopwords);
print("Exercise 1.1: Lemmas of content words:")
for token in doc:
    if not token.is_stop:
        print(token.text, token.lemma_, token.pos_, token.tag_,token.dep_)

# Exercise 1.2
# Find examples for which, in different contexts:
# The same word is classified with different grammatical categories

# print("Exercise 1.2: Examples of words with different grammatical categories:")
# for ent in docs.ent check that if the ent.label is different for each ent.text
for ent in doc.ents:
# check that if the ent.label is different for each ent.text
    if ent.label_ != "":
        print("in loop")
        print(ent.text, ent.label_)
    
