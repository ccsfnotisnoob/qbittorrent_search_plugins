#VERSION: 0.6
#AUTHORS: hoanns
# getigg.js needs to be in nova2.py folder
# doesnt work with qbit tho, only made to use with nova2.py
# python 3 only
# phantomjs needs to be installed and in path

import re
import subprocess
import base64

from novaprinter import prettyPrinter
from helpers import retrieve_url


# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
# headers = {'User-Agent': user_agent}


# noinspection PyPep8Naming
class warezgames(object):
    url = "http://www.warezgames.com/"
    name = "WarezGames"

    def search(self, what, cat='all'):
        what = what.lower()

        process = subprocess.Popen(['phantomjs.exe', 'getigg.js', what], stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        igg_data = out.decode('utf-8')
        igg_match = re.compile('<a\shref="(.*?)"\s.*?rel="bookmark".*?>(.*?)</a>')
        igg_results = re.findall(igg_match, igg_data)

        csrin_query = "https://cs.rin.ru/forum/search.php?keywords=" + what + "&terms=all&author=&sc=1&sf=titleonly&sk=t&sd=d&sr=topics&st=0&ch=300&t=0"
        csrin_data = retrieve_url(csrin_query)
        csrin_match = re.compile('<a\shref="(.*?)"\sclass="topictitle".*>(.*?)</a>')
        cs_results = re.findall(csrin_match, csrin_data)

        skid_query = "https://skidrowreloadedcodex.org/?s=" + what.replace(' ', '+')
        skid_data = retrieve_url(skid_query)
        skid_match = re.compile('<h1\sclass="title"><a\shref="(.*?)"\stitle="(.*?)">')
        skid_results = re.findall(skid_match, skid_data)

        for i in igg_results:
            self.printName(i[1] + " [IGG]", i[0])
        for i in cs_results:
            self.printName(i[1] + " [cs_rin]", "https://cs.rin.ru/forum" + i[0][1:])
        for i in skid_results:
            self.printName(i[1] + " [SkidrowReloadedCodex]", i[0], self.getSkidDl(i[0]))

    def printName(self, name, desc_link, link=None):
        link = link or desc_link
        prettyPrinter({
            'name': name.strip(),
            'size': -1,
            'link': link,
            'desc_link': desc_link,
            'seeds': -1,
            'leech': -1,
            'engine_url': self.url
        })

    # store dl links somewhere, not useful for qbit searching
    def getSkidDl(self, link):
        try:
            skid_dl_match = re.compile('<div style="text-align: center;"> <p><strong>MIRROR.*?</div><p>')
            skid_data = retrieve_url(link)
            return base64.b64encode(re.findall(skid_dl_match, skid_data)[0])
        except:
            return None


if __name__ == "__main__":
    engine = warezgames()
    engine.search('isaac')
