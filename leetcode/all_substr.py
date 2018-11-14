import time
import string
import random


n_words = 100
n_string =  100000
words = [''.join(random.sample(string.ascii_letters, 3)) for i in range(n_words)]

L = [random.choice(string.letters) for i in range(n_string)]
s = "".join(L)
t0 = time.time()
for i in words:
    x = s.count(i)
t1 = time.time()
print("Cost:", t1 - t0)

t0 = time.time()
for i in range(n_string):
    x = 0
    for word in words:
        if i + len(word) <= n_string and s[i:i+len(word)] == word:
            x += 1
t1 = time.time()
print("Cost:", t1 - t0)