index_sub = ["0","1","2","3","4","5","6","7","8","9"]
import re
import os
import threading

def downpapers(href,a,b,c,d):
    os.system("wget \"https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed25n"+a+b+c+d+".xml.gz")  # https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed25n0001.xml.gz
    return 1

get_href=re.compile(r'href="(.*?)"')  # href="10.1177_23259671241228316.PMC10880532.pdf">
base_dir="/data1/liubo_data/Paper_down/pubmed"

for a in index_sub:
    for b in index_sub:
        for c in index_sub:
            for d in index_sub:
                if not os.path.exists("pubmed25n"+a+b+c+d+".xml.gz"):
                    os.system("wget \"https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed25n"+a+b+c+d+".xml.gz\" -O pubmed25n"+a+b+c+d+".xml.gz")

