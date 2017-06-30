#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import print_function
from time import sleep
from collections import defaultdict
import argparse
import os
import re
import sys
import time
import io
import bisect
import codecs
import cPickle

def to_lower_case(bio_tag):
	if bio_tag == 'B':
		return 'b'
	elif bio_tag == 'O':
		return 'o'
	elif bio_tag == u'Ī':
		return u'ī'
	elif bio_tag == u'Ĩ':
		return u'ĩ'
	elif bio_tag == u'Î':
		return u'î'
	else:
		return bio_tag

def to_upper_case(bio_tag):
	if bio_tag == 'b':
		return 'B'
	elif bio_tag == 'o':
		return 'O'
	elif bio_tag == u'ī':
		return u'Ī'
	elif bio_tag == u'ĩ':
		return u'Ĩ'
	elif bio_tag == u'î':
		return u'Î'
	else:
		return bio_tag


def fix_line(has_started, annotation_tag, bio_tag, prev_index, line, output_file):
	culled_bio_tag = line[4][1:]
#	if culled_bio_tag.startswith('\xa8'):
#		culled_bio_tag = culled_bio_tag.replace('\xa8','') 
#	elif culled_bio_tag.startswith('\xaa'):
#		culled_bio_tag = culled_bio_tag.replace('\xaa','')	
#	elif culled_bio_tag.startswith('\xab'):
#		culled_bio_tag = culled_bio_tag.replace('\xab','')

	#output_f = io.open(output_file, 'a')

#	print([culled_bio_tag], file = output_f)

#	print(annotation_tag, file = output_f)


	if bio_tag == 'to_original':
                pass
		#print('\t'.join(line), file = output_f)					  		
	elif not has_started:
		if not bio_tag == 'o' and not bio_tag == 'O':
			#print(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + bio_tag + culled_bio_tag + "\t" + line[5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8], file = output_f)
                        line[4] = bio_tag
		else:
                        line[4] = bio_tag
                        line[5] = "0"
                        line[6] = ""
			#print(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + bio_tag + culled_bio_tag + "\t" + "0" + "\t" + "\t" + line[7] + "\t" + line[8], file = output_f)										 
	else:
		if bio_tag == 'convert_to_lower_case':
                        line[4] = to_lower_case(line[4][0])
			#print(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + to_lower_case(line[4][0]) + culled_bio_tag + "\t" + line[5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8], file = output_f)									 
		elif bio_tag == 'convert_to_upper_case':
                        line[4] = to_upper_case(line[4][0])
			#print(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + to_upper_case(line[4][0]) + culled_bio_tag + "\t" + line[5] + "\t" + line[6] + "\t" + line[7] + "\t" + line[8], file = output_f)									 
		elif bio_tag == 'O' or bio_tag == 'o':
                        line[4] = bio_tag
                        line[5] = "0"
                        line[6] = ""
			#print(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + bio_tag + culled_bio_tag + "\t" + "0" + "\t" + "\t" + line[7] + "\t" + line[8], file = output_f)
		else:
                        line[4] = bio_tag
                        line[5] = prev_index
                        line[6] = annotation_tag
			#print(line[0] + "\t" + line[1] + "\t" + line[2] + "\t" + line[3] + "\t" + bio_tag + culled_bio_tag + "\t" + prev_index + "\t" + annotation_tag + "\t" + line[7] + "\t" + line[8], file = output_f) 

												
def process_fixes(args, streusle_file, fix_file, output_file):
        f = codecs.open(streusle_file,encoding="utf-8")
        streusle_lookup = defaultdict(list)
        order = []
        for line in f:
                if line.strip():
                        line = line.strip().split("\t")
                        line[4] = line[4][0]
                        line[7] = ""
                        streusle_lookup[line[8]].append(line)
                        if not order or order[-1] != line[8]:
                                order.append(line[8])
        f.close()
        f = open("syntax_info.dat","rb")
        pos_fixes = cPickle.load(f)
        dep_lookup = cPickle.load(f)
        f.close()
        for pos_fix in pos_fixes:
              streusle_lookup[pos_fix[0]][pos_fix[1] - 1][3] = pos_fix[2]
        for ID in dep_lookup:
                for i in range(len(streusle_lookup[ID])):
                        #print(dep_lookup[ID][0][i])
                        #print(dep_lookup[ID][1][i])
                        #print(streusle_lookup[ID][i])
                        streusle_lookup[ID][i][7] = dep_lookup[ID][0][i]
                        streusle_lookup[ID][i].append(streusle_lookup[ID][i][8])
                        streusle_lookup[ID][i][8] = dep_lookup[ID][1][i]
	f1 = codecs.open(fix_file, encoding="utf-8")
	for line in f1:
		indicies_list = []
		has_started = False
		is_in_gap = False
		prev_index = 0

		ID, mwe, indicies, start_type, end_type = line.strip().split("\t")

		if line.startswith('#'):	# skip comments
			continue
						
		indicies_list = indicies.split()
		end_type_list = end_type.split()
                streusle_lines = streusle_lookup[ID]
                for line in streusle_lines:
                        for index, item in enumerate(indicies_list):
				if str(item) == str(line[0]): # check first column (index)
					if not has_started: # if this is the first word of MWE
						if line[4][0].islower(): # check BIO, see if it is lower case, if so it is in a gap	   
							is_in_gap = True
							if end_type_list[index] == "X": # retagged as not an MWE
								fix_line(has_started, end_type_list[index-1], 'o', prev_index, line, output_file)
							elif end_type_list[index] == "^" and args['hard_as_nonMWE']: 
								fix_line(has_started, end_type_list[index-1], 'o', prev_index, line, output_file)
							elif end_type_list[index] == "^" and args['hard_as_original']:
								fix_line(has_started, end_type_list[index-1], 'to_original', prev_index, line, output_file)
							else: #tagged as an MWE
								fix_line(has_started, end_type_list[index-1], 'b', prev_index, line, output_file)
						else:	# not in a gap
							if end_type_list[index] == "X": # retagged as not an MWE
								fix_line(has_started, end_type_list[index-1], 'O', prev_index, line, output_file)
							elif end_type_list[index] == "^" and args['hard_as_nonMWE']: # retagged as not an MWE
								fix_line(has_started, end_type_list[index-1], 'O', prev_index, line, output_file)
							elif end_type_list[index] == "^" and args['hard_as_original']:
								fix_line(has_started, end_type_list[index-1], 'to_original', prev_index, line, output_file)
							else: #tagged as an MWE
								fix_line(has_started, end_type_list[index-1], 'B', prev_index, line, output_file)
						has_started = True	# special handler for first word of MWE
					else:	# every other term in the MWE
						# in gap
						if is_in_gap:					 
							if end_type_list[index-1] == "_": 
								fix_line(has_started, end_type_list[index-1], u'ī', prev_index, line, output_file)
							elif end_type_list[index-1] == "~":	   
								fix_line(has_started, end_type_list[index-1], u'ĩ', prev_index, line, output_file)
							elif end_type_list[index-1] == "^":
								if args['hard_as_original']:
									fix_line(has_started, end_type_list[index-1], 'to_original', prev_index, line, output_file)
								elif args['hard_as_nonMWE']:
									fix_line(has_started, end_type_list[index-1], 'o', prev_index, line, output_file)
								elif args['hard_as_weak']:
									fix_line(has_started, '~', u'ĩ', prev_index, line, output_file)
								else: #keep_hard
									fix_line(has_started, end_type_list[index-1], u'î', prev_index, line, output_file)
							elif end_type_list[index-1] == "X":
								fix_line(has_started, end_type_list[index-1], 'o', prev_index, line, output_file)
						# not in gap
						elif end_type_list[index-1] == "_":
							fix_line(has_started, end_type_list[index-1], u'Ī', prev_index, line, output_file)
						elif end_type_list[index-1] == "~":
							fix_line(has_started, end_type_list[index-1], u'Ĩ', prev_index, line, output_file)						
						elif end_type_list[index-1] == "^":
							if args['hard_as_original']:
								fix_line(has_started, end_type_list[index-1], 'to_original', prev_index, line, output_file)
							elif args['hard_as_nonMWE']:
                                                                if len(end_type_list) > index and end_type_list[index] != "^":
                                                                        fix_line(has_started, "", 'B', "0", line, output_file)
                                                                else:
                                                                        fix_line(has_started, end_type_list[index-1], 'O', prev_index, line, output_file)
							elif args['hard_as_weak']:
								fix_line(has_started, '~', u'Ĩ', prev_index, line, output_file)
							else: #keep_hard
								fix_line(has_started, end_type_list[index-1], u'Î', prev_index, line, output_file)
						elif end_type_list[index-1] == "X":
							fix_line(has_started, end_type_list[index-1], 'O', prev_index, line, output_file)
				prev_index = item
			if " * " in mwe:	# handle for terms within gappy MWEs
				if has_started:
					if line[0] != '':	# ignore blank line
						if int(line[0]) in range(int(indicies_list[0]), int(indicies_list[-1])):  #gappy case only, convert to o or O
							if str(line[0]) not in indicies_list:
                                                                
                                                                #print(line)
								#indicies_list = map(int, indicies_list)
								indicies_list1 = map(int, indicies_list)
								lower_indice = bisect.bisect(indicies_list1, int(line[0]))
								#print(indicies_list1)
								#print(int(line[0]))
								#print(indicies_list1[lower_indice-1])
								#print(end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])])
								if end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])] == "X":
									if line[4][0].islower():
										fix_line(has_started, end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])], 'convert_to_upper_case', prev_index, line, output_file)	# has_started = True
									else:
										fix_line(has_started, end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])], 'to_original', prev_index, line, output_file)	# has_started = True				
								elif end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])] == "^" and args['hard_as_nonMWE']: 
									if line[4][0].islower():
										fix_line(has_started, end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])], 'convert_to_upper_case', prev_index, line, output_file)	# has_started = True
									else:
										fix_line(has_started, end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])], 'to_original', prev_index, line, output_file)	# has_started = True				
								elif end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])] == "^" and args['hard_as_original']: 
									fix_line(has_started, end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])], 'to_original', prev_index, line, output_file)
								else:
									fix_line(has_started, end_type_list[indicies_list1.index(indicies_list1[lower_indice-1])], 'convert_to_lower_case', prev_index, line, output_file)	# has_started = True
								#print(line)						

        f1.close()
        fout = codecs.open(output_file,"w",encoding="utf-8")
        first = True
        for ID in order:
                if first:
                        first = False
                else:
                        fout.write("\n")
                for line in streusle_lookup[ID]:
                        #print(line)
                        fout.write("\t".join(line) + "\n")
        fout.close()
                
                
							
def remove_file(file_name):
	try:
		os.remove(file_name)
	except OSError:
		pass
    
if __name__=='__main__':

	start_time = time.time()

	parser = argparse.ArgumentParser(description='Apply annotation fixes to the STREUSLE 3.0 .tag file.')

	parser.add_argument('streusle_file', help='STREUSLE 3.0 .tag file')
	parser.add_argument('output_file', help='HAMSTERIZED STREUSLE .tag filename.')
	
	group1 = parser.add_mutually_exclusive_group(required=True)
	
	group1.add_argument('--hard_as_hard', action='store_true', 
							help='Hard cases have a special hard tag.')
	group1.add_argument('--hard_as_nonMWE', action='store_true', 
							help='Hard cases are considered non-MWEs.')
	group1.add_argument('--hard_as_weak', action='store_true', 
							help='Hard cases are considered weak MWES.')
	group1.add_argument('--hard_as_original', action='store_true', 
							help='Hard cases revert to original annotation, no change.')
	args = vars(parser.parse_args())

	remove_file(args['output_file'])

	sys.stdout.write("Processing...")
	sys.stdout.flush()

	process_fixes(args, args['streusle_file'], "MWE_fixes.txt",args['output_file'])
	sys.stdout.write("Complete")
	sys.stdout.flush()
