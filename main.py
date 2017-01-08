# testing

#from News import News
from Crawler import Sniffer
from preprocessing import PreProcessing
from extractor import Extractor
import os

url = "http://falkor-cda.bastian.globo.com/feeds/8351bc2f-9988-4fed-bc44-13d62a3e966f/posts/page/1/query_parameter/http://semantica.globo.com/G1/Politico_7c678a2c-2e99-4c45-b20b-76d15b9d77f8";
sniffer = Sniffer(initialUrl=url, newsLimit=20, name='dilma')
sniffer.execute()

files = os.listdir(os.path.join('database', 'dilma'))
files_list = []
for fname in os.listdir(os.path.join('database', 'dilma')):
	files_list.append(os.path.join('database', 'dilma', fname))

news_preprocessed = PreProcessing(files=files_list)

extracted_data = Extractor(data=news_preprocessed)

knowledge_base = extracted_data.extract()

knowledge_base.save("dilma_knowledge.csv")

#
# for fname in os.listdir(os.path.join('database', 'dilma')):
# 	n = News()
# 	n.loadsFromJSON(os.path.join('database', 'dilma', fname))
#
# 	if(n.text == None or len(n.text) == 0):
# 		print(n.url)
# 		print(fname)
