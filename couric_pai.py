# =============================================================================
# IMPORTS
# =============================================================================
import praw
import config
import time
import datetime
import random
import os
import re
import sqlite3
import traceback

# =============================================================================
# GLOBALS
# =============================================================================

# Define database
conn = sqlite3.connect('couricpai.db')
c = conn.cursor()
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS comsRepliedTo(datestamp TEXT, com_id TEXT, author TEXT, replied INT)')

def data_entry(com_id, author, replied):
	unix = time.time()
	datestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	replied = int(replied)
	com_id = str(com_id)
	author = str(author)

	c.execute("INSERT INTO comsRepliedTo (datestamp, com_id, author, replied) VALUES(?, ?, ?, ?)", (datestamp, com_id, author, replied))
	conn.commit()

def data_read(comm):
	c.execute('SELECT count(*) FROM comsRepliedTo WHERE com_id = ?', (comm,))
	data = c.fetchone()[0]
	if data == 0:
		return 0
	else:
		return 1
create_table()

# Define Login Function
def bot_login():
	r = praw.Reddit(username = config.username,
					password = config.password,
					client_id = config.client_id,
					client_secret = config.client_secret,
					user_agent = "windows:com.example.myredditapp:v0.5 (by /u/Th3MadCreator)")

	return r

# Function to run bot
print("Starting bot....")
def run_bot(r):
	for comment in r.subreddit("all").comments(limit=100):
		#if "!CouricPai" in comment.body and comment.id not in comments_replied_to and not comment.author == r.user.me():
		comm = comment.id
		if "!CouricPai" in comment.body and data_read(comm) == 0 and not comment.author == r.user.me():
			com_id = comment.id
			com_auth = comment.author
			g = comment.body
			pattern = re.compile(r'\s+')
			g = re.sub(pattern, '', g)
			g = g.replace('!CouricPai', '')
			if g.isdigit():
				g = int(g)
				if isinstance(g, int):
					cp = float(g / 100)
					pa = float(cp / 10)
					try:
						comment.reply(str(g) + " Courics is equal to " + str(cp) + " Pai. Which, in turn, is equal to " + str(pa) + " Ajit." + "\n\n ^Beep ^Boop. ^I'm ^a ^bot. ^| [^My ^Creator](https://www.reddit.com/user/Th3MadCreator/) \n\n ^Donate: ^1F6ot1jCPW1Gi25v3nQzPPqkc2zVh2WVHL")
					except Exception as e:
						print('Error found in /r/' + comment.subreddit + '. Saving comment for later.')
						data_entry(com_id, com_auth, 0)
						print(e)
					else:	
						print("Found a comment! Posting reply to comment " + comment.id + "!")
						data_entry(com_id, com_auth, 1)
			else:
				comment.reply(str("I'm sorry, but I do not accept that input. Please try again with the following format:\n\n \n\n `!CouricPai 12345` \n\n ^Donate: ^1F6ot1jCPW1Gi25v3nQzPPqkc2zVh2WVHL"))
				data_entry(com_id, com_auth, 1)
				print("Bad comment found! Posting reply to comment " + comment.id + "!")
			#comments_replied_to.append(comment.id)

			#with open ("comments_replied_to.txt", "a") as f:
				#f.write(comment.id + "\n")

	time.sleep(1)

r = bot_login()
while True:
	try:
		run_bot(r)
	except Exception:
		traceback.print_exc()
