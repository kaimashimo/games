import pickle
import streamlit as st
from scipy import spatial

@st.cache(suppress_st_warning=True)
def get_dict():
    with open('embeddings.pkl','rb') as f:
        d = pickle.load(f)
    return d

def distance(word, reference):
    return spatial.distance.cosine(embeddings[word], embeddings[reference])

def closest_words(reference):
    return sorted(embeddings.keys(), key=lambda w: distance(w, reference))

def goodness(word, answers, bad):
    if word in answers + bad: return -999
    return sum([distance(word, b) for b in bad]) - 4.0 * sum([distance(word, a) for a in answers])

def minimax(word, answers, bad):
    if word in answers + bad: return -999
    return min([distance(word, b) for b in bad]) - max([distance(word, a) for a in answers])

def candidates(answers, bad, size=100):
    best = sorted(embeddings.keys(), key=lambda w: -1 * goodness(w, answers, bad))
    res = [(str(i + 1), "{0:.2f}".format(minimax(w, answers, bad)), w) for i, w in enumerate(sorted(best[:250], key=lambda w: -1 * minimax(w, answers, bad))[:size])]
    return [(". ".join([c[0], c[2]]) + " (" + c[1] + ")") for c in res]

st.write("# Joshenkanator 9000")
st.write('_so it\'s the computer\'s fault when we lose at codenames_')

answers = [x.strip() for x in st.text_input('Input your comma-separated words to get:').split(',')]
bad = [x.strip() for x in st.text_input('Input your comma-separated words to avoid:').split(',')]

if answers and bad:
    generate_candidates = st.button('Generate candidates:')
    if generate_candidates:
        embeddings = get_dict()
        st.write(candidates(answers, bad))
        st.balloons()