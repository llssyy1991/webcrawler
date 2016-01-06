from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from pymongo import MongoClient
import re

client = MongoClient()
db = client.test
seeds=[]
virusname=[]


#bloomfilter has be set as 262144 as 8^6
bloomfilter=[0]*262144

BrowserObj_dirver = webdriver.Chrome()
BrowserObj_dirver.implicitly_wait(20)
paratition=[0,12,24,34,44,54]

#bloomcheck is function for bloomfilter

def bloomcheck(hash):
	positions=[]
	hashnum=0
	r_value=1
	while hashnum<6:
		result=0
		itertime=0
		while itertime<6:
			if itertime>=2 and hashnum==5:
				hex=hash[paratition[itertime]:(paratition[itertime]+2)]
				try:
					result=result*8+int(hex,16)%8
				except ValueError:
					print "value error"
				itertime=itertime+1
				continue
			start=paratition[itertime]+hashnum*2
			end=paratition[itertime]+hashnum*2+2
			hex=hash[start:end]
			print hex
			try:
				result=result*8+int(hex,16)%8
			except ValueError:
				print "value error"
			itertime=itertime+1
		hashnum=hashnum+1
		positions.append(result)
	for position in positions:
		if bloomfilter[position]==1:
			continue
		bloomfilter[position]=1
		r_value=0
	if r_value==1:
		return False
	return True

# function get_infor is used to collect useful information from url given, whenever a new seed need to be inserted,bloom-filter query need to be applied 

def get_infor(url):
	global virusId

	BrowserObj_dirver.get(url)

	try:
		InputObj_search = BrowserObj_dirver.find_element_by_id('antivirus-results')

		body=InputObj_search.find_elements_by_tag_name('tbody')

		data1=body[0].find_elements_by_css_selector('.ltr.text-red')
		companyname=body[0].find_elements_by_xpath('//*[@id="antivirus-results"]/tbody/tr/td[1]')
	except NoSuchElementException:

		print "no page"

		return

	datalen=len(data1)
	companylen=len(companyname)
	info={}
	count=0

	while count<datalen:
		info[companyname[count].text]=data1[count].text
		if len(virusname)<100:
			virusname.append(data1[count].text)
		count=count+1
	while count<companylen:
		info[companyname[count].text]="null"
		count=count+1
	print info

	sha=BrowserObj_dirver.find_element_by_xpath("//table[@style='margin-bottom:8px;margin-left:8px;']/tbody/tr/td[2]")


	Vdata={"sha-256" : sha.text,"result" : info }
	result=db.hashdata.insert_one(Vdata)

	try:
		BrowserObj_dirver.implicitly_wait(10)
		BrowserObj_dirver.find_element_by_xpath("//li[@id='tab-item-relationships']/a").click()

		print "here"


		test=BrowserObj_dirver.find_elements_by_xpath("//div[@class='enum']/a")

		for t in test:
			if bloomcheck(t.text):
				seeds.append(t.get_attribute("href"))


	except NoSuchElementException:

		print "no relative"
	except ElementNotVisibleException:
		print "no visible"






	#BrowserObj_dirver.close()


get_infor("https://www.virustotal.com/en/file/f6239ba0487ffcf4d09255dba781440d2600d3c509e66018e6a5724912df34a9/analysis/")

while 1:
	if not seeds:
        	for name in virusname:
            		BrowserObj_dirver.get("http://www.google.com")
	        	InputObj_search = BrowserObj_dirver.find_element_by_id('lst-ib')
	        	search="virustotal "+name
	        	InputObj_search.send_keys(search)
	        	InputObj_search.send_keys(Keys.RETURN)
	        	BrowserObj_dirver.implicitly_wait(20)
	        	link=BrowserObj_dirver.find_elements_by_xpath("//a[text()='Antivirus scan for ... - VirusTotal']")
        		for li in link:
            			matchObj = re.search( r'[^/]{60,}', li.get_attribute("href"), re.M|re.I)
				try:
					print matchObj.group()
            				if bloomcheck(matchObj.group()):
						seeds.append(li.get_attribute("href"))
				except AttributeError:
					print "attribute"
				print seeds
		del virusname[:]
	print seeds[0]
	get_infor(seeds[0])
			
		
	
	
	
	del seeds[0]


