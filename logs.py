#!/usr/bin/env python
# Logs Analysis (logs.py)

# Display:
# 1) Most popular 3 Articles
# 2) Most popular authors
# 3) Days with more than 1% leading to errors

import psycopg2
DBNAME = "news"


def execute_query(query):
    """Takes an SQL query, executes it, and returns parameter. """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        posts = c.fetchall()
        db.close()
        return posts
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == '__main__':
    print "##############################"
    print "#Logs App, made with Python 2#"
    print "##############################"

    # Print top articles
    query1 = "select title, count from uniquearticles limit 3;"
    top_articles = execute_query(query1)

    print "\n1) The most popular three articles are: "
    for article, count in top_articles:
        print "{} - {} views".format(article, str(count))

    # Print top authors
    query2 = """
        select name, sum(count) as totalviews
        from authors, uniquearticles
        where authors.id = uniquearticles.author
        group by name
        order by totalviews desc;
        """
    top_authors = execute_query(query2)
    print "\n2) The top authors are: "
    for author, count in top_authors:
        print "{} - {} views".format(author, str(count))

    # Print error rate
    thislist = []
    query3 = """
        select to_char(day, 'FMMonth DD, YYYY'),
        percent from daywithpercenterrors
        where percent > 1;
        """
    days = execute_query(query3)
    thislist.append(days)
    print "\n3) The day where there were more than 1% errors are: "
    for dayof, errpercent in thislist[0]:
        print "{} - {} %".format(dayof, errpercent)

    print "\n##############################"
    print "#          Complete          #"
    print "##############################"
