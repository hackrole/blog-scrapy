#coding=utf-8

import sqlite3
import sys,traceback,time
import random

class BlogSaveHelps:
    """
    用于保存抓取博客的帮助类，主要用于将逻辑从pipe中抽离。更好的用于后续扩展
    """
    
    def __init__(self, db="/var/www/blog/sql/main.db"):
        self.db = db
        self.conn = sqlite3.connect(db)

    def saveCate(name, create_time=time.strftime("%Y-%m-%d"), desc="", category_pv=0):
        sql = 'insert into webblog_category (name,create_time, desc, category_pv) values (?, ?, ?, ?)'
        self.conn.execute(sql, (name, create_time, desc, category_pv))
        self.conn.commit()

    def saveTag(tag_name, desc="", create_time=time.strftime("%Y-%m-%d"), tag_pv=0):
         sql = 'insert into webblog_tag (tag_name, desc, create_time, tag_pv) values (?, ?, ?, ?)'
         self.conn.execute(sql, (tag_name, desc, create_time, tag_pv))
         self.conn.commit()
    
    def saveBlog(item):
        """
        先根据cate查询分类id,差不多则取随机值，
        然后插入blog信息，之后根据需要完成comments和tag的插入
        """
        r = random()
        # cate 处理
        catesql = "select category_id from webblog_category where name like ?" 
        cate = self.conn.execute(catesql, ('%'+item['cate']+'%',)).fetchall()
        if len(cate) >= 1:
            cate_id = cate[0][0]
        else:
            catesql = "select count(*) from webblog_category"
            cate = self.conn.execute(catesql)
            cate_id = r.randint(1, cate[0][0]) # 随机处理
          
        # blog 处理
        blogsql = "insert into blog (category_id, title, content, pub_time, blog_pv, is_closed) values (?,?,?,?,?,?)"
        blog = self.conn.execute(blogsql,(cate_id, item['title'], item['blog'], time.strftime('%Y-%m-%d'), 0, 0))
        self.conn.commit()

        # 评论与tag处理
        blog_id = blog.lastrowid
        if len(item['comments']) > 0:
            for comment in item['comments']:
                commentsql = "insert into webblog_comment (author_name, author_email, content, is_close, blog_id, comment_up) values (?, ?, ?, ?, ?, ?)"
                self.conn.execute(commentsql, ('shell', 'shell909090@gmail.com', comment, 0, blog_id, 0))
                self.conn.commit()

        tagsql1 = "select tag_id from webblog_tag where tag_name like ?"
        if len(item['tag']) >= 1:
            tag = item['tag'][0]
            tag = self.conn.execute(tagsql1, ('%'+tag+'%',)).fetchall()
            if len(tag) >= 1:
                tag_id = tag[0][0]
            else:
                tag_id = r.randint(1, 10) # 随机处理
                tagsql2 = "insert into webblog_tag_blog (tag_id, blog_id) values (?, ?)"
                self.conn.execute(tagsql2, (tag_id, blog_id))
                self.conn.commit()

