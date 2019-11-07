#!/usr/bin/env python3

#coding: utf-8

import os
import re
import sys
import subprocess
from optparse import OptionParser


def report_bib_list():

	biblist = open('report-biblist.txt.asc','w', encoding='utf-8')

	for m in MATCHES:
		#m = re.sub('\(|\)', '', m)
		biblist.write(m[1:] + '\n')

	biblist.close()


def get_author_year_pairs(matchlist):
	author_pattern = re.compile('(^[^,]+),[^\d]+(\d\d\d\d)')
	acc = []
	for m in matchlist:
		matches = author_pattern.match(m) 
		acc.append((matches.group(1)[1:], matches.group(2)))

	return acc

def check_bib_in_text(author, year):
	pattern = re.compile(author + '\D*' + year)
	return pattern.findall(TEXT)

def check_text_in_bib(authoryearlist):
	instream = open('report-biblist.txt.asc', 'r', encoding='utf-8')
	biblist = instream.readlines()
	instream.close()

	outstream = open('report-text2bib.txt.asc', 'w', encoding='utf-8')

	for ay in authoryearlist:
		author, year =  ay
		outstream.write(' '.join(author) + ' ' + year + '\n')
		for b in biblist:
			b = b.strip()
			if b.startswith(author[0].strip()) and (b.endswith(year+'.') or b.endswith(year)):
				outstream.write('\t' + b + '\n')
		
	outstream.close()

def get_intext_citations():
	citation_pattern = re.compile('([a-z]+ |\(|; ?|. |	|\n)(([#A-ZÖÇÜŞİ][^. ]+,? |and |& )+\(?\d\d\d\d\)?)')
	intext_citations = [x[1] for x in citation_pattern.findall(TEXT)]
	
	return uniq(intext_citations)

def report_text_to_bib():
	outstream = open('report-intext-citations.txt.asc', 'w', encoding='utf-8')

	intext_citations = get_intext_citations()

	for c in intext_citations:
		outstream.write(c + '\n')
	
	outstream.close()

	subprocess.run([EDITOR + ' report-intext-citations.txt.asc'], shell=True)

	instream = open('report-intext-citations.txt.asc', 'r', encoding='utf-8')

	author_year_list = []
	lines = instream.readlines()
	instream.close()

	for l in lines:
		stripped = re.sub('\(|\)|,|\n', '', l)
		stripped = re.sub(' and ', ' ', stripped)
		stripped = re.sub(' +', ' ', stripped)
		broken = stripped.split(' ')
		authors = broken[:-1]
		year = broken[-1]
		author_year_list.append((authors,year))
	
	author_year_list = uniq(author_year_list)
	check_text_in_bib(author_year_list)


def report_bib_to_text():
	outstream = open('report-bib2text.txt.asc', 'w', encoding = 'utf-8')

	for a, y in get_author_year_pairs(MATCHES):
		outstream.write(a + ' ' + y + ':\n')
		citations = check_bib_in_text(a, y)

		for c in citations:
			outstream.write('\t' + c + '\n')

	outstream.close()


def uniq(lst):
	store = []
	for x in lst:
		if not x in store:
			store.append(x)
	return store

def exit():
	subprocess.run(['ascii2tr.sh', 'report-intext-citations.txt.asc']) 
	subprocess.run(['ascii2tr.sh', 'report-bib2text.txt.asc'])
	subprocess.run(['ascii2tr.sh', 'report-biblist.txt.asc'])
	subprocess.run(['ascii2tr.sh', 'report-text2bib.txt.asc'])
	subprocess.Popen('rm *.asc', shell=True)
	LOGFILE.close()


if __name__ == '__main__':

	clparser = OptionParser()
	clparser.usage="%prog [options] input-file"
	clparser.add_option('-e', dest='editor', default='vim', help='editor to perform intermediary corrections.')
	clparser.add_option('-b', dest='bibname', default='references', help='title of the end-text references section -- case insensitive')
	opts, args = clparser.parse_args()

	subprocess.check_output(['tr2ascii.sh', args[0]])

	LOGFILE = open('log.txt', 'w', encoding='utf-8')
	EDITOR = opts.editor
	BIBNAME = opts.bibname

	f = open(args[0]+'.asc', 'r', encoding='utf-8')
	TEXT = f.read()
	TEXT = TEXT.replace("\u00A0", " ")


	bib_pattern = re.compile('\n[^ \n]+, \D*[^.]+. +\d\d\d\d.')
	MATCHES = bib_pattern.findall(TEXT[TEXT.lower().find(BIBNAME):])
	
	report_bib_list()
	report_bib_to_text()
	report_text_to_bib()
	exit()
