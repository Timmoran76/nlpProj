import sys
import json
import string
import csv

def getCommonWords():
    words = []
    with open('english-word-list-total.csv') as csvFile:
        reader = csv.reader(csvFile,delimiter=';')
        ctr = 0
        for line in reader:
            if ctr >= 4 and ctr <= 350:
                words.append(line[1])
            ctr += 1
    return words

# Remove punctuation and special characters from a word, and convert whole
# word to lowercase
def clean(word):
    word = word.rstrip()
    
    if "\xa0" in word:
        #print(word)
        word = word.replace("\xa0","")

    if "-\xa0" in word:
        #print(word)
        word = word.replace("-\xa0","")

    if '"' in word:
        word = word.replace('"','')

    hasPunc = False
    hasComma = False
    for char in word:
        if char in string.punctuation:
            if char == '.':
                hasPunc = True
            if char == ',':
                hasComma = True
            if char != '-':
                word = word.replace(char,'')
        if char == '\\':
            word = word.replace(char,'')

    return (word, hasPunc, hasComma)

def main(source_file,modeP,modeT):
    # Load JSON data and extract the JSON for the first N articles 
    source_json = json.load(source_file)
    raw_data = source_json

    commWords = getCommonWords()
    articleCtr = 0
    
    accuracies = []

    prevPunc = True

    octr = -1
    # Iterate over JSON elements in raw_data
    for element in raw_data:
        octr += 1
        title = element['title']
        title = title.lower()
        
        propPhrase = ""

        wordFreqs = {}
        prnFreqs = {}
        prnTags = []
        ourTags = []
        artTags = []
        # Convert article string to list of cleaned words
        article = element['article']
        if 'keywords' in element:
            if element['keywords']:
                artTags = element['keywords'].split(',')
        #Conver article tags to list, checking first if there are tags
        words = article.split(sep=' ')
        for word in words:
            #if previous word had punctuation
            currPunc = False
            currComma = False
            (word, currPunc, currComma) = clean(word)

            if word.lower() not in commWords and "'s" not in word:
                if word in wordFreqs:
                    wordFreqs[word] += 1
                else:
                    wordFreqs[word] = 1

                if word in title and modeT:
                    wordFreqs[word] *= 2

            if len(word) > 0 and modeP:
                firstChar = word[0]
                #proper noun
                if firstChar.isupper() and not prevPunc:
                    word = word.lower()
                    propPhrase += word + ' '
                    #if proper noun was followed by comma or period, this is end of proper noun phrase
                    if currComma or currPunc:
                        phr = propPhrase[:-1] #cut off last space
                        if phr in prnFreqs:
                            prnFreqs[phr] += 1
                        else:
                            prnFreqs[phr] = 1
                    
                        if phr in title and modeT:
                            prnFreqs[phr] *= 2

                        propPhrase = "" #reset
                #non-proper noun, check if end of proper noun phrase
                else:
                    if(propPhrase != ""):
                        phr = propPhrase[:-1] #cut off last space
                        if phr in prnFreqs:
                            prnFreqs[phr] += 1
                        else:
                            prnFreqs[phr] = 1
                        
                        if phr in title and modeT:
                            prnFreqs[phr] *= 2

                        propPhrase = "" #reset
            
            prevPunc = currPunc
    
        # "sort" dictionary
        freqs = dict(sorted(wordFreqs.items(),key=lambda item: item[1],reverse=True))
        fCtr = 0
        n1Ctr = 0
        for f in freqs: 
            if(fCtr < len(artTags)):
                if(len(f) > 0 and ' ' not in f):
                    ourTags.append(f.lower())
                    fCtr += 1
            elif(len(artTags) == 0):
                if n1Ctr < 5:
                    ourTags.append(f.lower())
                    n1Ctr += 1
        if modeP:
            pFreqs = dict(sorted(prnFreqs.items(),key=lambda item: item[1],reverse=True))
            pCtr = 0
            noneCtr = 0
            for f in pFreqs: 
                if(pCtr < len(artTags) and len(f) > 1):
                    prnTags.append(f.lower())
                    pCtr += 1
                #no tags to compare to, chooses top 5 tags
                elif(len(artTags) == 0):
                    if noneCtr < 5:
                        prnTags.append(f.lower())
                        noneCtr += 1

            combTags = prnTags
            
            if len(prnTags) < len(artTags):
                diff = len(artTags) - len(prnTags)
                combTags += ourTags[:diff]

        if octr < 30:
            if modeP:
                print(combTags)
            else:
                print(ourTags)
        # Compare generated list to source list
        
        correct = 0
        pCorrect = 0
        for tag in artTags:
            if tag[0] == ' ':
                tag = tag[1:]
            if tag.lower() in ourTags:
                correct += 1
            if modeP:
                if tag.lower() in combTags:
                    pCorrect += 1
        if len(artTags) > 0:
            if modeP:
                accuracies.append(pCorrect/len(artTags))
            else:
                accuracies.append(correct/len(artTags))

        articleCtr += 1

    if len(accuracies) > 0:
        return (sum(accuracies)/len(accuracies))
    else:
        return "No Accuracy Available"

if __name__ == "__main__":
    source_file = open('articles2.json')

    if len(sys.argv) > 1:
        source_file = open(sys.argv[1])

    #set modeP to:
    # True if you want only proper noun model
    # False if you want non-proper-noun model

    #set modeT to:
    # True if you want model to have title bias 
    # False if you want non-title-bias model
    acc = main(source_file,True,False)
    print("Our Current Accuracy is " + str(acc))