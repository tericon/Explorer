from Transformations.Explorer import browint
from Default import aliuminium as interface
from Default.aliuminium import pm
from time import sleep
from os import system
import re
from Default.selenium_support import *
from Transformations.Explorer.explorer_config import *


# EXPLORER CONFIG
path_to_urls_file = default_path_to_urls_file
browser_session = default_browser_session

config_file = "False"
config_status = "False"

# INITIALIZATION
def initialization(choice, debug=True):
	if debug:
		input()

	if str(choice) == "BACK":
		first_screen()
	elif str(choice) == "Auto mode":
		auto_mode()
	elif str(choice) == "Open file with urls":
		open_file_with_urls()
	elif str(choice) == "Open browser and return session":
		open_browser_session()
	elif str(choice) == "START AUTO MODE":
		start_auto_mode()
	elif str(choice) == "Change config status":
		change_config_status()
	elif str(choice) == "Default mode":
		default_mode()
	elif str(choice) == "Set file with urls":
		set_file_with_urls()
	elif str(choice) == "Start browser and return session":
		start_browser_and_return_session()
	elif str(choice) == "START DEFAULT MODE":
		start_default_mode()

# SETS
def set_urls_file():
	global path_to_urls_file
	path_to_urls_file = pm(logo = "Select file with urls")
	
def set_browser_session():
	global browser_session
	system("clear")
	print()
	browser_session = get_driver(debug=True)
	system("clear")
	input("\n\n  [PRESS ENTER - CONTINUE]")
	
# START DEFAULT MODE
def start_default_mode():
	browint.search(path_to_urls_list=path_to_urls_file, driver=browser_session)
	finish_process()

# SET FILE WITH URLS (DEFAULT)
def set_file_with_urls():
	set_urls_file()
	initialization("Default mode")
	
# START BROWSER AND RETURN SESSION (DEFAULT)
def start_browser_and_return_session():
	set_browser_session()
	initialization("Default mode", debug=False)
	
# DEFAULT MODE
def default_mode():
	logo = "Default mode"
	boards = [f"Path to file with urls = {str(path_to_urls_file)}"]
	items = ["Set file with urls", "Start browser and return session", "START DEFAULT MODE", "BACK"]
	spaces = [2]
	choice = interface.window(items=items, spaces=spaces, logo=logo, boards=boards)
	initialization(choice)

# CHANGE CONFIG STATUS
def change_config_status():
	logo = "Use Config?"
	items = ["True", "False"]
	choice = interface.window(items=items, logo=logo)
	
	case_path = re.sub(r"/.*", "", str(path_to_urls_file))
	config_path = str(case_path) + "/conf_data"
	config_file_path = str(config_path) + "/case_conf.lst"
	if str(choice) == "True":
		with open(str(config_file_path), "w") as new_status:
			new_status = new_status.write("True")
	elif str(choice) == "False":
		with open(str(config_file_path), "w") as new_status:
			new_status = new_status.write("False")
	initialization("Auto mode")
	
# CONFIG CHECK
def check_config_file():
	global config_status, config_file
	case_path = re.sub(r"/.*", "", str(path_to_urls_file))
	config_path = str(case_path) + "/conf_data"
	config_file_path = str(config_path) + "/case_conf.lst"
	try:
		status = open(str(config_file_path), "r")
		config_file = "True"
		config_status = status.read()
		status.close()
	except:
		config_status = "False"


# FINISH PROCESS
def finish_process(lable = None):
	logo = lable
	items = ["BACK"]
	choice = interface.window(items=items, logo=logo)
	if choice == "BACK":
		initialization(choice)
		
# START AUTO MODE
def start_auto_mode():
	send_conf = False
	if str(config_status) == "True":
		send_conf = True
	browint.auto_search(path_to_urls_list=path_to_urls_file, driver=browser_session, conf_status=send_conf)
	finish_process()
	
# OPEN FILE WITH URLS
def open_file_with_urls():
	set_urls_file()
	initialization("Auto mode")
	
# OPEN BROWSER AND SAVE SESSION
def open_browser_session():
	set_browser_session()
	initialization("Auto mode", debug=False)

# AUTO MODE
def auto_mode():
	check_config_file()
	if config_file == "False":
		logo = "Auto mode"
		boards = [f"Path to file with urls = {str(path_to_urls_file)}"]
		items = ["Open file with urls", "Open browser and return session", "START AUTO MODE", "BACK"]
		spaces = [2]
		choice = interface.window(items=items, spaces=spaces, logo=logo, boards=boards)
		initialization(choice)
	elif config_file == "True":
		logo = "Auto mode"
		boards = [f"Path to file with urls = {str(path_to_urls_file)}", f"Config file = {str(config_file)}", f"Use case config = {str(config_status)}"]
		items = ["Open file with urls", "Open browser and return session", "Change config status", "START AUTO MODE", "BACK"]
		spaces = [3]
		choice = interface.window(items=items, spaces=spaces, logo=logo, boards=boards)
		initialization(choice)

# FIRST SCREEN
def first_screen():
	logo = "Explorer"
	items = ["Auto mode", "Default mode", "EXIT"]
	spaces = [2]
	choice = interface.window(items=items, spaces=spaces, logo=logo)
	initialization(choice)
