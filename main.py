# Execute this using Python 2.7

from Crawler import Sniffer
from preprocessing import PreProcessing
from extractor import Extractor
import os
import sys

# if the word 'crawler' is passed as parameter so the news and new news will be collected.
# otherwise just the natural language processing will be made.
if('crawler' in sys.argv):
	url = "http://falkor-cda.bastian.globo.com/feeds/8351bc2f-9988-4fed-bc44-13d62a3e966f/posts/page/1/query_parameter/http://semantica.globo.com/G1/Politico_7c678a2c-2e99-4c45-b20b-76d15b9d77f8";
	sniffer = Sniffer(initialUrl=url, newsLimit=1000, name='dilma')
	sniffer.execute()

# This create a list of filenames of the news
files = os.listdir(os.path.join('database', 'dilma'))
files_list = []
for fname in os.listdir(os.path.join('database', 'dilma')):
	files_list.append(os.path.join('database', 'dilma', fname))

# This realize the natural language processing and save in a csv
# One file to entities and other to relationships
news_preprocessed = PreProcessing(files=files_list)
# Create a instance of Extractor to get entities and relations from the news
extracted_data = Extractor(data=news_preprocessed.data, main_entity='dilma')
knowledge_base = extracted_data.extract()
# Use the KnoledgeBase instance to save result at knowledge_base/dilma_knowledge
knowledge_base.save("dilma_knowledge")
