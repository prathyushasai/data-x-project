def loadModel():
    from gensim.models.keyedvectors import KeyedVectors
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  
    return model

def getCategory (labels, word_input, model = None):
    from gensim.models.keyedvectors import KeyedVectors
    if model == None:
        model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)  
    for label in labels: 
        for word in model.most_similar_cosmul(positive=["animal"], topn=100):
            if word[0] == word_input:
                return label
    return word_input
