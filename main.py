# testing

from News import News
from Crawler import Sniffer
import os

url = "http://falkor-cda.bastian.globo.com/feeds/8351bc2f-9988-4fed-bc44-13d62a3e966f/posts/page/1/query_parameter/http://semantica.globo.com/G1/Politico_7c678a2c-2e99-4c45-b20b-76d15b9d77f8";
sniffer = Sniffer(initialUrl=url, newsLimit=100, name='dilma')
sniffer.execute()

for fname in os.listdir(os.path.join('database', 'dilma')):
	n = News()
	n.loadsFromJSON(os.path.join('database', 'dilma', fname))

	if(n.text == None or len(n.text) == 0):
		print(n.url)
		print(fname)
