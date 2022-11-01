# This file contains the class database that handles the transactions with the mysql database

import mysql.connector


class Database:
    """This class handles the transactions with the mysql database"""
    def __init__(self):
        self.host = "localhost" # database host
        self.user = "root" # database user
        self.password = "" # database password
        self.database = "webpage_info" # database name
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.mycursor = self.db.cursor()
        
    def insert_images(self, src, alt, page_title, page_url):
        try:
            sql = "INSERT INTO images (src, alt, page_title, page_url) VALUES (%s, %s, %s, %s)"
            val = (src, alt, page_title, page_url)
            self.mycursor.execute(sql, val)
            self.db.commit()
            print(self.mycursor.rowcount, "record inserted.")
        except mysql.connector.errors.IntegrityError as err:
            pass
        
    def insert_metadata(self, title, meta_description, og_description, og_image, og_url, og_site_name):
        sql = "INSERT INTO metadata (title, description, og_description, og_image, og_url, og_site_name) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (title, meta_description, og_description, og_image, og_url, og_site_name)
        self.mycursor.execute(sql, val)
        self.db.commit()
        print(self.mycursor.rowcount, "record inserted.")
    
    def insert_body_content(self, url_id, title, paragraphs, spans, headings, lists):
        sql = "INSERT INTO website_content (url_id, title, paragraphs, span, headings, lists) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (url_id, title, paragraphs, spans, headings, lists)
        self.mycursor.execute(sql, val)
        self.db.commit()
        print(self.mycursor.rowcount, "record inserted.")
        
    def insert_links(self, url, visited):
        try:
            sql = "INSERT INTO urls (url, is_indexed) VALUES (%s, %s)"
            val = (url, visited)
            self.mycursor.execute(sql, val)
            self.db.commit()
            print(self.mycursor.rowcount, "record inserted.")
        except mysql.connector.errors.IntegrityError:
            pass
    
    def update_link_status(self, url, visited):
        sql = "UPDATE `urls` SET `is_indexed` = %s WHERE `urls`.`id` = %s;"
        val = (visited, self.get_url_id(url))
        self.mycursor.execute(sql, val)
        self.db.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        
    def get_unvisited_links(self):
        sql = "SELECT url FROM urls WHERE is_indexed = 0"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        # return the list of unvisited urls
        return myresult
    
    def get_url_id(self, url):
        sql = "SELECT id FROM urls WHERE url = %s"
        val = (url,)
        self.mycursor.execute(sql, val)
        myresult = self.mycursor.fetchone()
        # return the id of the url as an integer
        return myresult[0]
    
    def is_page_indexed(self, url) -> bool:
        sql = "SELECT is_indexed FROM urls WHERE url = %s"
        val = (url,)
        self.mycursor.execute(sql, val)
        myresult = self.mycursor.fetchone()
        if myresult:
            return myresult[0]
        else:
            return False
    
    def close_connection(self):
        self.mycursor.close()
        self.db.close()
class Links:
    """This class handles the links"""
    def __init__(self, url):
        self.url = url
        self.db = Database()
        self.queue = []
        for link in self.get_unvisited_links():
            self.queue.append(link[0])
        self.add_link_to_queue(url)
        
    def __str__(self):
        return f"URL: {self.url}"
    
    def url_builder(self, path):
        # ignore the links that start with # or javascript or mailto or tel or whatsapp or skype
        if path == None or  path.startswith("#") or path.startswith("javascript") or path.startswith("mailto") or path.startswith("tel") or path.startswith("whatsapp") or path.startswith("skype"):
            return None
        else:
            if path.startswith("http"):
                return path
            else:
                if path.startswith('/'):
                    return self.url + path[1:]
                else:
                    return self.url + path

    # add a link to the database and the queue and return the id of the link
    def add_link_to_queue(self, url):
        url = self.url_builder(url)
        if url is not None:
            self.db.insert_links(url, 0)
            self.queue.append(url)
            return self.db.mycursor.lastrowid # return the id of the last inserted row
    
    def has_links(self):
        return len(self.queue) > 0
    
    def get_next_link(self):
        return self.queue.pop(0)
    
    def get_unvisited_links(self):
        return self.db.get_unvisited_links()
