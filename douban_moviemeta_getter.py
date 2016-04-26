#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

# ======================================================================================
# File		 : douban_moviemeta_getter.py
# Author	   : zhanggongyuan 
# Last Change  : 04/26/2016 | 16:44:47 PM | Tuesday,April
# Description  : 
# ======================================================================================

import sys, os, time
import requests, pickle

# ======================================================== 
# get movie meta info by douban api v2
# ======================================================== 
def get_movie_metainfo_with_apiv2(movie_id, apikey=""):
	base_url = "http://api.douban.com";
	req_url = "%s/v2/movie/subject/%s" % (base_url, movie_id);
	if apikey != "":
		req_url = "%s?apikey=%s" % (req_url, apikey);
	
	##print "do request: %s" % req_url;
	rsp = requests.get(req_url);
	print "request.url : %s \t status: %d" % (rsp.url, rsp.status_code);

	if rsp.status_code == 200:
		return ( rsp.json(), 0 ) ; 
	else:
		return ( None, rsp.json()["code"] );
	pass ; 

if __name__ == "__main__":

	##loop_year = 2015; apikey = "05b2e24806124f0f1118a6d81236ed2d"; 
	##loop_year = 2014; apikey = "05b2e24806124f0f1118a6d81236ed2d"; 
	loop_year = 2013; apikey = "05b2e24806124f0f1118a6d81236ed2d"; 
	src_path = "fetch_out/%d" % loop_year;
	dst_path = "meta_out/%d" % loop_year;
	if not os.path.exists(dst_path):
		os.mkdir(dst_path, 0755);
	
	beg_time = time.time();
	fname_list = os.listdir(src_path);
	##for fname in fname_list[0:1]:
	for fname in fname_list:
		meta_info_list = [];
		fno = int(fname[6:9], 10);
		src_fname = "%s/%s" % (src_path, fname);
		dst_fname = "%s/meta_%03d.pkl" % (dst_path, fno);
		with open(src_fname, "r") as src_file, open(dst_fname, "w+") as dst_file:
			movie_detail_list = pickle.load(src_file);
			for movie_detail in movie_detail_list:
				try:
					movie_id = movie_detail["link_info"][0].split('/')[-2];
					meta_info, iRet = get_movie_metainfo_with_apiv2(movie_id, apikey);
					if iRet != 0 and iRet == 111:
						end_time = time.time();
						time.sleep(3601 - (end_time - beg_time));
						beg_time = time.time();
						meta_info, iRet = get_movie_metainfo_with_apiv2(movie_id, apikey);
					if iRet == 0 and meta_info is not None:
						meta_info_list.append(meta_info);
				except:
					pass;

			pickle.dump(meta_info_list, dst_file); 

		pass ; 

	sys.exit(0);



