#! /usr/bin/env python3
# TikTok OSINT Tool
# @author https://github.com/sc1341
# 
# The creator nor any contributors are responsible for any illicit
# use of this program
#
#
import argparse
import json
import os
import random
import requests
import sys

from bs4 import BeautifulSoup # type: ignore
from useragents import *
from useragents import banner
user_agents = [
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


class TikTokOSINT:

	def __init__(self, username):
		# Make sure that the usernames starts with @ for the http request
		if username.startswith('@'):
			self.username = username
		else:
			self.username = f'@{username}'
		
		self.create_dir()
		# Scrapes the profile and creates the data and posts objects
		self.data = self.scrape_profile()
		# Save the data into the text file in the dir
		self.save_data()
		self.print_data()


	def scrape_profile(self):
		"""
		Scrapes the user profile and creates the data object
		which contains the user information
		:params: none
		:return:none
		"""
		r = requests.get(f'https://tiktok.com/{self.username}', headers={'User-Agent':random.choice(user_agents)})
		soup = BeautifulSoup(r.text, "html.parser")

		content = soup.find_all("script", attrs={"type":"application/json", "crossorigin":"anonymous"})

		content = json.loads(content[0].contents[0])

		print(content["props"]["pageProps"])

		profile_data = {
			"UserID":content["props"]["pageProps"]["userInfo"]["user"]["id"],
			"username":content["props"]["pageProps"]["userInfo"]["user"]["uniqueId"],
			"nickName":content["props"]["pageProps"]["userInfo"]["user"]["nickname"],
			"bio":content["props"]["pageProps"]["userInfo"]["user"]["signature"],
			"profileImage":content["props"]["pageProps"]["userInfo"]["user"]["avatarLarger"],
			"following":content["props"]["pageProps"]["userInfo"]["stats"]["followingCount"],
			"followers":content["props"]["pageProps"]["userInfo"]["stats"]["followerCount"],
			"fans":content["props"]["pageProps"]["userInfo"]["stats"]["followerCount"],
			"hearts":content["props"]["pageProps"]["userInfo"]["stats"]["heart"],
			"videos":content["props"]["pageProps"]["userInfo"]["stats"]["videoCount"],
			"verified":content["props"]["pageProps"]["userInfo"]["user"]["verified"]
			}

		return profile_data

	def download_profile_picture(self):
		"""Downloads the profile picture
		:params: none
		:return: none
		"""
		r = requests.get(self.data['profileImage'])
		with open(f"{self.username}.jpg","wb") as f:
			f.write(r.content)

	def save_data(self):
		"""
		Dumps the dict into a json file in the user directory
		:params: none
		:return: none
		"""
		with open(f'{self.username}_profile_data.json','w') as f:
			f.write(json.dumps(self.data))
		#with open(f'{self.username}_post_data.json', 'w') as f:
			#f.write(json.dumps(self.posts))
		print(f"Profile data saved to {os.getcwd()}")


	def create_dir(self):
		"""
		Create a directory to put all of the OSINT files into,
		it also avoid a possible error with a directory already existing
		:params: none
		:return: none
		"""
		i = 0
		while True:
			try:
				os.mkdir(self.username)
				os.chdir(self.username)
				break
			except FileExistsError:
				i += 1

	def print_data(self):
		"""Prints out the data to the cmd line
		:params:none
		:return: none
		"""
		for key, value in self.data.items():
			print(f"{key.upper()}: {value}")


def arg_parse():
	parser = argparse.ArgumentParser(description="TikTok OSINT Tool")
	parser.add_argument("--username", help="Profile Username", required=True, nargs=1)
	parser.add_argument("--downloadProfilePic", help="Downloads the user profile picture", required=False, action='store_true')
	return parser.parse_args()

def main():
	print(banner)
	args = arg_parse()
	if args.downloadProfilePic == True:
		tiktok = TikTokOSINT(args.username[0])
		tiktok.download_profile_picture()
	else:
		tiktok = TikTokOSINT(args.username[0])


if __name__ == "__main__":
	main()
