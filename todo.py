from datetime import datetime
from pymongo.connection import Connection
import pymongo
import sys

class TodoDBConnection(object):

	def __init__(self):
		try:
			self.connection = Connection()
			#define database name
			self.db = self.connection.todo_db_delete
		except Exception, e:
			raise Exception ( "Error!! Please check db conenction: %s" % e )

class TodoApp(object):

	def __init__ (self, argv):
		self.argv = argv
		self.mongo = TodoDBConnection()

	def add (self, level):
		if 2 >= len( self.argv ):
			raise Exception( "missing argument" )
		self.mongo.db.todo_collection.insert( { "task": sys.argv[2], "level": level, "complete": False, "added": "" } )

	def list_incomplete (self, params):
		params.update({ "complete": False })
		cursor = self.mongo.db.todo_collection.find(params).sort([( "level", pymongo.ASCENDING),( "added", pymongo.ASCENDING)])
		for row in cursor:
			print row['task']

	def list_complete (self):
		cursor = self.mongo.db.todo_collection.find({ "complete":{ "$ne": False }}).sort("completed", pymongo.ASCENDING)
		for row in cursor:
			print row['task'], row['complete']

	def complete_todo (self, finish):
		if 2 >= len( self.argv ):
			raise Exception("missing argument")
		document = self.mongo.db.todo_collection.find_one( { "complete": False, "task": sys.argv[2]})
		if not document:
			print "No Matching ToDo Found"
		else:
			if finish:
				document['complete'] = datetime.utcnow()
				self.mongo.db.todo_collection.save( document )
			else:
				self.mongo.db.todo_collection.remove( document )

	def help ( self, error=None ):
		if None != error:
			print error
			print
		print "usage: %s <method>" % self.argv[0]
		print
		print "all command options"
		print
		print "<none>             list all incomplete tasks"
		print "help               show this help"
		print "next               list all incomplete tasks that are high priority"
		print "done               list all complete tasks chronologically"
		print "high <argument>    add high priority task called <argument>"
		print "low <argument>     add low priority task called <argument>"
		print "finish <argument>  complete task called <argument>"
		print "dont <argument>    delete unfinished task called <argument>"

	def run ( self ):
		try:
			if 1 >= len( self.argv ):
				self.list_incomplete( {} )
			else:
				if "help" == self.argv[1].lower():
					self.help()
				elif "next" == self.argv[1].lower():
					self.list_incomplete( { "level": "high" } )
				elif "done" == self.argv[1].lower():
					self.list_complete()
				elif "high" == self.argv[1].lower():
					self.add( "high" )
				elif "low" == self.argv[1].lower():
					self.add( "low" )
				elif "finish" == self.argv[1].lower():
					self.complete_todo( True )
				elif "dont" == self.argv[1].lower():
					self.complete_todo( False )
				else:
					raise Exception( "Something Went Wrong" )
		except Exception, e:
			self.help( str(e))

if __name__ == "__main__":
	try:
		app = TodoApp( sys.argv )
		app.run()	
	except Exception, e:
		print e