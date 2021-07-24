import hashlib

text = "Think and wonder, wonder and think."
text2 = "Think and wonder, wonder and think"
hash_object = hashlib.md5(text.encode()).hexdigest()
hash_object2 = hashlib.md5(text2.encode()).hexdigest()
print(hash_object == hash_object2)