#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

import os, sys
from pyquery import PyQuery as pyq

def movie_links_range(year, index):
	base_url="https://movie.douban.com/tag";
	resource_url = "%s/%d?start=%d&type=T" %(base_url, year, index);
	rtree = pyq(url=resource_url);
	print resource_url;
	items = rtree('.nbg');
	rst_list = [];
	##for idx in range(len(items)):
	for idx in range(1):
		link = items.eq(idx).attr('href');
		title = items.eq(idx).attr('title').encode("UTF-8");
		rst_list.append((link, title))
		pass ; 

##	actors_list = [];
##	items = rtree('.item');
##	##print items;
##	for idx in range(len(items)):
##		actors = items.eq(idx)('td')[1].find_class('pl')[0].text_content().encode("utf-8");
##		si = actors.rfind(") /");
##		if -1 != si:
##			actors = actors[si+3:];
##		actors_list.append(actors);

	movie_detail_list = [];
	for item in rst_list:
		movie_detail = get_movie_detail_by_link(item[0]);
		movie_detail_list.append(movie_detail);
		pass ;

	return rst_list, movie_detail_list; 

def get_movie_detail_by_link(link):
	movie_detail = dict();
	movie_page = pyq(url=link);
	info = movie_page('#info');
	slist = info('span');
	if len(slist) == 0:
		return None;
	## parse movie detail info
	idx = 0;
	while idx < len(slist):
		item = slist[idx];
		## fetch director list 
		if item.get("class") == "pl" and item.text_content() == u"导演":
			director_item = slist[idx + 1];
			children = director_item.getchildren();
			detail_info = [];
			for child in children:
				person_name = child.text_content().encode("utf-8");
				person_refid = child.get("href").split('/')[-2];
				detail_info.append( (person_refid, person_name) );
				pass ; 
			movie_detail["directors"] = detail_info;
			idx += 1;

		## fetch scriptwriter list 
		if item.get("class") == "pl" and item.text_content() == u"编剧":
			script_writers_item = slist[idx + 1];
			children = script_writers_item.getchildren();
			detail_info = [];
			for child in children:
				person_name = child.text_content().encode("utf-8");
				person_refid = child.get("href").split('/')[-2];
				detail_info.append( (person_refid, person_name) );
				pass ; 
			movie_detail["script_writers"] = detail_info;
			idx += 1;

		## fetch actor list 
		if item.get("class") == "pl" and item.text_content() == u"主演":
			actors_item = slist[idx + 1];
			children = actors_item.getchildren();
			detail_info = [];
			for child in children:
				person_name = child.text_content().encode("utf-8");
				person_refid = child.get("href").split('/')[-2];
				detail_info.append( (person_refid, person_name) );
				pass ; 
			movie_detail["actors"] = detail_info;
			idx += 1;
		
		## fetch movie type 
		if item.get("property") == "v:genre":
			if not movie_detail.has_key("movie_type"):
				movie_detail["movie_type"] = [];
			movie_detail["movie_type"].append(item.text_content().encode("utf-8"));

		idx += 1;
		pass; ## slist

	return movie_detail;

if __name__ == "__main__":

	movie_list, movie_detail_list = movie_links_range(2015, 10);
	for idx, item in enumerate(movie_list):
		directors = movie_detail_list[idx]["directors"];
		scriptwriters = movie_detail_list[idx]["script_writers"];
		actors = movie_detail_list[idx]["actors"];
		mtypes = movie_detail_list[idx]["movie_type"];
		detail_info = "[ director : %s ; scriptwriter : %s ; actors : %s, %s ; movie_type : %s ]" % \
				(directors[0][1], scriptwriters[0][1], actors[0][1], actors[1][1], mtypes[0]);
		sys.stdout.write("url: %s\ttitle: %s\ndetails: %s\n" % (item[0], item[1], detail_info));

		pass ; ## enumerate(movie_list)

	sys.exit(0);


