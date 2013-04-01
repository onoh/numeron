#!/usr/bin/python
# -*- encoding: utf-8 -*-
import sqlite3, itertools, random, json, re
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def default():

    params = { 'db': "db.sqlite3" }
    params['id'] = request.args.get("id","")
    params['card'] = request.args.get("card","")
    params['call'] = request.args.get("call","")

    match_id = re.compile("\d+").match(params['id'])
    match_card = re.compile("[3-5]").match(params['card'])

    if match_id and match_card:
      match_card = re.compile('\d'*int(params['card'])).search(params['call'])
      if match_card and int(params['card']) == len(params['call']):
        params['id'] = int(params['id'])
        return numeron(params)
    elif match_card:
      res = { "id": random.randint(1,ret_max(int(params['card']))), "card": params['card'] }
      return json.dumps(dict(res))

    params['id'] = random.randint(1,720)
    params['card'] = "3"
    return render_template("index.html", params=params)


def numeron(params):
    if 0 < params['id'] <= ret_max(int(params['card'])):
      table = "numeron"+params['card']
      n = q_db(params['db'],'select number from %(table)s where id = %(id)s' % { "table":table,"id":params['id']})[0][0]
      res = check(list(n),params['call'])
      return json.dumps(dict(res))


def ret_max(val):
    return reduce(lambda x,y:x*y,[x for x in range(10,(10-val),-1)] )
    

def check(target,call):
    match3 = [ "n..", ".n.", "..n" ]
    match4 = [ "n...", ".n..", "..n.", "...n" ]
    match5 = [ "n....", ".n...", "..n..", "...n.", "....n" ]
    eat, bite = 0, 0
    for i in range(0,len(call)):
      match = re.compile(target[i]).search(call)
      if match:
        r = eval("match"+str(len(call)))[i].replace("n",target[i])
        match = re.compile(r).match(call)
        if match: eat += 1
        else: bite += 1
    return  { "e":eat, "b":bite }


def q_db(db,query, args=(), one=False):
    cur = sqlite3.connect(db).cursor()
    cur.execute(query, args)
    res = cur.fetchall()
    return res

if __name__ == '__main__':
    app.debug = True
    app.run()
