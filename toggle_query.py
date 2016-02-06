#!/usr/bin/env python

import os
import cgitb
import MySQLdb
import cgi
import json
import HTMLParser
cgitb.enable()

class DB_Connection(object):
    def __init__(self, host="127.0.0.1"):
        self.db = MySQLdb.connect(host=host, 
                                  read_default_file = '/etc/mysql/my.cnf')
        self.cursor = self.db.cursor()

def debug(string):
    """
    For debugging through the browser
    """
    print "Content-type: text/html\n"
    print "<br>"
    print string
    print "<br>"

def main(JSONinput):
    query = JSONinput
    db = query['db'].replace('_phonemes', '')
    con = DB_Connection()

    if query['phonemes'] == True:
	to_db = db + '.catalog'
        from_db = db + '_phonemes.catalog'
    else:
        to_db = db + '_phonemes.catalog'
	from_db = db + '.catalog'

    sstring = HTMLParser.HTMLParser().unescape(query['sstring'])
    sql = "SELECT searchstring FROM " + to_db + " WHERE (filename, ep_number_year) IN (SELECT filename, ep_number_year FROM " + from_db + " WHERE searchstring=%s) LIMIT 1;"
    args = (sstring,) 
    con.cursor.execute(sql, args)
    result = con.cursor.fetchall()[0][0]

    print "Content-type: text/html\n"
    print result
    return True


if __name__=="__main__":
    form = cgi.FieldStorage()

    #Still supporting two names for the passed parameter.
    try:
        JSONinput = form["queryTerms"].value
    except KeyError:
        JSONinput = form["query"].value

    main(json.loads(JSONinput))
