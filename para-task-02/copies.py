import sys, hashlib, os

def read_and_hash(name):
	digest = hashlib.md5()
	with open(name, "rb") as f:
		new = f.read(1000)
		while new:
			digest.update(new)
			new = f.read(1000)
	return digest.hexdigest()	

def find_copies(dir):
	dic = {}
	for root, dirs, files in os.walk(dir):
		for file in files:
			if file[0] != "." and file[0] != "~" and  not os.path.islink(file):
				name = os.path.join(root, file)
				hashed = read_and_hash(name)
				if not(hashed in dic):
					dic[hashed] = []
				dic[hashed].append(name)
	return dic

def print_copies(hash_list):
	for v in hash_list.values():
		if len(v) > 1:
			print(':'.join(v))

dir = sys.argv[1]
hash_list = find_copies(dir)
print_copies(hash_list)