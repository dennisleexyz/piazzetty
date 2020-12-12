#!/usr/bin/python3
import pickle

from configparser import ConfigParser
from os import path
from pathlib import Path
from getpass import getpass

from appdirs import AppDirs
from piazza_api import rpc, exceptions
from requests import cookies

def login():
	d = AppDirs('piazzetty', 'piazzetty')

	# print(d.site_config_dir)
	# print(d.site_data_dir)
	# print(d.user_cache_dir)
	# print(d.user_config_dir)
	# print(d.user_data_dir)
	# print(d.user_log_dir)
	# print(d.user_state_dir)

	email = None

	config = ConfigParser()
	configpath = d.user_config_dir + '/config.ini'
	if path.exists(configpath):
		with open(configpath, 'r') as configfile:
			config.read(configpath)
			email = config.sections()[0] if config.sections() else None
			if config.get(email, None):
				password = config[email].get('password', None)
	else:
		Path(d.user_config_dir).mkdir(parents=True, exist_ok=True)
		Path(configpath).touch()

	cookie = None
	cookiepath = d.user_cache_dir + '/' + email if email else None
	if cookiepath:
		if not path.exists(cookiepath):
			Path(d.user_cache_dir).mkdir(parents=True, exist_ok=True)
			Path(cookiepath).touch()
		try:
			cookie = pickle.load(open(cookiepath, 'rb'))
		except:
			pass

	new_credentials = False
	new_cookie = False
	p = rpc.PiazzaRPC()

	while True:
		try:
			if cookie:
				p.session.cookies = cookie
				p._check_authenticated()
			elif password:
				p.user_login(email=email, password=password)
				new_cookie = True
			else:
				raise exceptions.AuthenticationError
			break
		except exceptions.NotAuthenticatedError:
			new_cookie = True
		except exceptions.AuthenticationError:
			email = input('Email: ')
			password = getpass()
			config[email] = {'password': password}
			new_credentials = True

	if new_credentials:
		with open(configpath, 'w') as configfile:
			config.write(configfile)

	if new_cookie:
		cookie = p.session.cookies
		with open(cookiepath, 'wb') as cookiefile:
			pickle.dump(cookie, cookiefile)

	return p

if __name__ == "__main__":
	p = login()
	print(p.get_user_status())
