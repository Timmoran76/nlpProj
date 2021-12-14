import sys

sys.path.insert(1, './rtItems')

import json
import string
import csv
import io
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

    # 1. initialize RAKE by providing a path to a stopwords file
    rake_object = rake.Rake(stoppath, 5, 3, 4)

    accuracies = []
    octr = -1
    for element in raw_data:
        artTags = {}
        octr += 1
        if 'keywords' in element:
            if element['keywords']:
                artTags = element['keywords'].split(',')

        article = element['article']

        article = clean(article)

        f = open("temp.txt", "w")
        f.write(article)
        f.close()
        

        # 2. run on RAKE on a given text
        sample_file = open("temp.txt", 'r',encoding="UTF-8")
        text = sample_file.read()
        sample_file.close()

        keywords = rake_object.run(text)

        ourTags = []
        #take desired length of keywords 
        fCtr = 0
        for sk in keywords: 
            skw = sk[0]
            if(fCtr < len(artTags)):
                if(len(skw) > 0 and not skw.isnumeric()):
                    ourTags.append(skw.lower())
            fCtr += 1

        if octr < 50:
            
            print(ourTags)
            print(artTags)
            print("\n")

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