from nltk.corpus import movie_reviews
import hashlib

reviews = []

for fileid in movie_reviews.fileids("pos"):
    reviews.extend(movie_reviews.words(fileid))

for fileid in movie_reviews.fileids("neg"):
    reviews.extend(movie_reviews.words(fileid))
    
result = 0

### TODO
### implement flajolet martin algorithm to count distinct elements.

max_zeros = 0

for word in reviews:
    hash_value = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16)
    trailing_zeros = len(bin(hash_value)[2:]) - len(bin(hash_value)[2:].rstrip('0'))
    max_zeros = max(max_zeros, trailing_zeros)

result = 2 ** max_zeros


### end of TODO

print(f"{result}")