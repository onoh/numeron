#!/usr/bin/python

import random, itertools, sqlite3

def main():

    db = "db.sqlite3"

    c = sqlite3.connect(db)
    cur = c.cursor()

    cur.execute("drop table if exists numeron3")
    cur.execute("drop table if exists numeron4")
    cur.execute("drop table if exists numeron5")
    cur.execute("create table numeron3 ( id integer primary key, number text)")
    cur.execute("create table numeron4 ( id integer primary key, number text)")
    cur.execute("create table numeron5 ( id integer primary key, number text)")

    insert(cur,3)
    insert(cur,4)
    insert(cur,5)
    c.commit()
    c.close()


def insert(cur,num):

    a = list(itertools.permutations(range(0,10),num))
    b = random.sample(a,len(a))
    for i in b:
      val = ""
      for x in i: val += str(x)
      cur.execute('insert into %(table)s(number) values("%(val)s")'% { "table":"numeron"+str(num),"val":val})


if __name__ == '__main__':
    main()
