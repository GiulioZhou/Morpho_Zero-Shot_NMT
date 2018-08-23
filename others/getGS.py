import sys

#
wordlist = []
# with open("./GS_NO.eng","r") as input:
# 	with open("./GS_seg_NO","a") as output:
# 		for line in input:
# 			output.write(" ".join(line.split()[1:])+"\n")
# with open("./GS_NO.eng","r") as input:
# 	with open("./wordlist.morph.NO","a") as output:
# 		for line in input:
# 			output.write(line.split()[0]+"\n")
#
# # print (wordlist)
#
total_predicted_positive = 0
total_actual_postivie = 0
true_positive = 0

segmentation = []
result =[]


with open("./GS_seg","r") as input:
	for line in input:
		segmentation.append(line.split())

with open(sys.argv[1],"r") as input:
	for line in input:
		result.append(line.lower().split())


for i in range(len(segmentation)):
	total_actual_postivie += len(segmentation[i])
	total_predicted_positive += len(result[i])

	for seg in result[i]:
		if seg in segmentation[i]:
			true_positive += 1

# print (true_positive)
precision = true_positive/total_predicted_positive
recall = true_positive/total_actual_postivie
f1 = 2*((precision*recall)/(precision+recall))
print("precision: "+str(precision))
print("recall: "+str(recall))
print("f1: "+str(f1))
