import json
import string

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

source_file = open('articles2.json')

source_json = json.load(source_file)
raw_data = source_json
allW = []
ac = 0
for element in raw_data:
    
    article = element['article']

    words = article.split(sep=' ')
    for word in words:
        (cword,_,_) = clean(word)
        if cword.lower() not in allW:
            allW.append(cword.lower())

    ac +=1

    print(str(len(allW)) + '  ' + str(ac))
