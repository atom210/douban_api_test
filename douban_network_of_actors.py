#!/usr/bin/python2.7
# -*- coding=utf-8 -*-

# ======================================================================================
# File		 : douban_network_of_actors.py
# Author	   : zhanggongyuan 
# Last Change  : 04/27/2016 | 17:41:42 PM | Wednesday,April
# Description  : 
# ======================================================================================

import sys, os, pickle;
import hashlib; 

fake_base_actorid = (30 * 1000 * 1000);
fake_count = 0;

fake_actorid_dict = dict();	 ## actor_name -> fake_actorid
actors_name_dict = dict();	  ## actor_id -> actor_name
collabrate_dict = dict();	   ## (actorA, actorB) -> weights

def key_of_edge_dict(actid1, actid2):
	##lhs_id = actid1 < actid2 ? actid1 : actid2;
	##rhs_id = actid1 > actid2 ? actid1 : actid2;
	lhs_id = actid1 if actid1 < actid2 else actid2;
	rhs_id = actid1 if actid1 > actid2 else actid2;
	return (lhs_id, rhs_id);

def update_key_weight(key, level):
	if not collabrate_dict.has_key(key):
		collabrate_dict[key] = float(0.0);
	collabrate_dict[key] += float(1.0) / (4 * (level - 1) + 1)
	pass ; 

def dump_node_dict(node_dict, out_fname):
	with open(out_fname, "w+") as out_file:
		for key, value in node_dict.items():
			out_file.write("%d,%s\n" % (key, value));
	pass ; 

def dump_edge_dict(edge_dict, out_fname):
	with open(out_fname, "w+") as out_file:
		for key, value in edge_dict.items():
			lhs_name = actors_name_dict[key[0]];
			rhs_name = actors_name_dict[key[1]];
			out_file.write("%s,%s,%.4f\n" % (lhs_name, rhs_name, value));
	pass ; 

# ======================================================== 
# generate collabrate weighted-network between actors 
# ======================================================== 
def douban_network_of_actors(merge_fname):
	global fake_count; global fake_base_actorid;
	with open(merge_fname, "r") as merge_file:
		merge_info_list = pickle.load(merge_file);
		for merge_info in merge_info_list:
			if not merge_info.has_key("subtype") or merge_info["subtype"] != "movie" : continue;
			if merge_info.has_key("countries"):
				country_desc = "/".join(merge_info["countries"]);
				if -1 == country_desc.find("中国"): continue;

			if not merge_info.has_key("actors"): continue;
			actors_list = merge_info["actors"];
			if len(actors_list) < 6 : continue;
			actors_list = actors_list[0:6];

			## fixed actorid -> actorname 
			for idx, actor in enumerate(actors_list):
				actid = actor[0]; actname = actor[1];
				if not actid.isdigit():
					fake_key = hashlib.md5(actor[1]).hexdigest();
					if not fake_actorid_dict.has_key(fake_key):
						fake_actorid_dict[fake_key] = str(fake_base_actorid + fake_count);
						fake_count += 1;
					actid = fake_actorid_dict[fake_key];
					actors_list[idx] = (actid, actname);

			for actor in actors_list:
				actors_name_dict[int(actor[0])] = actor[1];

			## generate edges
			a = int(actors_list[0][0]); b = int(actors_list[1][0]); ## level 1
			c = int(actors_list[2][0]); d = int(actors_list[3][0]); ## level 2
			e = int(actors_list[4][0]); f = int(actors_list[5][0]); ## level 3

			tmp_key = key_of_edge_dict(a, b); update_key_weight(tmp_key, 1); ## level 1 edge weight 1.0

			tmp_key = key_of_edge_dict(a, c); update_key_weight(tmp_key, 2); ## level 2 edge weight 1.0 / 4
			tmp_key = key_of_edge_dict(b, c); update_key_weight(tmp_key, 2); ## level 2 edge weight 1.0 / 4
			tmp_key = key_of_edge_dict(a, d); update_key_weight(tmp_key, 2); ## level 2 edge weight 1.0 / 4
			tmp_key = key_of_edge_dict(b, d); update_key_weight(tmp_key, 2); ## level 2 edge weight 1.0 / 4
			tmp_key = key_of_edge_dict(c, d); update_key_weight(tmp_key, 2); ## level 2 edge weight 1.0 / 4

			tmp_key = key_of_edge_dict(a, e); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(b, e); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(c, e); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(d, e); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(a, f); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(b, f); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(c, f); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(d, f); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
			tmp_key = key_of_edge_dict(e, f); update_key_weight(tmp_key, 3); ## level 2 edge weight 1.0 / 9
	pass ; 

if __name__ == "__main__":

	year_list = [ 2013, 2014, 2015 ];
	for year in year_list:
		merge_path = "merge_out/%d" % year;
		merge_fname_list = os.listdir(merge_path);
		##for fname in merge_fname_list[0:1]:
		for fname in merge_fname_list:
			douban_network_of_actors(merge_path + "/" + fname);

	dump_node_dict(actors_name_dict, "flat_out/node.list");
	dump_edge_dict(collabrate_dict, "flat_out/edges.list");

	sys.exit(0);




