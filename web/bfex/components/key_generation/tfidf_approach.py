from bfex.components.key_generation.key_generation_approach import KeyGenerationApproach
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import *
from bfex.components.data_pipeline.tasks import Task
from collections import Counter
import math
import re
import string

import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from nltk.tokenize import word_tokenize

class TfidfApproach(KeyGenerationApproach):
    def __init__(self):
        self.approach_id = 3
        self.description = """ Generate keyword with TF-IDF """
        

    def generate_keywords(self, text):
        """ Generate keyword with TF-IDF

        TF-IDF = tf x (log(N/df))
        tf = term frequency within the document
        N = # of documents in the corpus (collection of  texts)
        df = # of documents the term appears in

        :param text is the text field from a document object
        :return: keywords as generated by TF-IDF algorithm
        """
        keywords =[]
        scores = {}
        corpus = Document.search().execute()
        N = len(corpus)
        stop_words = ["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","knows","known","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]
        extra_filter = ["research","interests","interested","1","2","3","4","5","6","7","8","9","0"]

        text = re.sub("[^\w']+", ' ', text.lower())
        tokens= nltk.word_tokenize(text)

        #defines the score that tf-idf must be greater than inorder to be considered as a keyword
        if len(tokens) < 20:
            threshold = 1
            bigram_threshold = 1.5
            trigram_threshold = 2
        else:
            threshold = 2
            bigram_threshold = 4
            trigram_threshold = 6 

        single_count = Counter(tokens)
        single_words = list(set(tokens))

        bigram_count = Counter(nltk.bigrams(tokens))
        bigrams = list(nltk.bigrams(tokens))

        trigram_count = Counter(nltk.trigrams(tokens))
        trigrams =list(nltk.trigrams(tokens))

        for word in single_words:
            if word not in stop_words and word not in extra_filter:
                tf = single_count[word]
                df_search = Document.search().query('term', text=word).execute()
                df = len(df_search)
                if df>0:
                    idf = math.log10(N/df)
                    tf_idf = tf*idf
                    scores[word] = tf_idf
                    if tf_idf > threshold and word not in keywords:
                        keywords.append(word)

        for bigram in bigrams:
            if (bigram[0] not in stop_words) and (bigram[1] not in stop_words)\
                and (bigram[0] not in extra_filter) and (bigram[1] not in extra_filter):
                tf = bigram_count[bigram]
                search_bigram = " ".join(bigram)
                df_search = Document.search().query('match_phrase', text=search_bigram).execute()
                df = len(df_search)
                if df>0:
                    score = 0
                    for word in bigram:
                        if word in scores:
                            score = scores[word] + score
                    if score > bigram_threshold and search_bigram not in keywords:
                        keywords.append(search_bigram)
        
        for trigram in trigrams:
            if (trigram[0] not in stop_words) and (trigram[1] not in stop_words)\
             and (trigram[2] not in stop_words) and (trigram[0] not in extra_filter) \
             and (trigram[1] not in extra_filter) and (trigram[2] not in extra_filter):
                tf = trigram_count[trigram]
                search_trigram = " ".join(trigram)
                df_search = Document.search().query('match_phrase', text=search_trigram).execute()
                df = len(df_search)
                if df>0:
                    score = 0
                    for word in trigram:
                        if word in scores:
                            score = scores[word] + score
                    if score>trigram_threshold and search_trigram not in keywords:
                        keywords.append(search_trigram)

        return keywords

        
    def get_id(self):
        return self.approach_id

if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Keywords.init()

    search = Document.search()
    allDocs = [document for document in search.scan()]
    task = TfidfApproach()

    for doc in allDocs:
        results = task.generate_keywords(doc.text)
    