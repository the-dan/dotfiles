#!/usr/bin/env python3

import subprocess
import sys
import os
import getpass
import datetime
import smtplib
from email.message import EmailMessage

import hashlib

COOLDOWN = datetime.timedelta(hours=6)

def touch(cmd, times=None):
	fname = get_lockfile(cmd)
	with open(fname, 'a'):
		os.utime(fname, times)

def get_lockfile(cmd):
	lock = hashlib.sha256(cmd.encode("utf8")).hexdigest()
	lock_file = os.path.join("/var/tmp/", "lock-%s" % (lock,))
	return lock_file

def should_send(cmd):
	lock_file = get_lockfile(cmd)
	last_run = datetime.datetime.now() - COOLDOWN - datetime.timedelta(seconds = 1)
	if not os.path.exists(lock_file):
		with open(lock_file,  "wb") as f:
			f.write(f"this is lock file for {cmd} under cron".encode("utf8"))
	else:
		last_run = datetime.datetime.fromtimestamp(os.path.getmtime(lock_file))


	if last_run + COOLDOWN < datetime.datetime.now():
		return True
	else:
		return False




def main():
	cmd = sys.argv[1]
	title = cmd
	if len(sys.argv) > 2:
		title = sys.argv[2]

	do_send_error = should_send(cmd)
	
	proc = subprocess.run(cmd, capture_output=True, shell=True, text=True)

	if proc.returncode != 0:

		if not do_send_error:
			return

		title = f"[FAILED] {title}"

		body = []
		if len(proc.stderr) > 0:
			body.append("Error output: %s" % (proc.stderr,))
		else:
			body.append("No error output")

		if len(proc.stdout) > 0:
			body.append("Standard output: %s" % (proc.stdout,))
		else:
			body.append("No standard output")			

		msg = "\n\n\n".join(body)

		msg = EmailMessage()
		msg['Subject'] = title
		msg['From'] = getpass.getuser()
		msg['To'] = getpass.getuser()
		msg.set_content("\n".join(body))

		s = smtplib.SMTP("localhost")
		s.send_message(msg)
		s.quit()

		touch(cmd)
	else:
		#title = f"[SUCCESS] {title}"
		#msg = ""
		pass
		# TODO: process could produce some useful artifacts, which would be worth putting in the mail itself

	
if __name__ == "__main__":
	main()



