import difflib
import numpy
from pypo.data_list import regions_list_all
import json

with open('file/regions.json', 'r',encoding='utf-8') as fp:
	regions = json.load(fp)
def find_closet_match_name(test_str, list2check):

	list3check = list2check
	a = []
	for i in list2check:
		a.append(i[0])
	list2check =a
	
	a = []

	for ii in range(0,3):

		scores = {}
		for ii in list2check:
			cnt = 0
			if len(test_str)<=len(ii):
				str1, str2 = test_str, ii
			else:
				str1, str2 = ii, test_str
			for jj in range(len(str1)):
				cnt += 1 if str1[jj]==str2[jj] else 0
			scores[ii] = cnt
		scores_values        = numpy.array(list(scores.values()))
		closest_match_idx    = numpy.argsort(scores_values, axis=0, kind='quicksort')[-1]
		closest_match        = numpy.array(list(scores.keys()))[closest_match_idx]
		
		a.append(list3check[closest_match_idx])
		list2check.pop(closest_match_idx)
		
	return a