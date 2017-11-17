import nltk
import string
from nltk.corpus import state_union , stopwords
from nltk.tokenize import PunktSentenceTokenizer



train_text = state_union.raw("2005-GWBush.txt")
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

try:
    import json
except ImportError:
    import simplejson as json



tweets = []
tweets_filename = 'tweets_data.txt'
for line in open(tweets_filename):
  try:
    tweets.append(json.loads(line))
  except:
    pass


  def extract_entity_names(t):
      entity_names = []

      if hasattr(t, 'label') and t.label:
          if t.label() == 'NE':
              entity_names.append(' '.join([child[0] for child in t]))
          else:
              for child in t:
                  entity_names.extend(extract_entity_names(child))

      return entity_names

texts=[]
for tweet in tweets:
    try:
        #texts = [tweet['text'] for tweet['text'] in tweet if tweet['text'] not in stop]
        if tweet['text'] not in stop:
            texts.append(tweet['text'])
            #print(tweet['text'])

    except:
        pass
#print(texts)


entity_names = []
for eachText in texts:

    tokenized = custom_sent_tokenizer.tokenize(eachText)
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)

            namedEnt = nltk.ne_chunk(tagged, binary=True)
            for tree in namedEnt:
                #print(tree)
                entity_names.extend(extract_entity_names(tree))
    except Exception as e:
        print(str(e))

#print(entity_names)

all_words = []
for w in entity_names:
    all_words.append(w.lower())

#print(all_words)

all_words = nltk.FreqDist(all_words)

finalResult = []


finalResult = all_words.most_common(10)
print(finalResult)
f = open("queryKeywords.txt", "w+")
for i in finalResult:
        f.write("%s\n" % (i[0]))
f.close()