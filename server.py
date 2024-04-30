import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future
import os;
import json;

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl

import Physics, math, random

public_files = [ '/shoot.html', '/shoot.css', '/shoot.js', '/title.html', '/title.css', '/title.js', '/anim.css', '/anim.js', '/victory.html' ]

gameNum = -1
totalGames = 0
p1Low = []
playerNum = []
              
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        global gameNum, totalGames, p1Low, playerNum
        # parse the URL to get the path and form data
        parsed = urlparse( self.path )

        # check if the web-pages matches the list
        if parsed.path in public_files:
            #NOTE THAT  THIS IS NEVER CALLED CURRENTLY BUT WILL BE LATER!!!
            #YOU HAVE TO CHANGE THE PATH TO /shoot.html
            if(parsed.path.startswith("/shoot.html")):

                form = dict( parse_qsl( parsed.query ) )
                # print(len(form))
                # retreive the HTML file
                if(len(form) > 1):
                    fp = open( '.'+parsed.path )
                    form["turnnum"] = 0 #<-- just added
                    form["playernum"] = 0
                    form["p1low"] = -1
                    

                    totalGames += 1
                    gameNum = totalGames-1

                    # print(form)

                    myGameName=form["gamename"]
                    
                    if totalGames > 1:
                        i=0
                        db = Physics.Database()
                        curs = db.connect.cursor()
                        curs.execute("""SELECT GAMENAME FROM Game""")
                        gameNames=curs.fetchall()
                        # print(len(gameNames))
                        while i < len(gameNames):
                            # print(i)
                            if myGameName == gameNames[i][0]:
                                myGameName = "Copy of " + myGameName
                                # print(myGameName, gameNames[i][0])
                                i=0
                            i += 1
                        curs.close()

                    form["gamename"] = myGameName

                    content = fp.read() % form
                    
                    Physics.Game(gameName=myGameName, player1Name=form["p1name"], player2Name=form["p2name"])
                    fp.close()
                else:
                    db = Physics.Database()
                    curs = db.connect.cursor()
                    curs.execute("""SELECT GAMENAME FROM Game""")
                    gameNames=curs.fetchall()
                    numGames = len(gameNames)
                    
                    # contentLength = int(self.headers['Content-Length'])
                    # postData = self.rfile.read(contentLength)
                    # data = json.loads(postData.decode("utf-8"))

                    # print(form["gamename"])

                    curs.execute("""SELECT GAMEID FROM Game WHERE GAMENAME='%s'""" % form["gamename"])

                    gameNum = curs.fetchone()
                    # print(gameNum)
                    if gameNum is not None:
                        gameNum = gameNum[0]-1
                    else:
                        gameNum=0

                    # print("GAme Nume = ", gameNum)

                    curs.execute("""SELECT PLAYERNAME FROM Player WHERE GAMEID=%d""" % (gameNum+1))

                    playerNames = curs.fetchall()
                    # print(gameNum)
                    if playerNames is not None:
                        p1Name = playerNames[0][0]
                        p2Name = playerNames[1][0]
                    else:
                        p1Name = "Player 1"
                        p2Name = "Player 2"

                    curs.execute("""SELECT MAX(TABLEID) FROM TableShot WHERE SHOTID = (SELECT MAX(SHOTID) FROM Shot WHERE GAMEID=%d)""" % (gameNum+1))
                    tableID = curs.fetchone()
                    # print(tableID)

                    curs.execute("""SELECT MAX(SHOTID) FROM Shot WHERE GAMEID=%d""" % (gameNum+1))

                    turnNum = curs.fetchone()
                    # print("turnNum = ", turnNum)
                    if turnNum is not None and turnNum[0] is not None:
                        turnNum = turnNum[0]
                    else:
                        turnNum=0

                    curs.execute("""SELECT COUNT(SHOTID) FROM Shot WHERE GAMEID!=%d""" % (gameNum+1))

                    numOtherTurns = curs.fetchone()
                    # print("turnNum = ", turnNum)
                    if numOtherTurns is not None and numOtherTurns[0] is not None:
                        numOtherTurns = numOtherTurns[0]
                    else:
                        numOtherTurns=0

                    turnNum -= numOtherTurns

                    # curs.execute("""SELECT PLAYERNAME FROM Player WHERE PLAYERID = (SELECT PLAYERID FROM Shot WHERE SHOTID=%d)""" % (turnNum))

                    # playerName = curs.fetchone()
                    # print("playerName = ", playerName)
                    # if playerName is not None and playerName[0] is not None:
                    #     playerName = playerName[0]
                    #     if playerName == p1Name:
                    #         playerNum = 2
                    #     else:
                    #         playerNum = 1
                    # else:
                    #     playerNum=0

                    curs.close()

                    # global p1Low
                    if tableID is not None and tableID[0] is not None:
                        tableID = tableID[0]

                        table=db.readTable(tableID-1)
                        # print(table)
                        fp = open( '.'+parsed.path )
                        content = fp.read()
                        fp.close()

                        startOfContent = content[:content.find("<?xml")-1]
                        endOfContent = content[content.find("</svg>")+6:]

                        if p1Low[gameNum]==True:
                            p1Low[gameNum]=1
                        elif p1Low[gameNum] == False:
                            p1Low[gameNum]=2

                        form = {"gamename" : form["gamename"],
                                "p1name" : p1Name,
                                "p2name" : p2Name,
                                "turnnum": turnNum,
                                "playernum": playerNum[gameNum],
                                "p1low": p1Low[gameNum]}

                        content = startOfContent + table.svg() + endOfContent
                        content = content % form
                    else:
                        fp = open( '.'+parsed.path )
                        form = {"gamename" : form["gamename"],
                                "p1name" : p1Name,
                                "p2name" : p2Name,
                                "turnnum": turnNum,
                                "playernum": playerNum[gameNum],
                                "p1low": p1Low[gameNum]}
                        print(form)
                        content = fp.read() % form
                        fp.close()
                        
            elif(parsed.path.startswith("/title.html")):

                form = dict( parse_qsl( parsed.query ) )

                if len(form) > 0:

                    db = Physics.Database()
                    curs = db.connect.cursor()

                    curs.execute("""SELECT GAMEID FROM Game WHERE GAMENAME='%s'""" % form["gamename"])

                    gameNum = curs.fetchone()
                    # print(gameNum)
                    if gameNum is not None:
                        gameNum = gameNum[0]-1
                    else:
                        gameNum=0

                    curs.close()

                    # global p1Low
                    if gameNum < len(p1Low):
                        p1Low[gameNum]=form["p1low"]
                        playerNum[gameNum] = int(form["playernum"])
                    else:
                        p1Low.append(form["p1low"])
                        playerNum.append(int(form["playernum"]))
                    

                    print(p1Low[gameNum], playerNum[gameNum])

                    if p1Low[gameNum]=="true":
                        p1Low[gameNum]=1
                    elif p1Low[gameNum] == "false":
                        p1Low[gameNum]=2
                    else:
                        p1Low[gameNum]=-1

                count=0
                while(os.path.exists("./table%02d.svg" % count)):
                    os.remove("./table%02d.svg" % count)
                    count += 1

                fp = open( '.'+parsed.path )
                content = fp.read()
                fp.close()
            
            elif(parsed.path.startswith("/victory.html")):
                form = dict( parse_qsl( parsed.query ) )

                print(form)

                if int(form["endinfo"]) == 1:
                    form["endinfo"]= "%s sank the 8 ball after sinking all their other balls!" % form["winner"]
                else:
                    form["endinfo"]= "%s sank the 8 ball before sinking all their other balls." % form["loser"]
                fp = open( '.'+parsed.path )
                content = fp.read() % form
                fp.close()
                db = Physics.Database()
                curs = db.connect.cursor()

                curs.execute("""SELECT GAMEID FROM Game WHERE GAMENAME='%s'""" % form["gamename"])

                gameNum = curs.fetchone()
                # print(gameNum)
                if gameNum is not None:
                    gameNum = gameNum[0]-1
                else:
                    gameNum=0
                
                curs.execute("DELETE FROM  Player WHERE GAMEID=%d" % (gameNum+1))
                curs.execute("DELETE FROM  Shot WHERE GAMEID=%d" % (gameNum+1))
                curs.execute("DELETE FROM Game WHERE GAMEID=%d" % (gameNum+1))

                # curs.execute("DELETE * FROM Player WHERE GAMEID=(SELECTMAX(GAMEID) FROM Player)")
                curs.close()
                db.connect.commit()

            elif(parsed.path.startswith("/title.js")):
                    
                    if(totalGames == 0):
                        Physics.Database(True)

                    db = Physics.Database()
                    # db.createDB()
                    curs = db.connect.cursor()
                    # curs.execute("""SELECT * FROM Game""")
                    # games = curs.fetchall()
                    # print(games)
                    curs.execute("""SELECT Name 
                            FROM SQLITE_MASTER""")
                    if curs.fetchone() is not None:
                        curs.execute("""SELECT GAMENAME FROM Game""")
                        gameNames=curs.fetchall()
                        # curs.execute("""SELECT MAX(GAMEID) FROM Game""")
                        # numGames=curs.fetchone()
                        # if numGames is None:
                        #     numGames=0
                        # else:
                        #     numGames = numGames[0]
                        numGames = len(gameNames)
                        # print(gameNames, numGames)
                        fp = open( '.'+parsed.path )
                        nameList = []
                        for i in range(numGames):
                            nameList.append(gameNames[i][0])
                        # print(tuple(nameList))
                        content = fp.read()
                        # print(content)
                        startOfContent = content[:content.find("YEET")-1]
                        endOfContent = content[content.find("YEET")+5:]

                        content = startOfContent
                        for i in range(numGames):
                            content += """$("body").append("<button style=\\"font-size:40px;\\"onclick=\\"loadGame(event)\\">%s</button>")\n""" % nameList[i]
                        content += endOfContent
                        # print(content)

                        fp.close()
                        curs.close()
                    else:
                        fp = open( '.'+parsed.path )
                        content = fp.read()
                        fp.close()
            
            # retreive the HTML file
            else:
                fp = open( '.'+parsed.path )
                content = fp.read()
                fp.close()

            # generate the headers
            self.send_response( 200 ); # OK
            if(parsed.path.endswith(".html")):
                self.send_header( "Content-type", "text/html" )
            elif(parsed.path.endswith(".css")):
                self.send_header( "Content-type", "text/css" )
            elif(parsed.path.endswith(".js")):
                self.send_header("Content-type", "text/javascript")

            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )

            

        elif parsed.path.endswith(".svg"):
            # print(parsed.path)
            if os.path.exists('.' + parsed.path):
                # retreive the HTML file
                fp = open( '.'+self.path )
                content = fp.read()
                self.send_response( 200 ); # OK
                if(parsed.path.startswith("/table")):
                    content=content[content.find("<svg"):]
                    self.send_header( "Content-type", "text/svg+xml" )
                    # content = content[content.find("""<circle class="ball" """):content.find("""</svg>""")]
                    # print(content)
                # content = content[content.find("<svg "):]
                else:
                    self.send_header( "Content-type", "image/svg+xml" )
                
                # print("YEET")
                fp.close()
                
                # generate the headers
                
                
                self.send_header( "Content-length", len( content ) )
                self.end_headers()

                # send it to the broswer
                self.wfile.write( bytes( content, "utf-8" ) )
                
            else:
                self.send_response( 404 )
                self.end_headers()
                self.wfile.write( bytes( "404: not found", "utf-8" ) )
        else:
                self.send_response( 404 )
                self.end_headers()
                self.wfile.write( bytes( "404: not found", "utf-8" ) )
        
    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data

        if self.path == '/anim.html':

            # form = cgi.FieldStorage( fp=self.rfile,
            #                          headers=self.headers,
            #                          environ = { 'REQUEST_METHOD': 'POST',
            #                                      'CONTENT_TYPE': 
            #                                        self.headers['Content-Type'],
            #                                    } 
            #                        )
            
            global gameNum

            contentLength = int(self.headers['Content-Length'])
            postData = self.rfile.read(contentLength)
            data = json.loads(postData.decode("utf-8"))
            print(data)
            turnNum = data[0]
            x1=data[1]
            y1=data[2]
            x2=data[3]
            y2=data[4]
            playerNum=data[5]
            gameName=data[6]
            # p1Low = data[6]

            db = Physics.Database()
            cur = db.connect.cursor()

            cur.execute("""SELECT GAMEID FROM Game WHERE GAMENAME='%s'""" % gameName)

            gameNum = cur.fetchone()
            # print(gameNum)
            if gameNum is not None:
                gameNum = gameNum[0]-1
            else:
                gameNum=0
            
            # read the HTML file and insert the form data
            # fp = open( './shoot.html' )
            # content = fp.read() % form
            # print(content)
            # content = fp.read()
            if(turnNum > 1):
                count=0
                while(os.path.exists("./table%02d.svg" % count)):
                    os.remove("./table%02d.svg" % count)
                    count += 1

                # cur.execute( """SELECT TABLEID FROM TableShot WHERE TableShot.SHOTID = (SELECT MAX(SHOTID) FROM TableShot);""")
                cur.execute("""SELECT MAX(TABLEID) FROM TableShot WHERE SHOTID = (SELECT MAX(SHOTID) FROM Shot WHERE GAMEID=%d)""" % (gameNum+1))
                tableIDs = cur.fetchone()
                # print(tableIDs)
                # count = tableIDs[len(tableIDs)-1][0]
                count = tableIDs[0]
                # print("STOP THE COUNT", count)

                table = db.readTable(count-1)
                # print(table)
            else:
                count=0
                # print("yeet")
                while(os.path.exists("./table%02d.svg" % count)):
                    os.remove("./table%02d.svg" % count)
                    count += 1

                # Physics.Game(gameName=game_name, player1Name=p1_name, player2Name=p2_name)
                # Physics.Game(0)
                table=initDB()

            #A2Test2 Stuff:
            
            # pos = Physics.Coordinate(table.cueBall().obj.still_ball.pos.x, table.cueBall().obj.still_ball.pos.y) 
            # point1 = Physics.Coordinate(x1, y1)
            # point2 = Physics.Coordinate(float(form.getvalue("x2")), float(form.getvalue("y2")))
            vector = Physics.Coordinate(x2-x1, y2-y1)
            # vector =  math.sqrt((point2.x-point1.x)*(point2.x-point1.x) + (point2.y-point1.y)*(point2.y-point1.y))
            # pos = Physics.Coordinate(point1.x, point1.y)
            vel = Physics.Coordinate(vector.x*(-3), vector.y*(-3))
            # print(vel.x,vel.y)
            if vel.x > 2000:
                vel.x=2000
                vel.y *= (2000 / (vector.x*(-3)))
            elif vel.x < -2000:
                vel.x=-2000
                vel.y *= (-2000 / (vector.x*(-3)))
            # print(vel.x,vel.y)
            if vel.y > 2000:
                vel.y=2000
                vel.x *= (2000 / (vector.y*(-3)))
            elif vel.y < -2000:
                vel.y = -2000
                vel.x *= (-2000 / (vector.y*(-3)))
            print(vel.x,vel.y)
            # if vel.x > 1000:
            #     vel.x=1000
            # if vel.y > 1000:
            #     vel.y=1000

            
            print("Game Num:",gameNum)
            game = Physics.Game(gameNum)
            # game = Physics.Game(gameName="HEHE", player1Name="Ryan", player2Name="James")
            if(playerNum==1):
                player = game.player1Name
            else:
                player = game.player2Name
            numFrames = game.shoot(game.gameName, player, table, vel.x, vel.y)
            if(numFrames >= 3000):
                print("Error: Infinite collision bug occurred.")
                self.send_response( 404 )
                self.end_headers()
                self.wfile.write( bytes( "404: Error: Infinite collision bug occurred", "utf-8" ) )
                return

            # content = """<!DOCTYPE html>
            #                 <html lang=”en”>
            #                     <head>
            #                     <meta charset=”utf-8” />
            #                     <link rel="stylesheet" href="./anim.css">
            #                     <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            #                     <script src="anim.js"></script>
            #                     </head>
            #                     <body>
            #                     <svg width="700" height="1375" viewBox="-25 -25 1400 2750"
            #                         xmlns="http://www.w3.org/2000/svg"
            #                         xmlns:xlink="http://www.w3.org/1999/xlink">
            #                         <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />
            #                         <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />
            #                         <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />
            #                         <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />
            #                         <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />
            #                         <circle cx="0" cy="0" r="114" fill="black" />
            #                         <circle cx="0" cy="1350" r="114" fill="black" />
            #                         <circle cx="0" cy="2700" r="114" fill="black" />
            #                         <circle cx="1350" cy="0" r="114" fill="black" />
            #                         <circle cx="1350" cy="1350" r="114" fill="black" />
            #                         <circle cx="1350" cy="2700" r="114" fill="black" />"""
            
            # for thing in table:
            #     if thing.__class__ == Physics.RollingBall:
            #         content += "Ball Number: %d, Ball Position: (%6.1lf, %6.1lf), Ball Velocity: (%6.1lf, %6.1lf)" % (thing.obj.rolling_ball.number, thing.obj.rolling_ball.pos.x, thing.obj.rolling_ball.pos.y, thing.obj.rolling_ball.vel.x, thing.obj.rolling_ball.vel.y)
            #         content += "<br>"
            #     elif thing.__class__ == Physics.StillBall:
            #         content += "Ball Number: %d, Ball Position: (%6.1lf, %6.1lf)" % (thing.obj.still_ball.number, thing.obj.still_ball.pos.x, thing.obj.still_ball.pos.y)
            #         content += "<br>"
            
            
            cur.execute( """SELECT TABLEID FROM TableShot WHERE TableShot.SHOTID = (SELECT MAX(SHOTID) FROM TableShot);""")
            tableIDs = cur.fetchall()
            # print(tableIDs)
            count = tableIDs[0][0] - 1
            # print("PLEASE", count)
            # cur.execute( """SELECT * FROM TableShot """)
            # print(cur.fetchall())
            # for i in range(len(tableIDs)):
            #     write_svg(i, db.readTable(i))
            while table and count < tableIDs[len(tableIDs)-1][0]:
                # print(count)
                table = db.readTable(count)
                write_svg(count - tableIDs[0][0]+1, table)
                # fp = open('./table-%d.svg' % (count), "w")
                # fp.write(table.svg())
                count += 1
            # fp.close()

            # for i in range(count):

            #     fp = open("./table%02d.svg" % i, "r")
            #     svgContent = content + fp.read()
                
            # content += """<br></svg></body>
            #             </html>"""
                # generate the headers

            cur.close()
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len("HOORAY") )
            self.end_headers()
                
            # send it to the browser
            self.wfile.write(bytes("HOORAY", "utf-8"))
                
            # fp.close()
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

def initDB():
        

    table = Physics.Table()
    addBalls(table)

    db = Physics.Database()
    # db.createDB()

    # db.writeTable(table)

    return table

def addBalls(table):

    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0,
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 )
    table += Physics.StillBall(0, pos)
    row=1
    spotInRow=1
    start = 0
    for i in range(15):
        
        # pos = Physics.Coordinate(
        #         Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER)*i//2 +
        #         nudge(),
        #         Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)*i//5 +
        #         nudge()
        #         )
        pos = Physics.Coordinate(Physics.TABLE_WIDTH/2.0-(Physics.BALL_DIAMETER+4.0) * (start+spotInRow-1) + nudge(), Physics.TABLE_WIDTH/2.0 - 
                math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)*row + nudge())

        spotInRow+=1
        if spotInRow > row:
            spotInRow = 1
            row += 1
            start -=0.5
        if i != 4 and i != 0 and i != 1:
            ballNum = 8 - (-i//2 + i*(i%2))
        elif i == 4:
            ballNum=8
        elif i == 0:
            ballNum = 1
        else:
            ballNum = 10
        table += Physics.StillBall(ballNum, pos)

def readCueLine(htmlContent):
    lineIndex = htmlContent.find("<line ")
    if lineIndex != -1:
        rb = Physics.RollingBall()

def nudge():
    return random.uniform( -1.5, 1.5 )

def write_svg( table_id, table ):
    with open( "table%02d.svg" % table_id, "w" ) as fp:
        if table:
            fp.write( table.svg() )
        else:
            fp.write(Physics.HEADER + Physics.FOOTER)


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), RequestHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()
    