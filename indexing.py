#-------------------------------------------------------------------------
# AUTHOR: Lokaranjan Munta
# FILENAME: indexing.py
# SPECIFICATION: The program reads collection.csv, calculates the document-term matrix with tf-idf, and prints it
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
stopWords = {"i", "and", "she", "her", "they", "their"}

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
stemming = {
    "cats": "cat",
    "loves": "love",
    "dogs": "dog"
}

# Function to clean the documents using stop words and stemming
def clean_and_stem_document(document):
    words = document.lower().split()   # Lower case and split words
    cleaned = []

    for word in words:
        if word not in stopWords:   # No stop words
            stemmed_word = stemming.get(word, word)   # Stem if in stemming dictionary
            cleaned.append(stemmed_word)   # Add cleaned word

    return cleaned

# Clean and stem all documents
cleaned_documents = []
for document in documents:
    cleaned_documents.append(clean_and_stem_document(document))

#Identifying the index terms.
terms = set()   # Set for unique values

for document in cleaned_documents:
    for word in document:
        terms.add(word)   # Add word to set

terms = list(terms)   # Convert back to list

# Method to calculate TF
# tf(t, d) = count of t in d / number of terms in d
def tf(term, document):
    return document.count(term) / len(document)

# Method to calculate DF
# df(t, D) = occurence of t in documents D
def df(term, all_documents):
    count = 0
    for document in all_documents:
        if term in document:
            count += 1
    return count

# Method to calculate IDF
# idf(t, D) = log(|D| / df(t, D))
def idf(term, all_documents):
    document_df = df(term, all_documents)
    if document_df == 0:
        return 0   # To stop division by 0
    return math.log10(len(all_documents) / document_df)

# Method to calculate TF-IDF
# tf-idf(t, d, D) = tf(t, d) * idf(t, D)
def tf_idf(term, document, all_documents):
    return tf(term, document) * idf(term, all_documents)

#Building the document-term matrix by using the tf-idf weights.
docTermMatrix = []

for document in cleaned_documents:
    tf_idf_list = []
    for term in terms:
        tf_idf_list.append(tf_idf(term, document, cleaned_documents))   # Calculate TF-IDF for each term
    docTermMatrix.append(tf_idf_list)

#Printing the document-term matrix.
print("Document-Term Matrix")
print("\t" + "     ".join(terms))
for i, row in enumerate(docTermMatrix):
    print(f"d{i+1}:", "\t".join(f"{value:.3f}" for value in row))

'''
Document-Term Matrix
	love     cat     dog
d1: 0.000	0.117	0.000
d2: 0.000	0.000	0.088
d3: 0.000	0.059	0.059
'''