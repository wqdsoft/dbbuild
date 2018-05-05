# dbbuild

dbbuild is database script generating tool for the mybatis project.

dbbuild 是一个mybatis项目数据库脚本生成工具，通过读取mybatis的mapper文件，分析出绝大部分数据库名称与相应的字段。

# 开发目的
本脚本是python2.7编写，目的是让那些丢失了数据库的mybatis项目起死回生，免得要一个个字段手工创建。

# 使用方法

python dbbuild.py mybatis_mapper_xml_full_path

mybatis_mapper_xml_full_path 是指代码所在文件夹的绝对路径。

