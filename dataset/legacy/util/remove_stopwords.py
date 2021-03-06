import re
from nltk.corpus import stopwords

def remove_stopwords(sentence, lang='english'):

	#We only want to work with lowercase for the comparisons
	sentence = sentence.lower()

	#remove punctuation and split into seperate words
	words = re.findall(r'\w+', sentence, flags = re.UNICODE | re.LOCALE) 

	#This is the more pythonic way
	important_words = filter(lambda x: x not in stopwords.words(lang), words)

	return " ".join(important_words)

def main():
	s = raw_input("String: ")
	l = raw_input("Lang: ")
	print remove_stopwords(s, l)

if __name__ == '__main__':
	main()