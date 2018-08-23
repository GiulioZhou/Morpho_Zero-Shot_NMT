#For all the language pairs, remove metadata and insert the target tokens
#NOTE-> it doesn't work with xml files!
import os, shutil, re

languages = ["en","de","it","nl","ro"]
input_dir = "./working_dir/"
output_dir = "./out_dir/"
devset = "IWSLT17.TED.dev2010."
testset = "IWSLT17.TED.tst2010."
# testset = "IWSLT17.TED.tst2017.mltlng."

def remove(ext,trg):
	with open(input_dir+"train.tags."+ext,"r") as input:
		with open(output_dir+"train."+ext,"w") as output:
			for line in input:
				if not (line.startswith("<") or line.startswith(" <")):
					if trg:
						output.write("-2"+trg+"- "+line)
					else:
						output.write(line)


def removeXML(ext,trg):
	with open(input_dir+devset+ext+".xml","r") as input:
		with open(output_dir+"dev."+ext,"a") as output:
			for line in input:
				if line.startswith("<seg"):
					text = re.sub('<.*?>', '', line)
					if trg:
						output.write("-2"+trg+"- "+text)
					else:
						output.write(text)

	with open(input_dir+testset+ext+".xml","r") as input:
		with open(output_dir+"test."+ext,"a") as output:
			for line in input:
				if line.startswith("<seg"):
					text = re.sub('<.*?>', '', line)
					if trg:
						output.write("-2"+trg+"- "+text)
					else:
						output.write(text)

#Create the output directory if it doesn't exist
try:
    os.stat(output_dir)
except:
    os.mkdir(output_dir)


for src in languages:
	for trg in languages:
		if src == trg:
			continue
		else:
			ext = src+"-"+trg+"."
			#training set
			remove(ext+src,trg)
			remove(ext+trg,"")
			# #devset
			removeXML(ext+src,trg)
			removeXML(ext+trg,"")
			print (ext)

#Empty the input directory =
# shutil.rmtree(input_dir)
# os.mkdir(input_dir)
