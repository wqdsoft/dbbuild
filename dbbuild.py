# -*- coding: utf-8 -*-  
import os
import sys
import xml.dom.minidom
import re

# use 

def camelToUnderlines(x):  
    return re.sub('_([a-z])', lambda match: match.group(1).upper(), x).lower()
  
  
def underlinesToCamel(x):  
    return re.sub('([a-zA-Z])([A-Z])', lambda match: match.group(1).lower() + "_" + match.group(2).lower(), x).lower()
  


def getDatabaseType(var):
    return {
            'BIGINT': 'BIGINT(10)',
            'TINYINT': 'INT(2)',
            'VARCHAR': 'VARCHAR(255)',
            'TIMESTAMP':'TIMESTAMP',
            'INTEGER':'INT(10)',
            'BIT':'INT(2)',
            'LONGVARCHAR':'TEXT'
    }.get(var,'VARCHAR(255)')    #'error'为默认返回值，可自设置

def useage():
	print("dbbuild.py:  a database script generating tool for the mybatis project.")
	print("designer: rockguo guoxin@wqdsoft.com")
	print("useage:   python dbbuild.py mybatis_mapper_xml_full_path ")



def main():
	if len(sys.argv)<=1 :
		useage()
		quit()

	path = sys.argv[1] #文件夹目录
	if(not os.path.exists(path)):
		print("error:path not exists.")
		quit()

	files= os.listdir(path) #得到文件夹下的所有文件名称
	dbString= ""
	for file in files: #遍历文件夹
	     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开

			#打开xml文档
			dom = xml.dom.minidom.parse(path+"/"+file)
			#得到文档元素对象
			root = dom.documentElement
			bb = root.getElementsByTagName('resultMap')
			tableName=""
			
			for i,b in enumerate(bb):
				tableName=underlinesToCamel(b.getAttribute("type").split('.')[-1])
				print("ADD TO TABLE:"+tableName) 
				if(bb[0]==b ):
					dbString=dbString+" DROP TABLE IF EXISTS `"+tableName+"`;\n";
					dbString=dbString+" CREATE TABLE `"+tableName+"` (\n"
				
				rr=b.getElementsByTagName("result")
				for i2,r in enumerate(rr):
					#print r.getAttribute("column")
					#print getDatabaseType(r.getAttribute("jdbcType"))
					if (rr[0]==r and bb[0]==b):
						dbString=dbString+" `id` BIGINT(10) PRIMARY KEY AUTO_INCREMENT,\n"
						dbString=dbString+" `"+r.getAttribute("column")+"` "+getDatabaseType(r.getAttribute("jdbcType"))+",\n"
					elif(i2 == len(rr) - 1 and (len(bb)-1==i)):
						dbString=dbString+" `"+r.getAttribute("column")+"` "+getDatabaseType(r.getAttribute("jdbcType"))+"\n"
					else :
						dbString=dbString+" `"+r.getAttribute("column")+"` "+getDatabaseType(r.getAttribute("jdbcType"))+",\n"

			dbString=dbString+") ENGINE=InnoDB DEFAULT CHARSET=utf8;\n"

	filename = 'db_struct.sql'
	with open(filename,'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
	    f.write(dbString)



if __name__ == '__main__':
	main()