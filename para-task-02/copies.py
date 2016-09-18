import sys, hashlib, os
dir = sys.argv[1]
tree = os.walk(dir)
dic = {}
for root, dirs, files in tree:
	for file in files:
		if file[0] != ".":
			name = dir + '/'.join(dirs) + "/" + file
			hashed = hashlib.md5(open(name, "rb").read()).hexdigest();
			if not(hashed in dic):
				dic[hashed] = []
			dic[hashed].append(name)
for k, v in dic.items():
	if len(v) > 1:
		print(':'.join(v))
