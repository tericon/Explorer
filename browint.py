from Default.color import printer, color_init
from Transformations.Explorer.browint_config import *
from Default.selenium_support import *
from time import sleep
from Default.scommand import execute
import os
import re
import pynput
from pynput import keyboard 


def search(path_to_urls_list, driver=None):
	execute("clear")
	global now_index, saved_index
	
	# Set now index
	now_index = 0
	
	# Details
	saved_index = []
	file_name = re.sub(r".*/", "", str(path_to_urls_list))
	case_path = re.sub(r"/.*", "", str(path_to_urls_list))
	
	# Driver Initialization
	if driver == None:
		driver = get_driver(debug=True)
		
	# Read file with urls
	urls_list = []
	with open(str(path_to_urls_list), "r") as urls_file_list:
		urls_dirty = urls_file_list.readlines()
		for url in urls_dirty:
			true_url = re.sub("\n", "", str(url))
			urls_list.append(str(true_url))
			
	# First screen
	def first_screen():
		color_init("default_colorschemes")
		execute("clear")
		for element in urls_list:
			if element == urls_list[int(now_index)]:
				color_init("coursor_colorschemes")
				printer(f"  [+]---> {str(element)}")
				color_init("default_colorschemes")
			else:
				printer(f"  [-] {str(element)}")
				
	# Reactions on button
	def on_press(key):
		shower_gel = True
		global now_index, saved_index
		execute("clear")
		
		if key == keyboard.Key.enter:
			execute("clear")
			get_url(driver, str(urls_list[int(now_index)]))
			execute("clear")

		elif key == keyboard.Key.esc:
			shower_gel = False
			driver_close(driver)
			listener.stop()
			
		elif key == keyboard.Key.space:
			save_file_name = str(prefix_to_save_file) + str(file_name)
			with open(str(save_file_name), "a") as save_file:
				save_file.write(str(urls_list[int(now_index)-1]) + "\n")
			saved_index.append(urls_list[int(now_index)-1])
			
		elif key == keyboard.Key.up:
			now_index -= 1
		
		elif key == keyboard.Key.down:
			now_index += 1
			
		elements_number = int(len(urls_list))
		if int(now_index) <= 0:
			now_index = elements_number
		if int(now_index) >= elements_number:
			now_index = 0
		
		if shower_gel == True:
			for element in urls_list:
				if element == urls_list[int(now_index)]:
					color_init("coursor_colorschemes")
					printer(f"  [+]---> {str(element)}")
					color_init("default_colorschemes")
				elif element in saved_index:
					print()
					color_init("A_colorschemes")
					printer(f"  [S]=> {str(element)}")
					color_init("default_colorschemes")
				else:
					printer(f"  [-] {str(element)}")
			
	# Start fist screen
	first_screen()
	# Button checker
	with keyboard.Listener(on_press=on_press) as listener:
		#try:
		listener.join()
		execute("clear")
		#except:
			#pass
	# EXIT
	#try:
	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	#except:
		#pass
	#try:
	listener.stop()
	#except:
		#pass

def auto_search(path_to_urls_list, driver=None, conf_status=False):
	execute("clear")
	global now_index, saved_index
	
	# Details
	saved_index = []
	errors_index = []
	file_name = re.sub(r".*/", "", str(path_to_urls_list))
	case_path = re.sub(r"/.*", "", str(path_to_urls_list))
	
	# Driver Initialization
	if driver == None:
		driver = get_driver(debug=True)
	
	# Check config and set now_index
	if conf_status == True:
		try:
			config_path = str(case_path) + str(conf_directory)
			shadow_path = str(config_path) + str(shadow_directory)
			shadow_file = str(shadow_path) + "/" + str(prefix_to_shadow_file) + str(file_name)
			with open(str(shadow_file), "r") as shadow_config:
				shadow_index = shadow_config.read()
			now_index = int(shadow_index)
		except:
			now_index = 0
	else:
		now_index = 0
		
	# Read file with urls
	urls_list = []
	with open(str(path_to_urls_list), "r") as urls_file_list:
		urls_dirty = urls_file_list.readlines()
		for url in urls_dirty:
			true_url = re.sub("\n", "", str(url))
			urls_list.append(str(true_url))
	urls_list.append("FINISH")
	
	# Config writer
	def config_writer(now_index):
		config_path = str(case_path) + str(conf_directory)
		shadow_path = str(config_path) + str(shadow_directory)
		shadow_file = str(shadow_path) + "/" + str(prefix_to_shadow_file) + str(file_name)
		try:
			os.system(f"mkdir {str(shadow_path)}")
		except:
			pass
		with open(str(shadow_file), "w") as shadow_config:
			shadow_config.write(str(now_index))
	
	# First screen
	def first_screen():
		color_init("default_colorschemes")
		execute("clear")
		for element in urls_list:
			if element == urls_list[int(now_index)]:
				color_init("coursor_colorschemes")
				printer(f"  [+]---> {str(element)}")
				color_init("default_colorschemes")
			else:
				printer(f"  [-] {str(element)}")
		
	# Reactions on button
	def on_press(key):
		shower_gel = True
		global now_index, saved_index
		execute("clear")
		
		if key == keyboard.Key.enter:
			elements_number = int(len(urls_list)) - 1
			if int(now_index) >= elements_number:
				driver_close(driver)
				if conf_status == True:
					config_writer(0)
				listener.stop()
			else:
				execute("clear")
				try:
					get_url(driver, str(urls_list[int(now_index)]))
				except:
					errors_index.append(str(urls_list[int(now_index)]))
					errors_index.append(str(urls_list[int(now_index)-1]))
					error_file_name = str(case_path) + "/"  + str(prefix_to_error_file) + str(file_name)
					with open(str(error_file_name), "a") as error_file:
						error_file.write(str(urls_list[int(now_index)]) + "\n")
						error_file.write(str(urls_list[int(now_index)-1]) + "\n")
				execute("clear")
				now_index += 1
			
		elif key == keyboard.Key.esc:
			shower_gel = False
			driver_close(driver)
			if conf_status == True:
				config_writer(now_index)
				listener.stop()
			listener.stop()
			
		elif key == keyboard.Key.space:
			try:
				save_file_name = str(case_path) + "/" + str(prefix_to_save_file) + str(file_name)
				with open(str(save_file_name), "a") as save_file:
					save_file.write(str(urls_list[int(now_index)-1]) + "\n")
				saved_index.append(urls_list[int(now_index)-1])
			except:
				save_file_name = str(prefix_to_save_file) + str(file_name)
				with open(str(save_file_name), "a") as save_file:
					save_file.write(str(urls_list[int(now_index)-1]) + "\n")
				saved_index.append(urls_list[int(now_index)-1])
		
		if shower_gel == True:
			for element in urls_list:
				if element == urls_list[int(now_index)]:
					color_init("coursor_colorschemes")
					printer(f"  [+]---> {str(element)}")
					color_init("default_colorschemes")
				elif element in saved_index:
					print()
					color_init("A_colorschemes")
					printer(f"  [S]=> {str(element)}")
					color_init("default_colorschemes")
				elif element in errors_index:
					print()
					color_init("B_colorschemes")
					printer(Back.RED + Fore.BLACK + f"  [E]=> {str(element)}")
					color_init("default_colorschemes")
				else:
					printer(f"  [-] {str(element)}")
			
	# Start fist screen
	first_screen()
	# Button checker
	with keyboard.Listener(on_press=on_press) as listener:
		try:
			listener.join()
		except:
			pass
	# EXIT
	try:
		listener = keyboard.Listener(on_press=on_press)
		listener.start()
	except:
		pass
	try:
		listener.stop()
	except:
		pass
