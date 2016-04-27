#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

# ======================================================================================
# File		 : douban_flat_movie_detail.py
# Author	   : zhanggongyuan 
# Last Change  : 04/27/2016 | 10:59:49 AM | Wednesday,April
# Description  : 
# ======================================================================================

import os, sys, pickle;
from exceptions import Exception;
import traceback;

def douban_flat_movie_detail(merge_fname, actors_ofname, movie_ofname):

	try : 
		with open(merge_fname, "r") as merge_file, open(actors_ofname, "a+") as actors_file, \
				open(movie_ofname, "a+") as movie_file:
			merge_info_list = pickle.load(merge_file);
			for item in merge_info_list:
				mtype = "unknown"; year = 0; rating_score = 0; rating_people = 0; reviews_count = 0;
				countries = "unknown"; title = "unknown"; subtype = "unknown"; url = "";
				if item.has_key("year"): year = item["year"];
				if item.has_key("rating_score"): rating_score = item["rating_score"];
				if item.has_key("rating_people"): rating_people = item["rating_people"];
				if item.has_key("reviews_count"): reviews_count = item["reviews_count"];
				if item.has_key("movie_type"): mtype = "/".join(item["movie_type"]);
				if item.has_key("countries"): countries = "/".join(item["countries"]);
				if item.has_key("subtype"): subtype = item["subtype"];
				if item.has_key("link_info"): 
					title = item["link_info"][1]; url = item["link_info"][0];
					title.replace(",", "_");

				try :
					movie_id = url.split('/')[-2];
				except IndexError:
					continue ; 
				if year < 2012: continue;   ## skip movies before 2012
				## movie_desc -> title, movie_type, year, countries, rating_score, rating_people, reviews_count, subtype
				movie_desc = "%s,%s,%d,%s,%.2f,%d,%d,%s" % \
						(title, mtype, year, countries, rating_score, rating_people, reviews_count, subtype); 
				## movie record: movie_id, url, movie_desc
				movie_file.write( "%s,%s,%s\n" % (movie_id, url, movie_desc) );

				PLAYER_TYPE = { "directors" : 1, "actors" : 2, "script_writers" : 3 };
				PLAYER_KEYS = [ "directors", "actors", "script_writers" ];
				for key in PLAYER_KEYS:
					if not item.has_key(key): continue;
					member_list = item[key];
					for order, member in enumerate(member_list):
						## player_desc: actor_id,actor_name,player_type,order,movie_id,url
						actors_file.write("%s,%s,%d,%d,%s,%s\n" % \
								( member[0], member[1], PLAYER_TYPE[key], order + 1, movie_id, url) );
	except Exception, e: 
		print e.message;
		print traceback.format_exc();
		pass ; 

	return None; 

if __name__ == "__main__":

	merge_fname = "merge_out/2015/merge_000.pkl";
	actors_ofname = "flat_out/actors_detail.list";
	movie_ofname = "flat_out/movie_info.list";
	##douban_flat_movie_detail(merge_fname, actors_ofname, movie_ofname);

	if os.path.exists(actors_ofname): os.remove(actors_ofname);
	if os.path.exists(movie_ofname): os.remove(movie_ofname);

	year_list = [ 2013, 2014, 2015 ];
	for year in year_list:
		merge_path = "merge_out/%d" % year;
		merge_fname_list = os.listdir(merge_path);
		for fname in merge_fname_list:
			douban_flat_movie_detail(merge_path + "/" + fname, actors_ofname, movie_ofname);

	sys.exit(0);






