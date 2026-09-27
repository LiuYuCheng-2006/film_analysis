import requests
from lxml import html
target_url="https://tiobe.com/tiobe-index/"
response=requests.get(target_url)
print(response.text)
document=html.fromstring(response.text)
th_list=document.xpath("//*[@id='top20']/thead/tr/th/text()")


print(th_list)
tr_list=document.xpath("//table[@id='top20']/tbody/tr")
for tr in tr_list:
    td_list=tr.xpath("./td/text()")
    print(td_list)
