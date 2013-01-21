cate="shellcate"
tag="shelltag"
blog="shellblog"
dir="${cate} ${tag} ${blog}"
all: 
	if [ ! -d "./log" ]
	then
		mkdir log
	fi
	
	for i in ${dir}
	do
		crawl --output=./log/all.log ${i}
	done
	

cate: 
	crawl --output=./log/cate.log ${cate}
	
tag:
	crawl --output=./log/tag.log ${tag}
	
blog:
	crawl --ouput=./log/blog.log ${blog}

sqlclear:
	sqlite3 ${sql} << EOF
	BEGIN;
	delete from "webblog_contact";
	delete from "webblog_about";
	delete from "webblog_comment";
	delete from "webblog_tag";
	delete from "webblog_tag_blog";
	delete from "blog";
	delete from "webblog_category";
	COMMIT;
	EOF
