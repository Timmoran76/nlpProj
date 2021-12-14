import sys

sys.path.insert(1, './rtItems')

import json
import string
import io, six
import rake
import operator

# Load JSON data and extract the JSON
source_file = open('articles2.json')
source_json = json.load(source_file)
raw_data = source_json


# Remove punctuation and special characters from a word, and convert whole
# word to lowercase
def clean(text):
    
    if "\xa0" in text:
        #print(word)
        text = text.replace("\xa0","")

    if "-\xa0" in text:
        #print(word)
        text = text.replace("-\xa0","")

    if '"' in text:
        text = text.replace('"','')

    if "â\x80" in text:
        text = text.replace("â\x80","")

    if "\x99" in text:
        text = text.replace("\x99","")

    return text

def main():
    # EXAMPLE ONE - SIMPLE
    stoppath = "rtItems/data/stoplists/SmartStoplist.txt"

    octr = -1
    accuracies = []
    for element in raw_data:
        octr += 1
        if 'keywords' in element:
            if element['keywords']:
                artTags = element['keywords'].split(',')

        article = element['article']

        article = clean(article)
        '''
        f = open("temp.txt", "w")
        f.write(article)

        # 2. run on RAKE on a given text
        sample_file = io.open("temp.txt", 'r',encoding="UTF-8")
        text = sample_file.read()
        '''
        sentenceList = rake.split_sentences(article)

        
        # generate candidate keywords
        stopwords = rake.load_stop_words(stoppath)
        stopwordpattern = rake.build_stop_word_regex(stoppath)
        phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern, stopwords)

        # calculate individual word scores
        wordscores = rake.calculate_word_scores(phraseList)

        # generate candidate keyword scores
        keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)

        # sort candidates by score to determine top-scoring keywords
        sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
        totalKeywords = len(sortedKeywords)

        ourTags = []
        #take desired length of keywords 
        fCtr = 0
        for sk in sortedKeywords: 
            skw = sk[0]
            if(fCtr < len(artTags)):
                if(len(skw) > 0 and not skw.isnumeric()):
                    ourTags.append(skw.lower())
                    fCtr += 1

        if octr < 50:
            print(ourTags)

        # Compare generated list to source list
        correct = 0
        for tag in artTags:
            if tag[0] == ' ':
                tag = tag[1:]
            if tag.lower() in ourTags:
                correct += 1
            
        if len(artTags) > 0:
            accuracies.append(correct/len(artTags))
            
    return (sum(accuracies)/len(accuracies))



if __name__ == "__main__":
    acc = main()
    print("Our Current Accuracy is " + str(acc))