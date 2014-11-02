import urllib2
from stripogram import html2text

import datetime
import time

from lxml import html
import requests

import sys

def reqTree(href, site = 'http://www.sec.gov/'):
	page = requests.get(site+href)
	tree = html.fromstring(page.text)
	return tree

def formatData(period_date, risk_length, close_price, ticker, mdna):
	print " Formatting : ", period_date, risk_length, close_price, ticker, len(mdna)
	data = "<DOC>\n<DATE>{0}</DATE>\n<RISKLENGTH>{1}</RISKLENGTH>\n<PRICE>{2}</PRICE>\n<COMPANY>{3}</COMPANY>\n{4}</DOC>\n\n".format(period_date, risk_length, close_price, ticker, mdna.encode('utf-8'))
	return data

def scrape10Q(href):
	tree = reqTree(href)
	following = tree.xpath('//font[contains(@style,"font-weight:bold") and contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"discussion")]/following::* | //b[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"discussion")]//following::*')
	preceding = tree.xpath('//font[contains(@style,"font-weight:bold") and contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"quantitative")]/preceding::* | //b[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"quantitative")]//preceding::*')
	mdna = [elem for elem in following if elem in preceding]
	
	s = ''
	for t in mdna:
		if t.text != None:
			s += t.text
	return s

def scrapePrice(ticker, period_date):
	url = 'http://finance.yahoo.com/q/hp?s={0}&a={1}&b={2}&c={3}&d={1}&e={2}&f={3}&g=d'.format(
		ticker, period_date.month-1, period_date.day, period_date.year)
	page = requests.get(url)
	tree = html.fromstring(page.text)
	prices = tree.xpath('//td[@class="yfnc_tabledata1"][@align="right"]/text()')
	if len(prices) > 4:
		close_price = prices[4]
		return close_price
	else:
		new_date = period_date - datetime.timedelta(days=1)
		return scrapePrice(ticker, new_date)

def scrapeDocs(href, ticker):
	tree = reqTree(href)
	
	period_date = tree.xpath('//div[div[@class="infoHead"]="Period of Report"]/div[@class="info"]/text()')[0]
	period_date = datetime.datetime.strptime(period_date, '%Y-%m-%d').date()
	close_price = scrapePrice(ticker, period_date)

	rows = tree.xpath('//tr')
	for row in rows:
		if '10-Q' in row.xpath('td[@scope="row"]/text()'):
			href = row.xpath('td[@scope="row"]/a/@href')
			mdna = scrape10Q(href[0])
			break

	if len(mdna) < 50:
		return (5,4) # Throw an error to end it
	else:
		return formatData(period_date, len(mdna.split()), close_price, ticker, mdna)

def scrapeSearch(ticker):
	url = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type=&dateb=&owner=exclude&start={1}&count=100'
	count = 0
	not_last = True
	s = ''

	while not_last:
		page = requests.get(url.format(ticker, count))
		tree = html.fromstring(page.text)

		titles = tree.xpath('//td[@nowrap="nowrap"]/text()')
		links = tree.xpath('//td[@nowrap="nowrap"]/a/@href')
		
		for idx,title in enumerate(titles):
			if '10-Q' in title:
				try:
					s += scrapeDocs(links[idx], ticker)
				except:
					print "Failed: ", ticker, count
					time.sleep(2.0)
					return s

		next_button = tree.xpath('//input[@type="button"][@value="Next 100"]')
		if len(next_button) == 0:
			not_last = False
		else:
			count += 100

	return s

def scrapeData(tickers):
	s = ''
	for ticker in tickers:
		try:
			s += scrapeSearch(ticker)
		except:
			print "Failed on:", ticker
			time.sleep(2.0)
			pass

	f = open('training_set.data','w')
	f.write(s)
	f.close()

if __name__ == '__main__':
	start = datetime.datetime.now()
	tickers = ['AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD',
		'IBM','INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE',
		'PG','T','TRV','UNH','UTX','V','VZ','WMT','XOM']
	scrapeData(tickers)
	print "Exec time: ", datetime.datetime.now() - start

