f = open("Restaurants_Train_v2.xml")
sentences = {
	"sentence" : [],
	"aspects" : []
}
rows = []
for row in f:
	rows.append(row)

l = len(rows)
i = 0
s_count = 0
a_count = 0
while i < l:
	row = rows[i]
	if "<text>" in row and "</text>" in row:
		sentence = row[row.find("<text>") + 6 : row.find("</text>")]
		i = i + 1
		row = rows[i]
		sentences["sentence"].append(sentence)
		aspects = dict()
		s_count += 1	
		if "<aspectTerms>" in row:
			a_count += 1
			i += 1
			row = rows[i]
			while not "</aspectTerms>" in row:
				if "<aspectTerm term=" in row:
					row = row.strip()
					aspect = row[row.find("<aspectTerm term=") + 18: row.find("polarity=") - 2]
					polarity = row[row.find("polarity=") + 10 : row.find("from=") - 2]
					aspects[aspect] = polarity
				i += 1
				row = rows[i]
		sentences["aspects"].append(aspects)
	i += 1

print(len(sentences["sentence"]), len(sentences["aspects"]))

from nltk import word_tokenize

l = len(sentences["sentence"])
i = 0
output_sentences = []
fout = open("Restaurants_preprocessed.txt","w")

while i < l:
	output_string = ""
	original_sen = sentences["sentence"][i]
	aspects = sentences["aspects"][i]
	tokens = word_tokenize(original_sen)
	token_label = []
	for token in tokens:
		token_label.append([token, "o"])
	sen = original_sen.lower()
	tokens = [token.lower() for token in tokens]
	# print(tokens)
	for aspect in aspects:
		polarity = aspects[aspect].upper()[:3]
		start = "B-" + polarity
		intermediate = "I-"+polarity
		aspect = aspect.lower()
		aspect_tokens = word_tokenize(aspect)
		# print(aspect_tokens)
		aspect_length = len(aspect_tokens)
		for j in range(aspect_length,len(tokens)):
			k = j - aspect_length
			is_it_aspect = True
			for ind in range(k, j):
				if tokens[ind] != aspect_tokens[ind - k]:
					is_it_aspect = False
			if is_it_aspect:
				# print("matched")
				token_label[k][1] = start
				for ind2 in range(k + 1, j):
					token_label[ind2][1] = intermediate
				# print(token_label)
	output_sentences.append(token_label)
	final_sentence = original_sen+"###"
	for token in token_label:
		final_sentence += (token[0]+"="+token[1]+" ")
	final_sentence = final_sentence.strip()
	print(final_sentence)
	fout.write(final_sentence+"\n")
	i += 1

