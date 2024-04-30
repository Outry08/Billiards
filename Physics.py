import phylib
import sqlite3
import os

from copy import copy, deepcopy

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS   = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH  = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH   = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE      = phylib.PHYLIB_SIM_RATE
VEL_EPSILON   = phylib.PHYLIB_VEL_EPSILON
DRAG          = phylib.PHYLIB_DRAG
MAX_TIME      = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS   = phylib.PHYLIB_MAX_OBJECTS
FRAME_PERIOD  = 0.01

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ]

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # add an svg method here
    def svg(self):
        if self.obj.still_ball.number == 0:
            return """ <circle class="ball" id="que" cx="%d" cy="%d" r="%d" fill="%s"></circle>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return """ <circle class="ball" cx="%d" cy="%d" r="%d" fill="%s"></circle>\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

        
class RollingBall( phylib.phylib_object ):
    
    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_ROLLING_BALL, 
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0)
        
        self.__class__ = RollingBall

    def svg(self):
        if self.obj.rolling_ball.number == 0:
            return """ <circle class="ball" id="que" cx="%d" cy="%d" r="%d" fill="%s"></circle>\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return """ <circle class="ball" cx="%d" cy="%d" r="%d" fill="%s"></circle>\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

class Hole(phylib.phylib_object):

    def __init__(self, pos):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      None,
                                      pos, None, None,
                                      0.0, 0.0)
        self.__class__ = Hole

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

class HCushion(phylib.phylib_object):
    def __init__(self, y):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      None,
                                      None, None, None,
                                      0.0, y)
        self.__class__ = HCushion

    def svg(self):
        if(self.obj.hcushion.y == 0):
            y = -25
        else:
            y = 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)

class VCushion(phylib.phylib_object):

    def __init__(self, x):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      None,
                                      None, None, None,
                                      x, 0.0)
        self.__class__ = VCushion

    def svg(self):
        if(self.obj.vcushion.x == 0):
            x = -25
        else:
            x = 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self )
        self.current = -1

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other )
        return self

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ] # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1    # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ) 
        if result==None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += "time = %6.1f;\n" % self.time    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            
            result += "  [%02d] = %s\n" % (i,obj)  # append object description
        return result  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self )
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here
    def svg(self):
        strcat = HEADER + "\n"
        for i in self:
            if i is not None:
                strcat += i.svg()
        strcat += FOOTER
        return strcat
    
    def roll( self, t ):
        new = Table()
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(ball.obj.rolling_ball.acc.x, ball.obj.rolling_ball.acc.y) )
                # Changed to original ball's acc.x & acc.y b/c phylib_roll doesn't update or set new acc anywhere ^^^
                # compute where it rolls to
                # print(ball.obj.rolling_ball.vel.y)
                # print(new_ball.obj.rolling_ball.vel.y)
                phylib.phylib_roll( new_ball, ball, t )
                # print()
                # print(ball.obj.rolling_ball.vel.y)
                # print(new_ball.obj.rolling_ball.vel.y)
                # add ball to table
                new += new_ball
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
        # return table
        return new
    
    def copyTable( self ):
        newTable = Table()
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create a new ball with the same number as the old ball
                newBall = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y),
                                        Coordinate(ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y),
                                        Coordinate(ball.obj.rolling_ball.acc.x, ball.obj.rolling_ball.acc.y) )

                # add ball to table
                newTable += newBall
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                newBall = StillBall( ball.obj.still_ball.number,
                                      Coordinate( ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y ) )
                # add ball to table
                newTable += newBall

        newTable.time = self.time

        # return table
        return newTable
    
    def cueBall(self):
        for thing in self:
            if isinstance(thing, StillBall) and thing.obj.still_ball.number == 0:
                self.current = -1
                return thing
            
        return None

    
class Database :
    def __init__(self, reset=False):
        if os.path.exists("./phylib.db") and reset == True:
            os.remove("./phylib.db")
        self.connect = sqlite3.connect("phylib.db")
        

    def createDB(self):

        cursor = self.connect.cursor()
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'Ball'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE Ball(BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                BALLNO INTEGER NOT NULL,
                                XPOS FLOAT NOT NULL,
                                YPOS FLOAT NOT NULL,
                                XVEL FLOAT,
                                YVEL FLOAT)""")
            
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'TTable'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE TTable(TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                TIME FLOAT NOT NULL)""")
                
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'BallTable'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE BallTable(BALLID INTEGER NOT NULL,
                                TABLEID INTEGER NOT NULL,
                                FOREIGN KEY(BALLID) REFERENCES Ball,
                                FOREIGN KEY(TABLEID) REFERENCES TTable)""")
            
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'Shot'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE Shot(SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                PLAYERID INTEGER NOT NULL,
                                GAMEID INTEGER NOT NULL,
                                FOREIGN KEY(PLAYERID) REFERENCES Player,
                                FOREIGN KEY(GAMEID) REFERENCES Game)""")
            
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'TableShot'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE TableShot(TABLEID INTEGER NOT NULL,
                                SHOTID INTEGER NOT NULL,
                                FOREIGN KEY(TABLEID) REFERENCES TTable,
                                FOREIGN KEY(SHOTID) REFERENCES Shot)""")
            
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'Game'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE Game(GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                GAMENAME VARCHAR(64) NOT NULL)""")
            
        cursor.execute("""SELECT Name 
                            FROM SQLITE_MASTER
                            WHERE Name = 'Player'""")
        if cursor.fetchone() == None:
            cursor.execute("""CREATE TABLE Player(PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                GAMEID INTEGER NOT NULL,
                                PLAYERNAME VARCHAR(64) NOT NULL,
                                FOREIGN KEY(GAMEID) REFERENCES Game)""")
        
        cursor.close()
        self.connect.commit()
        
    def readTable(self, tableID):
        
        table = Table()
        
        cursor = self.connect.cursor()
        
        cursor.execute("""SELECT TTable.TIME FROM TTable WHERE TTable.TABLEID = %d""" % (tableID+1))
        fetched = cursor.fetchone()
        if fetched is not None:
            table.time = fetched[0]
        else:
            return None
        
        cursor.execute("""SELECT BallTable.TABLEID FROM BallTable WHERE BallTable.TABLEID = %d""" % (tableID+1))
        fetched = cursor.fetchone()
        if fetched is None:
            return None
        
        cursor.execute("""SELECT * FROM BallTable, Ball
                                     WHERE BallTable.BALLID = Ball.BALLID AND BallTable.TABLEID = %d""" % (tableID+1))
        balls = cursor.fetchall()
        if balls is None:
            return None
        
        # Debugging print
        # print(balls)
        
        sbList = []
        rbList = []
        
        for row in balls:
            pos = Coordinate(row[4], row[5])
            if row[6] == None and row[7] == None:
                sbList.append(StillBall(row[3], pos))
            else:
                vel = Coordinate(row[6], row[7])
                aSpeed = phylib.phylib_length(vel)

                if(aSpeed > VEL_EPSILON):
                    acc = Coordinate(-1 * vel.x / aSpeed * DRAG, -1 * vel.y / aSpeed * DRAG)
                else:
                    acc = Coordinate(0,0)
                rbList.append(RollingBall(row[3], pos, vel, acc))
                
        for ball in sbList:
            table += ball
        for ball in rbList:
            table += ball
            
        cursor.close()
        self.connect.commit()
            
        return table
        
    def writeTable(self, table):
        cursor = self.connect.cursor()
        
        cursor.execute("""INSERT INTO TTable(TIME)
                        VALUES(%lf)""" % (table.time))
        
        for i in table:
            if(isinstance(i, RollingBall) or isinstance(i, StillBall)):
                if isinstance(i, RollingBall):
                    cursor.execute("""INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL)
                                VALUES(%d, %lf, %lf, %lf, %lf)""" % (i.obj.rolling_ball.number, i.obj.rolling_ball.pos.x, i.obj.rolling_ball.pos.y, i.obj.rolling_ball.vel.x, i.obj.rolling_ball.vel.y))
                elif isinstance(i, StillBall):
                    cursor.execute("""INSERT INTO Ball(BALLNO, XPOS, YPOS, XVEL, YVEL)
                                    VALUES(%d, %lf, %lf, NULL, NULL)""" % (i.obj.still_ball.number, i.obj.still_ball.pos.x, i.obj.still_ball.pos.y))
                cursor.execute("""INSERT INTO BallTable
                                VALUES((SELECT MAX(Ball.BALLID) FROM Ball), (SELECT MAX(TTable.TABLEID) FROM TTable))""")
        
        cursor.execute("""SELECT MAX(TTable.TABLEID) FROM TTable""")
        fetched = cursor.fetchone()
        if fetched is not None:
            tableID = fetched[0]
        cursor.close()
        self.connect.commit()
        
        return tableID
    
    def close(self):
        self.connect.commit()
        self.connect.close()

    def getGame(self, gameID):
        cursor = self.connect.cursor()

        cursor.execute("""SELECT * FROM Player, Game WHERE Player.GAMEID = Game.GAMEID AND Game.GAMEID = %d""" % (gameID))
        selectList = cursor.fetchall()
        print(selectList)

        if selectList is not None and selectList[0] is not None:
            gameName = selectList[0][4]
            player1Name = selectList[0][2]
            player2Name = selectList[1][2]
        else:
            gameName = "Game"
            player1Name = "Player 1"
            player2Name = "Player 2" 
        
        cursor.close()

        return gameName, player1Name, player2Name
    
    def setGame(self, gameName, player1Name, player2Name):
        cursor = self.connect.cursor()

        cursor.execute("""INSERT INTO Game (GAMENAME) VALUES('%s')""" % (gameName))
        cursor.execute("""SELECT MAX(GAMEID) FROM Game""")
        idList = cursor.fetchone()
        if idList is not None:
            gameID = idList[0]
        else:
            gameID = None
        cursor.execute("""INSERT INTO Player(GAMEID, PLAYERNAME) VALUES(%d, '%s')""" % (gameID, player1Name))
        cursor.execute("""INSERT INTO Player(GAMEID, PLAYERNAME) VALUES(%d, '%s')""" % (gameID, player2Name))
        
        cursor.close()
        self.connect.commit()

        return gameID

    def newShot(self, playerName, gameID):
        cursor = self.connect.cursor()

        cursor.execute("""INSERT INTO Shot (PLAYERID, GAMEID) VALUES((SELECT PLAYERID FROM Player WHERE Player.PLAYERNAME = '%s' AND Player.GAMEID = %d), %d)""" % (playerName, gameID, gameID))

        cursor.execute("""SELECT MAX(SHOTID) FROM Shot""")

        idList = cursor.fetchone()
        if idList is not None:
            shotID = idList[0]
        else:
            shotID = None

        cursor.close()
        self.connect.commit()

        return shotID

class Game :
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        db = Database()
        db.createDB()
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            self.gameID = gameID + 1
            nameList = db.getGame(self.gameID)
            self.gameName = nameList[0]
            self.player1Name = nameList[1]
            self.player2Name = nameList[2]
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameID = db.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError

    def shoot(self, gameName, playerName, table, xvel, yvel):
        db = Database()
        shotID = db.newShot(playerName, self.gameID)

        cue = table.cueBall()
        xpos = cue.obj.still_ball.pos.x
        ypos = cue.obj.still_ball.pos.y
        cue.type = phylib.PHYLIB_ROLLING_BALL
        cue.obj.rolling_ball.number = 0
        cue.obj.rolling_ball.pos.x = xpos
        cue.obj.rolling_ball.pos.y = ypos
        cue.obj.rolling_ball.vel.x = xvel
        cue.obj.rolling_ball.vel.y = yvel
        
        speed = phylib.phylib_length(cue.obj.rolling_ball.vel)

        if speed > VEL_EPSILON:
            cue.obj.rolling_ball.acc.x = -1 * xvel / speed * DRAG
            cue.obj.rolling_ball.acc.y = -1 * yvel / speed * DRAG
        else:
            cue.obj.rolling_ball.acc.x = 0
            cue.obj.rolling_ball.acc.y = 0

        tableCopy = table.copyTable()
        
        cursor = db.connect.cursor()

        count = 0
        while tableCopy and count < 3000:
            print(count)
            table = tableCopy.copyTable()
            prevTime = tableCopy.time
            tableCopy = tableCopy.segment()
            if tableCopy:
                newTime = tableCopy.time
                segTime = round((newTime - prevTime) / FRAME_PERIOD, 0)
                for time in range(int(segTime)):
                    count+=1
                    tableRollCopy = table.roll(time * FRAME_PERIOD)
                    tableRollCopy.time = prevTime + time * FRAME_PERIOD
                    tableID = db.writeTable(tableRollCopy)
                    cursor.execute("""INSERT INTO TableShot(TABLEID, SHOTID) VALUES(%d, %d)""" % (tableID, shotID))
            else:
                tableID = db.writeTable(table)
                cursor.execute("""INSERT INTO TableShot(TABLEID, SHOTID) VALUES(%d, %d)""" % (tableID, shotID))

        cue = table.cueBall()
        if cue == None:
            xpos = TABLE_WIDTH/2.0
            ypos = TABLE_LENGTH/2.0
            cue = StillBall(0, Coordinate(xpos, ypos))
            table += cue
            tableID = db.writeTable(table)
            cursor.execute("""INSERT INTO TableShot(TABLEID, SHOTID) VALUES(%d, %d)""" % (tableID, shotID))

        cursor.close()
        if(count < 3000):
            db.connect.commit()

        return count
        