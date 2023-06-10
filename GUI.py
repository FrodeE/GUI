from tkinter import *
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
import os
import re
import subprocess
import time
from pynput import keyboard
from multiprocessing import Process
import threading

#MULTIPROCESSING FUNCTIONS

current = set()
start = None
is_main_thread_active = lambda : any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())
save = 0

COMBINATIONS = [{keyboard.Key.f9},
{keyboard.Key.f10}]

start_hotkey = [{keyboard.Key.f9}]
stop_hotkey = [{keyboard.Key.f10}]

def on_press(key):
	if any([key in COMBO for COMBO in COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in start_hotkey):
			execute_start()
		if any(all(k in current for k in COMBO) for COMBO in stop_hotkey):
			execute_stop()

def hotkeys():
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()
		#is_main_thread_active()
		#threading.main_thread().is_alive()

def on_release(key):
	if any([key in COMBO for COMBO in stop_hotkey]):
		current.remove(key)

def start_bot():
	global start
	start = subprocess.Popen(['Python', 'launcher.py'])

def stop_bot():
	start.kill()

def execute_start():
	start = subprocess.Popen(['Python', 'launcher.py'])
	print(start)

def execute_stop():
	print(start)
	#start.kill()

def main():
	#VARIABLES
	HEIGHT = 400
	WIDTH = 750
	Config = None
	preconfigured_positions = ["2, 25, 21, 27, 23, 26, 4, 24",
	 "21, 1, 4, 24, 2, 3, 27, 5", "4, 7, 27, 24, 0, 2, 26, 21",
	 "27, 1, 21, 2, 14, 3, 26, 0"]
	

	#ROOT AND CANVAS
	root = tk.Tk()
	root.title('FAAKbot')
	root.iconbitmap('faakbotlogo.ico')

	canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
	canvas.pack()

	#CHECK IF CONFIG ALREADY EXISTS
	config_exists = Path("./config.txt")

	if config_exists.is_file():
		Config = True #config exists
		print("Config already exists!\n")
	else:
		Config = False #config does not exist
		print("Config does not exist!\n")

	#FUNCTIONS
	#READ DEFAULT CONFIG
	def default_config():
		with open("default_config.txt", "r") as default_config_file:
			def_conf = []
			for line in default_config_file:
				def_conf.append(line)
		return def_conf

	def start_or_no(decider):
		if decider == 1:
			start_bot()

	#GET A LIST OF CHAMPIONS IN DEFAULT CONFIG
	def default_champs():
		count = 0
		with open("default_config.txt", "r") as default_config_file:
			def_champs = []
			lines_of_champs = int(fn_build_count)-1
			for line in default_config_file:
				if count <= int(lines_of_champs):
					def_champs.append(line)
				count += 1
		return def_champs

	#FIND OUT HOW MANY LINES OF CHAMPS ARE IN CONFIG
	def build_count():
		with open("default_config.txt", "r") as default_config_file:
			builds = 0
			for line in default_config_file:
				if (',' in line):
					builds += 1
		return builds

	#FIND OUT THE META NAME THAT WAS SELECTED
	def meta_build_name():
		meta_name = metabuilds.get(metabuilds.curselection())
		return meta_name.split("- ",1)[1]

	#GET FULL META CHAMPIONS LIST
	def meta_build_list():
		with open("default_config.txt", "r") as default_config_file:
			meta_list = []
			for line in default_config_file:
				if (',' in line and '-' in line):
					line = line.rstrip("\n")
					meta_list.append(line.split('- ',1)[1])
		return meta_list

	#MATCHING SELECTED META WITH THE ONE FROM CONFIG LIST AND GETTING PLACEMENT
	def meta_find_placement(meta_name, meta_list):
		length = len(meta_list)
		placement_to_config = []
		for i in range(length):
			if meta_name == meta_list[i]:
				placement_to_config = preconfigured_positions[i]
		return placement_to_config

	def format_numbers(string):
		is_correct = 0
		if string.isdigit():
			is_correct = 1
		else:
			is_correct = 0
		return is_correct

	def format_placement(string):
		is_correct = 0
		pattern = re.compile(r'\d+(?:, \d+)*')
		if  re.fullmatch(pattern, string):
			is_correct = 1
		return is_correct

	#SAVING CONFIG AFTER PRESSING START OR SAVE CHANGES
	def save_data_start():
		fn_format_numbers_until_break = format_numbers(entry_until_break.get())
		fn_format_numbers_break_time = format_numbers(entry_break_time.get())
		fn_format_numbers_max_games = format_numbers(entry_max_games.get())
		fn_format_numbers_until_buy = format_numbers(entry_until_buy.get())

		with open("config.txt", "w") as conf:
			if (len(entry_placement.get()) == 0 and len(entry_until_break.get()) is not None and len(entry_break_time.get()) is not None and len(entry_max_games.get()) is not None and len(entry_until_buy.get()) is not None and metabuilds.curselection()):
				if('-' in  metabuilds.get(metabuilds.curselection())):
					if len(entry_until_break.get()) == 0 or len(entry_break_time.get()) == 0 or len(entry_max_games.get()) == 0 or len(entry_until_buy.get()) == 0 or not metabuilds.curselection():
						messagebox.showerror("ERROR!", "YOU FORGOT TO ENTER SOMETHING!")
						yes = 0
						start_or_no(yes)
					else:
						if (fn_format_numbers_until_break == 1 and fn_format_numbers_break_time == 1 and fn_format_numbers_max_games == 1 and fn_format_numbers_until_buy == 1): #VALITUD BUILD, PLACEMENT PUUDUB
							#SIIA FUNKTSIOON ETTENAHTUD PLACEMENTILE
							fn_meta_build_name = meta_build_name()
							fn_meta_build_list = meta_build_list()
							fn_meta_find_placement = meta_find_placement(fn_meta_build_name, fn_meta_build_list)
							
							#PUT TO CONFIG
							conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
							conf.write(fn_meta_find_placement + "\n")
							conf.write(entry_until_break.get() + "\n")
							conf.write(entry_break_time.get() + "\n")
							conf.write(entry_max_games.get() + "\n")
							conf.write(entry_until_buy.get() + "\n")
							yes = 1
							start_or_no(yes)
							
						else:
							messagebox.showerror("ERROR!", "YOU ARE USING WRONG FORMAT!")
							yes = 0
							start_or_no(yes)
				elif len(entry_until_break.get()) == 0 or len(entry_break_time.get()) == 0 or len(entry_max_games.get()) == 0 or len(entry_until_buy.get()) == 0 or not metabuilds.curselection():
					messagebox.showerror("ERROR!", "YOU FORGOT TO ENTER SOMETHING!")
					yes = 0
					start_or_no(yes)
				else:
					messagebox.showerror("ERROR!", "NOT USING META BUILD! PLACEMENT MUST BE SET!")
					yes = 0
					start_or_no(yes)
			elif (len(entry_placement.get()) is not None and len(entry_until_break.get()) is not None and len(entry_break_time.get()) is not None and len(entry_max_games.get()) is not None and len(entry_until_buy.get()) is not None and metabuilds.curselection()): #VALITUD BUILD, SISESTATUD PLACEMENT
				
				if('-' in  metabuilds.get(metabuilds.curselection()) and ',' in metabuilds.get(metabuilds.curselection())): 
					messagebox.showinfo("Important!", "Since you chose preconfigured build, default placements will be used!")
					if (fn_format_numbers_until_break == 1 and fn_format_numbers_break_time == 1 and fn_format_numbers_max_games == 1 and fn_format_numbers_until_buy == 1):
						fn_meta_build_name = meta_build_name()
						fn_meta_build_list = meta_build_list()
						fn_meta_find_placement = meta_find_placement(fn_meta_build_name, fn_meta_build_list)
						conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
						conf.write(fn_meta_find_placement + "\n")
						conf.write(entry_until_break.get() + "\n")
						conf.write(entry_break_time.get() + "\n")
						conf.write(entry_max_games.get() + "\n")
						conf.write(entry_until_buy.get() + "\n")
						yes = 1
						start_or_no(yes)
					else:
						messagebox.showerror("ERROR!", "YOU ARE USING WRONG FORMAT!")
						yes = 0
						start_or_no(yes)
				else: #TAVALINE; PLACEMENT CUSTOM, BUILD CUSTOM
					fn_format_placement = format_placement(entry_placement.get())
					if fn_format_placement == 1:
						conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
						conf.write(entry_placement.get() + "\n")
						conf.write(entry_until_break.get() + "\n")
						conf.write(entry_break_time.get() + "\n")
						conf.write(entry_max_games.get() + "\n")
						conf.write(entry_until_buy.get() + "\n")
						yes = 1
						start_or_no(yes)
					else:
						messagebox.showerror("ERROR!", "YOU ARE USING WRONG FORMAT!")
						yes = 0
						start_or_no(yes)

	def save_data_save():
		fn_format_numbers_until_break = format_numbers(entry_until_break.get())
		fn_format_numbers_break_time = format_numbers(entry_break_time.get())
		fn_format_numbers_max_games = format_numbers(entry_max_games.get())
		fn_format_numbers_until_buy = format_numbers(entry_until_buy.get())

		with open("config.txt", "w") as conf:
			if (len(entry_placement.get()) == 0 and len(entry_until_break.get()) is not None and len(entry_break_time.get()) is not None and len(entry_max_games.get()) is not None and len(entry_until_buy.get()) is not None and metabuilds.curselection()):
				if('-' in  metabuilds.get(metabuilds.curselection())):
					if len(entry_until_break.get()) == 0 or len(entry_break_time.get()) == 0 or len(entry_max_games.get()) == 0 or len(entry_until_buy.get()) == 0 or not metabuilds.curselection():
						messagebox.showerror("ERROR!", "YOU FORGOT TO ENTER SOMETHING!")
					else:
						if (fn_format_numbers_until_break == 1 and fn_format_numbers_break_time == 1 and fn_format_numbers_max_games == 1 and fn_format_numbers_until_buy == 1): #VALITUD BUILD, PLACEMENT PUUDUB
							#SIIA FUNKTSIOON ETTENAHTUD PLACEMENTILE
							fn_meta_build_name = meta_build_name()
							fn_meta_build_list = meta_build_list()
							fn_meta_find_placement = meta_find_placement(fn_meta_build_name, fn_meta_build_list)
							
							#PUT TO CONFIG
							conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
							conf.write(fn_meta_find_placement + "\n")
							conf.write(entry_until_break.get() + "\n")
							conf.write(entry_break_time.get() + "\n")
							conf.write(entry_max_games.get() + "\n")
							conf.write(entry_until_buy.get() + "\n")
							
						else:
							messagebox.showerror("ERROR!", "YOU ARE USING WRONG FORMAT!")

				elif len(entry_until_break.get()) == 0 or len(entry_break_time.get()) == 0 or len(entry_max_games.get()) == 0 or len(entry_until_buy.get()) == 0 or not metabuilds.curselection():
					messagebox.showerror("ERROR!", "YOU FORGOT TO ENTER SOMETHING!")
				else:
					messagebox.showerror("ERROR!", "NOT USING META BUILD! PLACEMENT MUST BE SET!")
			elif (len(entry_placement.get()) is not None and len(entry_until_break.get()) is not None and len(entry_break_time.get()) is not None and len(entry_max_games.get()) is not None and len(entry_until_buy.get()) is not None and metabuilds.curselection()): #VALITUD BUILD, SISESTATUD PLACEMENT
				
				if('-' in  metabuilds.get(metabuilds.curselection()) and ',' in metabuilds.get(metabuilds.curselection())): 
					messagebox.showinfo("Important!", "Since you chose preconfigured build, default placements will be used!")
					if (fn_format_numbers_until_break == 1 and fn_format_numbers_break_time == 1 and fn_format_numbers_max_games == 1 and fn_format_numbers_until_buy == 1):
						fn_meta_build_name = meta_build_name()
						fn_meta_build_list = meta_build_list()
						fn_meta_find_placement = meta_find_placement(fn_meta_build_name, fn_meta_build_list)
						conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
						conf.write(fn_meta_find_placement + "\n")
						conf.write(entry_until_break.get() + "\n")
						conf.write(entry_break_time.get() + "\n")
						conf.write(entry_max_games.get() + "\n")
						conf.write(entry_until_buy.get() + "\n")
					else:
						messagebox.showerror("ERROR!", "YOU ARE USING WRONG FORMAT!")
				else: #TAVALINE; PLACEMENT CUSTOM, BUILD CUSTOM
					fn_format_placement = format_placement(entry_placement.get())
					if fn_format_placement == 1:
						conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
						conf.write(entry_placement.get() + "\n")
						conf.write(entry_until_break.get() + "\n")
						conf.write(entry_break_time.get() + "\n")
						conf.write(entry_max_games.get() + "\n")
						conf.write(entry_until_buy.get() + "\n")
					else:
						messagebox.showerror("ERROR!", "YOU ARE USING WRONG FORMAT!")

			elif len(entry_until_break.get()) == 0 or len(entry_break_time.get()) == 0 or len(entry_max_games.get()) == 0 or len(entry_until_buy.get()) == 0 or not metabuilds.curselection():
				messagebox.showerror("ERROR!", "EVERY LINE NEEDS TO HAVE ENTRIES!")
			else:
				conf.write(metabuilds.get(metabuilds.curselection()) + "\n")
				conf.write(entry_placement.get() + "\n")
				conf.write(entry_until_break.get() + "\n")
				conf.write(entry_break_time.get() + "\n")
				conf.write(entry_max_games.get() + "\n")
				conf.write(entry_until_buy.get() + "\n")


	#IMAGES
	fn_default_config = default_config()
	fn_build_count = build_count()
	fn_default_champs = default_champs()

	print("LIST: " + str(fn_default_config))
	print("Amount of champion build lines: " + str(fn_build_count))

	background_image = tk.PhotoImage(file='background_new.png')
	background_label = tk.Label(root, image=background_image)
	background_label.place(x=0,y=0, relwidth=1, relheight=1)

	logo_image = tk.PhotoImage(file='logo4.png')
	logo_label = tk.Label(root, image =logo_image)
	logo_label.place(relx=0,rely=0, relwidth=0.4, relheight=0.2)

	#CREATE FRAME FOR LISTBOX
	metabuilds_frame = Frame(root)
	metabuilds_scrollbar = Scrollbar(metabuilds_frame, orient=VERTICAL)

	#LISTBOX
	metabuilds = Listbox(metabuilds_frame, width=88, borderwidth=2, relief="sunken", 
		yscrollcommand=metabuilds_scrollbar.set, bg='#45ADA8', fg= 'white')
	metabuilds.place(relx=0.22, rely=0.28, relwidth=0.50, relheight=0.09)
	for item in fn_default_champs:
		strip_item = item
		strip_item = strip_item.rstrip("\n")
		metabuilds.insert(0, strip_item)

	#LISTBOX CONF
	metabuilds_scrollbar.config(command=metabuilds.yview)
	metabuilds_scrollbar.pack(side=RIGHT, fill=Y)
	metabuilds_frame.place(relx=0.22, rely=0.28, relwidth=0.68, relheight=0.09)
	metabuilds.pack()

	#BUTTONS AND ENTRIES
	button_start = tk.Button(root, text="Start FAAKbot", bg ='#45ADA8', fg = 'white', command=lambda:[save_data_start()])
	button_start.place(relx=0.5, rely=0.56, relwidth=0.15, relheight=0.1)

	button_save = tk.Button(root, text="Save changes", bg ='#45ADA8', fg = 'white', command=lambda:[save_data_save()])
	button_save.place(relx=0.5, rely=0.83, relwidth=0.15, relheight=0.1)

	label_champs = tk.Label(root, text ="Buy these champions", borderwidth=2, relief="groove", bg = '#6CB9E3', fg = 'black')
	label_champs.place(relx=0.02, rely=0.28, relwidth=0.18, relheight=0.08)

	label_until_break = tk.Label(root, text ="Stop bot after .. games", borderwidth=2, relief="groove", bg = '#6CB9E3', fg = 'black')
	label_until_break.place(relx=0.02, rely=0.38, relwidth=0.18, relheight=0.08)

	#NUMBER II ENTRY
	entry_until_break = tk.Entry(root, borderwidth=2, relief="sunken", bg='#45ADA8', fg= 'white')
	entry_until_break.place(relx=0.22, rely=0.38, relwidth=0.20, relheight=0.08)
	strip_until_break = fn_default_config[fn_build_count]
	strip_until_break = strip_until_break.rstrip("\n")
	entry_until_break.insert(END, strip_until_break)

	label_break_time = tk.Label(root, text ="Break time in minutes", borderwidth=2, relief="groove", bg = '#6CB9E3', fg = 'black')
	label_break_time.place(relx=0.02, rely=0.48, relwidth=0.18, relheight=0.08)

	#NUMBER III ENTRY
	entry_break_time = tk.Entry(root, borderwidth=2, relief="sunken", bg='#45ADA8', fg= 'white')
	entry_break_time.place(relx=0.22, rely=0.48, relwidth=0.20, relheight=0.08)
	strip_break_time = fn_default_config[fn_build_count+1]
	strip_break_time = strip_break_time.rstrip("\n")
	entry_break_time.insert(END, strip_break_time)

	label_max_games = tk.Label(root, text ="Max. amount of games", borderwidth=2, relief="groove", bg = '#6CB9E3', fg = 'black')
	label_max_games.place(relx=0.02, rely=0.58, relwidth=0.18, relheight=0.08)

	#NUMBER IV ENTRY
	entry_max_games = tk.Entry(root, borderwidth=2, relief="sunken", bg='#45ADA8', fg= 'white')
	entry_max_games.place(relx=0.22, rely=0.58, relwidth=0.20, relheight=0.08)
	strip_max_games = fn_default_config[fn_build_count+2]
	strip_max_games = strip_max_games.rstrip("\n")
	entry_max_games.insert(END, strip_max_games)

	label_until_buy = tk.Label(root, text ="Start buying after .. credits", borderwidth=2, relief="groove", bg = '#6CB9E3', fg = 'black')
	label_until_buy.place(relx=0.02, rely=0.68, relwidth=0.20, relheight=0.08)

	#NUMBER V ENTRY
	entry_until_buy = tk.Entry(root, borderwidth=2, relief="sunken", bg='#45ADA8', fg= 'white')
	entry_until_buy.place(relx=0.24, rely=0.68, relwidth=0.18, relheight=0.08)
	strip_until_buy = fn_default_config[fn_build_count+3]
	strip_until_buy = strip_until_buy.rstrip("\n")
	entry_until_buy.insert(END, strip_until_buy)

	label_placement = tk.Label(root, text ="Placement", borderwidth=2, relief="groove", bg = '#6CB9E3', fg = 'black')
	label_placement.place(relx=0.02, rely=0.78, relwidth=0.20, relheight=0.08)

	#NUMBER VI ENTRY
	entry_placement = tk.Entry(root, borderwidth=2, relief="sunken", bg='#45ADA8', fg= 'white')
	entry_placement.place(relx=0.24, rely=0.78, relwidth=0.18, relheight=0.08)

	button_stop = tk.Button(root, text="Stop FAAKbot", command=lambda:[stop_bot()], bg ='#45ADA8', fg = 'white')
	button_stop.place(relx=0.5, rely=0.7, relwidth=0.15, relheight=0.1)
	
	p = Process(target=hotkeys)
	p.start()

	root.mainloop()


if __name__ == '__main__':
	
	main()
	threading.main_thread().is_alive()
	