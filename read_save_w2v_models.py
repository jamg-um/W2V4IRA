import os
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
warnings.filterwarnings(action='ignore')
##Code to read a text file and produce two w2v models: CBOW and Skip-Gram

input_text_file = "pppprw_SCT_onto.txt"
output_CBOW_model = "SCT_model_CBOW.model"
output_SKIP_model = "SCT_model_Skip.model"


sample = open(input_text_file)
s = sample.read()

# Replaces escape character with space
f = s.replace("\n", " ")

data = []

# iterate through each sentence in the file
for i in sent_tokenize(f):
	temp = []

	# tokenize the sentence into words
	for j in word_tokenize(i):
		temp.append(j.lower())

	data.append(temp)

model1 = gensim.models.Word2Vec(data, min_count=1,	vector_size=100, window=6)
model1.save(output_CBOW_model)

model2 = gensim.models.Word2Vec(data, min_count=1, vector_size=100, window=6, sg=1)
model2.save(output_SKIP_model)