#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

# ======================================================================================
# File		 : douban_merge_data.py
# Author	   : zhanggongyuan 
# Last Change  : 04/26/2016 | 19:25:38 PM | Tuesday,April
# Description  : 
# ======================================================================================

import os, sys, pickle

# ======================================================== 
# function: merge_movie_detail_info
# ======================================================== 
def merge_movie_detail_info(year, fno):
	merge_info_list = [];
	fetch_fname = "fetch_out/%d/fetch_%03d.pkl" % (year, fno);
	meta_fname = "meta_out/%d/meta_%03d.pkl" % (year, fno);
	meta_dict = dict();
	with open(fetch_fname, "r") as fetch_file, open(meta_fname, "r") as meta_file:
		movie_detail_list = pickle.load(fetch_file);
		meta_info_list = pickle.load(meta_file);
		## foreach meta_info_list
		for item in meta_info_list:
			try : 
				url = item[u"alt"].encode("utf-8");
				countries = [ ci.encode("utf-8") for ci in item[u"countries"] ];
				year = int(item[u"year"].encode("utf-8"), 10);
				reviews_count = item[u"reviews_count"];
				meta_dict[url] = (countries, year, reviews_count);
			except :
				pass ; 
		
		## foreach movie_detail_list
		for item in movie_detail_list:
			try : 
				url = item["link_info"][0];
				merge_info = item; 
				if meta_dict.has_key(url):
					merge_info["countries"] = meta_dict[url][0];
					merge_info["year"] = meta_dict[url][1];
					merge_info["reviews_count"] = meta_dict[url][2];
				merge_info_list.append(merge_info);
			except :  
				pass ; 

	return merge_info_list;

if __name__ == "__main__":
	
	sys.exit(0);
