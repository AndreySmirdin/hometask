import sys, hashlib, os

def read_and_hash(name):
	digest = hashlib.md5()
	with open(name, "rb") as f:
		digest.update(f.read(1000))
	return digest.hexdigest()	

def find_copies(dir):
	tree = os.walk(dir)
	dic = {}
	for root, dirs, files in tree:
		for file in files:
			if file[0] != "." and file[0] != "~":
				name = dir + '/'.join(dirs) + "/" + file
				hashed = read_and_hash(name)
				if not(hashed in dic):
					dic[hashed] = []
				dic[hashed].append(name)
	print_copies(dic)

def print_copies(dic):
	for k, v in dic.items():
		if len(v) > 1:
			print(':'.join(v))

dir = sys.argv[1]
find_copies(dir)