import torch, argparse, sys, json, string

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

    for char in word:
        if char in string.punctuation:
                word = word.replace(char,'')
        if char == '\\':
            word = word.replace(char,'')

    return word.lower()

if __name__ == '__main__':
    data_file  = open('articles2.json')
    source_json = json.load(data_file)
    raw_data = source_json

    vocab = set()
    article_count = 0
    total_words = 0

    print(f'Number of json elements: {len(raw_data)}')

    for element in raw_data:
        title = element['title']
        article = element['article']
        content = title + ' ' + article
        words = content.split(sep=' ')
        for word in words:
            total_words += 1
            cword = clean(word)
            vocab.update(cword)

        article_count += 1

print(f'Total articles processed: {article_count}')
print(f'Total words found: {total_words}')
print(f'Total unique words found: {len(vocab)}')
print(f'Average words per article: {total_words/article_count}')
print(f'Percentage of distinct words: {(len(vocab)/total_words) * 100}%')



    
    # parser = argparse.ArgumentParser()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('--train', type=str, help='training data')
    # parser.add_argument('--dev', type=str, help='development data')
    # parser.add_argument('infile', nargs='?', type=str, help='test data to translate')
    # parser.add_argument('-o', '--outfile', type=str, help='write translations to file')
    # parser.add_argument('--load', type=str, help='load model from file')
    # parser.add_argument('--save', type=str, help='save model in file')
    # args = parser.parse_args()

    # if args.train:
        # Read training data and create vocabularies
        # traindata = None
