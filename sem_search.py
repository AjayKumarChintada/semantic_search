# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spacy
import gensim
import operator
import re
import string


# %%
df = pd.read_csv('movies.csv')
df.head()

# %%
from spacy.lang.en.stop_words import STOP_WORDS
spacy_nlp = spacy.load('en_core_web_sm')
punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# %%
def spacy_tokenizer(sentence):
 
    #remove distracting single quotes
    sentence = re.sub('\'','',sentence)

    #remove digits adnd words containing digits
    sentence = re.sub('\w*\d\w*','',sentence)

    #replace extra spaces with single space
    sentence = re.sub(' +',' ',sentence)

    #remove unwanted lines starting from special charcters
    sentence = re.sub(r'\n: \'\'.*','',sentence)
    sentence = re.sub(r'\n!.*','',sentence)
    sentence = re.sub(r'^:\'\'.*','',sentence)
    
    #remove non-breaking new line characters
    sentence = re.sub(r'\n',' ',sentence)
    
    #remove punctunations
    sentence = re.sub(r'[^\w\s]',' ',sentence)
    
    #creating token object
    tokens = spacy_nlp(sentence)
    
    #lower, strip and lemmatize
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]
    
    #remove stopwords, and exclude words less than 2 characters
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]
    
    #return tokens
    return tokens


# %%
df['tokenized_wiki']= df ['wiki_plot'].map(lambda x: spacy_tokenizer(x))

# %%
df.head()

# %%
movie_plot= df['tokenized_wiki']
movie_plot[:3]

# %%
from gensim import corpora
dictionary = corpora.Dictionary(movie_plot)


# %%


# %%
vals=[[val,key] for key,val in dictionary.items() if key<=50]


# %%
bow= [dictionary.doc2bow(words) for words in movie_plot]



# %%
word_frequencies = [[(dictionary[id], frequency) for id, frequency in line] for line in bow[0:1]]
word_frequencies


# %%
a=np.array(movie_plot)[0]
a.count('accept')

# %%
movie_tfidf_model = gensim.models.TfidfModel(bow, id2word=dictionary)
movie_lsi_model = gensim.models.LsiModel(movie_tfidf_model[bow], id2word=dictionary, num_topics=300)

# %%
tfidif_mode=movie_tfidf_model[bow]
lsi_model=movie_lsi_model[movie_tfidf_model[bow]]




# %%

# print(len(dictionary),movie_lsi_model.num_terms)


# %%
from gensim.similarities import MatrixSimilarity
sim_index = MatrixSimilarity(lsi_model, num_features=len(dictionary))

# %%
from operator import itemgetter

def search_similar_movies(search_term):

    query_bow = dictionary.doc2bow(spacy_tokenizer(search_term))
    query_tfidf = movie_tfidf_model[query_bow]
    query_lsi = movie_lsi_model[query_tfidf]

    sim_index.num_best = 5

    movies_list = sim_index[query_lsi]

    movies_list.sort(key=itemgetter(1), reverse=True)
    movie_names = []

    for j, movie in enumerate(movies_list):

        movie_names.append (
            {
                'Relevance': round((movie[1] * 100),2),
                'Movie Title': df['title'][movie[0]],
                'Movie Plot': df['wiki_plot'][movie[0]]
            }

        )
        if j == (sim_index.num_best-1):
            break

    return pd.DataFrame(movie_names, columns=['Relevance','Movie Title','Movie Plot'])

# %%
# (sim_index.num_best,sim_index.num_features)



# %%
# search_similar_movies('violence protest march ')


