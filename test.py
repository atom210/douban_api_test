import sys; 

if __name__ == "__main__":
	with open("not exist") as f:
		print "open success..."
	sys.exit(0);
	