  #import modules
from __future__ import division
from time import localtime, strftime
from numpy import array, append, resize, set_printoptions
from math import pow, sqrt
import time; import viz; import viztask; import vizinfo
import vizmat; import vizact; import vizjoy
#launch vizard and enable physics and joystick
viz.go(viz.FULLSCREEN); viz.phys.enable(); joy = vizjoy.add()

#disable numpy array printing threshold
set_printoptions(threshold='nan')

#define globals
coordinate_array = array([]); movement_time = 0; trial_number = 0; sub_trial_number = 0
collide_coords = []; subject_id_data = 0; signal = viztask.Signal(); maze = ''; maze_root = ''; condition = 0
end_coords = (); status = 0; time_signal = viztask.Signal(); phase = ''; trial_time = 0; trial_object = ''
start_coords = (); start_ori = ();

def get_subject_info():

	#create an input box for entering experiment information
	input_box = vizinfo.add('')
	input_box.title('Subject Info')
	input_box.scale(2,2)
	input_box.translate(0.85,0.65)
	input_box.drag(viz.OFF)

	#create inpux box and handles
	subject_id = input_box.add(viz.TEXTBOX,'Subject ID')
	experimenter = input_box.add(viz.TEXTBOX,'Experimenter')
	start_button = input_box.add(viz.BUTTON,'Continue')

	#wait until the start button is pressed
	yield viztask.waitButtonDown(start_button)

	#get the data from the input box
	global subject_id_data
	subject_id_data = subject_id.get()
	experimenter_data = experimenter.get()

	input_box.remove()

	#get the date
	date = strftime("%m/%d/%Y",localtime())

	#write out information

	output = open(str(subject_id_data) + '.txt' ,'a')
	output.write('Subject ID: ' + str(subject_id_data))
	output.write('\n' + 'Experimenter: ' + str(experimenter_data))
	output.write('\n' + 'Date: ' + str(date))
	output.close()


def task_choice():
	
	#ensure that the mouse is turned on
	viz.mouse(viz.ON); viz.mouse.setVisible(viz.ON);
	
	#load condition_box
	condition_box = vizinfo.add(''); condition_box.title('SNAP')
	condition_box.scale(2,2); condition_box.translate(0.85,0.65); condition_box.drag(viz.OFF)
	
	#add different options
	condition_one = condition_box.add(viz.BUTTON,'Condition 1')
	condition_two = condition_box.add(viz.BUTTON,'Condition 2')
	practice = condition_box.add(viz.BUTTON,'Practice Program')
	expertise = condition_box.add(viz.BUTTON,'Visuomotor Expertise Program')
	maze_quit = condition_box.add(viz.BUTTON,'Quit Maze Program')
	
	#add variables for user chocies
	condition_one_pressed = viztask.waitButtonDown(condition_one)
	condition_two_pressed = viztask.waitButtonDown(condition_two)
	practice_pressed = viztask.waitButtonDown(practice)
	expertise_pressed = viztask.waitButtonDown(expertise)
	maze_quit_pressed = viztask.waitButtonDown(maze_quit)
	
	#data variable to hold user choices
	data = viz.Data()

	#setup globals
	global condition; global maze_root; global start_coords; global start_ori; global end_coords;
	
	#While statment that will run a different maze based on user choice.
	#Will keep looping until the user selects quit and ends the program
	while True:
		yield viztask.waitAny([condition_one_pressed,condition_two_pressed,practice_pressed,
								expertise_pressed,maze_quit_pressed],data)
		condition_box.remove()
		if data.condition is condition_one_pressed:
			condition = 1
			yield maze_choice(); yield run_condition_one(); yield task_choice()
		elif data.condition is condition_two_pressed:
			condition = 2
			yield maze_choice(); yield run_condition_two(); yield task_choice()
		elif data.condition is practice_pressed:
			viz.mouse(viz.OFF); viz.mouse.setVisible(viz.OFF)
			maze_root = 'C:\Experiments\AMBI2016\SNAP\Programs_Environments\\SNAP\Programs_Environments\PMS'; start_coords = (0,40,0); start_ori = (3.5,0,0);
			yield practice_maze(); yield task_choice()
		elif data.condition is expertise_pressed:
			viz.mouse(viz.OFF); viz.mouse.setVisible(viz.OFF)
			maze_root = 'C:\Experiments\AMBI2016\SNAP\Programs_Environments\VMS'; start_coords = (0,40,0); start_ori = (0,0,0); end_coords = [1150,1275,-190,-100];
			yield expertise_maze(); yield task_choice()
		elif data.condition is maze_quit_pressed:
			viz.quit()

	viz.quit()
	
def maze_choice():
	
	#load start box
	choice_box = vizinfo.add(''); choice_box.title('Maze Choice')
	choice_box.scale(2,2); choice_box.translate(0.85,0.65); choice_box.drag(viz.OFF)
	
	#add options for different mazes
	maze_a = choice_box.add(viz.BUTTON,'Maze Layout A')
	maze_b = choice_box.add(viz.BUTTON,'Maze Layout B')
	
	#add variables for user chocies
	maze_a_pressed = viztask.waitButtonDown(maze_a)
	maze_b_pressed = viztask.waitButtonDown(maze_b)
	
	#data variable to hold user choices
	data = viz.Data()
	
	
	#get the maze name root, and start/end coordinates from user choice
	global maze_root; global start_coords; global start_ori; global end_coords
	yield viztask.waitAny( [ maze_a_pressed, maze_b_pressed ], data )
	if data.condition is maze_a_pressed:
		choice_box.remove(); yield phase_choice()
		maze_root = 'C:\Experiments\AMBI2016\SNAP\Programs_Environments\SNAPMazeA'; start_coords = (0,40,0); start_ori = (0,0,0); end_coords = (-745,-700,2125,2180)
	elif data.condition is maze_b_pressed:
		choice_box.remove(); yield phase_choice()
		maze_root = 'C:\Experiments\AMBI2016\SNAP\Programs_Environments\SNAPMazeB'; start_coords = (-1114,40,2151); start_ori = (-180,0,0); end_coords = (-1876,-1795,115,156)

	
	
	#turn the mouse off so it doesn't interfere with the environment
	viz.mouse(viz.OFF); viz.mouse.setVisible(viz.OFF)
	
def phase_choice():
	#load start box
	choice_box = vizinfo.add(''); choice_box.title('Phase Choice')
	choice_box.scale(2,2); choice_box.translate(0.85,0.65); choice_box.drag(viz.OFF)
	
	#add options for different mazes
	learning_phase = choice_box.add(viz.BUTTON,'Learning')
	testing_phase = choice_box.add(viz.BUTTON,'Testing')
	
	#add variables for user chocies
	learning_phase_pressed = viztask.waitButtonDown(learning_phase)
	testing_phase_pressed = viztask.waitButtonDown(testing_phase)
	
	#data variable to hold user choices
	data = viz.Data()
	
	global phase_selection
	yield viztask.waitAny( [ learning_phase_pressed, testing_phase_pressed ], data )
	if data.condition is learning_phase_pressed:
		phase_selection = 'Learning'
		choice_box.remove()
	elif data.condition is testing_phase_pressed:
		phase_selection = 'Testing'
		choice_box.remove()
	
def run_condition_one():
	
	#declare globals
	global collide_coords; global movement_time; global coordinate_array; global trial_number; global sub_trial_number
	global maze; global phase; global trial_time

	################
	#Learning Phase#
	################
	#phase = 'Learning'
	
	
	#setup viewpoint and positioning
	yield setup_view()
	
	
	#Setup the object for "collision"
	collide_coords = end_coords;
	
	if phase_selection is 'Learning':
		phase = 'Learning'
		#Setup, but do not load maze
		maze_name = maze_root + 'arrows.IVE'
		maze = viz.add(maze_name); maze.visible(viz.OFF)
		
		#loop through the four learning trials
		for trial in range(1,5):
			
			trial_number = trial; sub_trial_number = 1
			
			#show user instructions
			instructions = viz.addText('Trial ' + str(trial) + ': Please follows the arrows',viz.SCREEN);
			instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
			yield viztask.waitKeyDown('m');
			yield instructions.remove()

			#show user fixation cross
			yield display_fix()
			
			#load maze
			yield maze.visible(viz.ON)
			
			#clear coordinate_array so that previous trial data is gone
			coordinate_array = array([])
			
			#enable events
			joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON);
			quit_onkey.setEnabled(viz.ON); pos_move_timer.setEnabled(viz.ON); time_timer.setEnabled(viz.ON)
			
			#reset and start both the movement time and the total trial time
			movement_time = TickTockTimer(); movement_time.StartTimer(); trial_time = TickTockTimer(); trial_time.StartTimer()

			#Wait until timer signal has been sent.
			yield time_signal.wait()
			
			#disable events and write the data
			disable()
			write_trial_data()
			
			#turn maze off and then move
			maze.visible(viz.OFF)
			yield move()
			
			
		#remove maze
		maze.remove()
		
		#Display between phase instructions
		instructions = viz.addText('Please wait for the experimenter to give you more instructions.',viz.SCREEN);
		instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
		yield viztask.waitKeyDown('m')
		yield instructions.remove()
		
		phase = 'Testing'
	
	###############
	#Testing Phase#
	###############
	#remove the learning maze and setup testing maze
	
	maze_name = maze_root + 'noarrows.IVE'
	maze = viz.add(maze_name); maze.visible(viz.OFF)
	
	#loop through the three testing trials
	for trial in range(1,4):
		
		trial_number = trial
		
		#Show instructions and wait for user signal until they are removed
		instructions = viz.addText('Please navigate to the end of the maze',viz.SCREEN);
		instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
		yield viztask.waitKeyDown('m')
		yield instructions.remove()
		
		#display fixation
		yield display_fix()
		
		#turn maze on
		yield maze.visible(viz.ON)
		
		#clear the coordinate array
		coordinate_array = array([])
		
		#enable events
		joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON)
		quit_onkey.setEnabled(viz.ON); pos_timer.setEnabled(viz.ON); 
		
		#reset and start the clock
		movement_time = TickTockTimer(); movement_time.StartTimer();

		#wait for "collision" signal
		yield signal.wait()

		#disable all timers
		disable()
		write_trial_data()
		
		#turn maze off and then move
		maze.visible(viz.OFF)
		if trial != 4:
			yield move()
	
	maze.remove()


def run_condition_two():
	
	#declare globals
	global collide_coords; global movement_time; global coordinate_array
	global trial_number; global maze; global phase; global trial_object
	
	#setup collision destination
	collide_coords = end_coords
	
	################
	#Learning Phase#
	################
	#phase = 'Learning'
	
		
	#setup viewpoint and positioning
	yield setup_view()

	#setup maze for loading
	maze_name = maze_root + 'noarrows.IVE'
	maze = viz.add(maze_name); maze.visible(viz.OFF)
	if phase_selection is 'Learning':
		phase = 'Learning'
		#loop through each of the five learning phase trials
		for trial in range(1,5):
			
			trial_number = trial
			
			#Show instructions and wait for user signal until they are removed
			instructions = viz.addText('Please explore the maze.',viz.SCREEN);
			instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
			yield viztask.waitKeyDown('m')
			instructions.remove()
			
			#show user fixation cross
			yield display_fix()
			
			#turn maze on
			yield maze.visible(viz.ON)
			
			#load coordinate_array in clear it so that previous trial data is gone
			coordinate_array = array([])
			
			#enable events
			joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON)
			quit_onkey.setEnabled(viz.ON); pos_timer.setEnabled(viz.ON); 
			
			#reset and start the clock
			movement_time = TickTockTimer(); movement_time.StartTimer();

			#Wait for trial to expire
			yield viztask.waitTime(300)
			#yield viztask.waitTime(420)
			
			#disable all timers
			disable()
			write_trial_data()
			
			#turn maze off and then move
			maze.visible(viz.OFF)
			#if trial != 3:
			if trial != 5:
				yield move()
		
		#Display between phase instructions
		instructions = viz.addText('Please wait for the experimenter to give you more instructions.',viz.SCREEN);
		instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
		yield viztask.waitKeyDown('m')
		yield instructions.remove()
		
		phase = 'Testing'
		
	###############
	#Testing Phase#
	###############
	
	#setup maze start and end locations for each maze
	if maze_root == 'C:\Experiments\AMBI2016\SNAP\Programs_Environments\SNAPMazeA':
		#setup start location dictionary {Start Location:((Start Coordinates),(Start Orientation)),...}
		start_dic = {'A': ((-1049,40,1530),(0,0,0)), 'B': ((675,40,1814),(-90,0,0)), 'C': ((110,40,678),(0,0,0)), 'D': ((-725,40,2155),(-90,0,0)), 'E': ((0,40,0),(0,0,0)), 'F': ((-1040,0,670),(-180,0,0))}
		#setup object list (Object,Start Location,End Coordinates)
		objects = (  ('Table','C',(-710,-664,669,769)), ('Chair','A',(397,464,1784,1849)),('Round Stool','F',(148,174,1445,1480)), ('Rug','E',(-312,-259,1060,1130)), ('Mirror','B',(-330,259,730,755)), ('Wooden Basket','A',(-1070,-994,361,433)),\
					('Bench with cushions','B',(-316,-194,1784,1827)),('Coat Rack','D',(-675,-645,890,945)), ('Wooden Chest','E',(-1071,-1032,1170,1850)), ('Potted Plant','F',(-6,40,206,260)),  ('TV','D',(113,149,1013,1111)), ('Curtains','C',(-1070,-1022,1518,1538)) )
	elif maze_root == 'C:\Experiments\AMBI2016\SNAP\Programs_Environments\SNAPMazeB':
		#setup start location dictionary {Start Location:((Start Coordinates),(Start Orientation)),...}
		start_dic = {'A': ((-1835,40,1100),(0,0,0)), 'B': ((12,40,-10),(0,0,0)), 'C': ((-1114,40,2151),(-180,0,0)), 'D': ((-1835,40,545),(-180,0,0)), 'E': ((-1255,40,323),(-90,0,0)), 'F': ((410,40,737),(-90,0,0))}
		#setup object list (Object,Start Location,End Coordinates)
		objects = ( ('Purple Chair','C',(-223,-165,1030,1080)),('Round Table','E',(-381,-277,282,358)),('Fireplace','B',(-1873,-1854,289,371)), ('Long Table','A',(-1058,-951,634,669)), ('Dining Chair','F',(-854,-826,1003,1048)), ('Wall Lamp','E',(-1856,-1802,1057,1080)), \
		('Window','F',(-1519,-1440,1410,1433)), ('Umbrella Stand','D',(-678,-628,681,715)),('Vase','A',(-19,46,-57,-10)), ('Cabinet with Dishes','B',(-1290,-1251,1019,1201)), ('Floor Lamp','D',(-817,-772,1435,1491)), ('Rug','C',(-1600,-1510,667,715)) )
	else:
		print 'Maze ' + maze_root + ' not supported for condition 2 testing phase.'

	#loop through object/finish location
	trial_number = 1
	for object in objects:
		
		trial_object = object[1]
		
		#show user instructions
		instructions = viz.addText('Please navigate to the object displayed on the stand.',viz.SCREEN);
		instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
		yield viztask.waitKeyDown('m')
		instructions.remove()

		#show user fixation cross
		yield display_fix()

		#load coordinate_array, then clear it so that previous trial data is gone
		coordinate_array = array([])

		#set object specific finish location
		collide_coords = object[2];

		#set position and orientation 
		viz.MainView.setPosition(start_dic[object[1]][0],viz.ABS_GLOBAL)
		viz.MainView.setEuler((0,0,0),viz.ABS_GLOBAL)
		viz.MainView.setEuler(start_dic[object[1]][1],viz.BODY_ORI,viz.ABS_GLOBAL)

		#load the maze
		yield maze.visible(viz.ON)
			
		#enable events
		joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON)
		quit_onkey.setEnabled(viz.ON); pos_timer.setEnabled(viz.ON); 
			
		#reset and start the clock
		movement_time = TickTockTimer(); movement_time.StartTimer();

		#wait for "collision" signal
		yield signal.wait()

		#disable all timers
		disable()
		write_trial_data()
		
		#turn maze off and then move
		maze.visible(viz.OFF)
		if ( object != objects[len(objects)-1] ):
			yield move()
			trial_number = trial_number + 1
	maze.remove()

def practice_maze():

	#declare globals
	global coordinate_array; global movement_time; global maze;
	
	#Display instructions until they are removed
	practice_instructions = viz.addText('This practice session is designed to help you get used to\n using the joystick. Navigate through the hallways using\n the joystick until you are comfortable using to move.',viz.SCREEN)
	practice_instructions.fontSize(42)
	practice_instructions.setPosition(.5,.5)
	practice_instructions.alignment(viz.TEXT_CENTER_CENTER)
	yield viztask.waitKeyDown('m')
	practice_instructions.remove()

	#show user fixation cross
	yield display_fix()
	
	#setup viewpoint and positioning
	yield setup_view()

	#load the  maze
	maze_name = maze_root + '.IVE'; maze = viz.add(maze_name); maze.visible(viz.OFF); yield maze.visible(viz.ON)

	#load coordinate_array in clear it so that previous trial data is gone
	coordinate_array = array([])

	#enable all of the global events
	joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON);
	quit_onkey.setEnabled(viz.ON)

	#reset and start the clock
	movement_time = TickTockTimer(); movement_time.StartTimer();

	#stay in maze until experimenter presses a key...
	yield viztask.waitKeyDown('m')

	#disable events and quit maze
	disable()
	write_trial_data()
	maze.remove()

def expertise_maze():
 
	#setup viewpoint and positioning
	yield setup_view()
	
	#declare globals
	global signal; global collide_coords; global movement_time; global coordinate_array; global maze
	
	#clear the coordinate array
	coordinate_array = array([])
	
	#Setup the objection "collision"
	signal = viztask.Signal(); collide_coords = end_coords
	
	#Show instructions and wait for user signal until they are removed
	instructions = viz.addText('Please navigate to the blue wall',viz.SCREEN);
	instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
	yield viztask.waitKeyDown('m')
	instructions.remove()
	
	#show user fixation cross
	yield display_fix()
	
	#Load the maze
	maze_name = maze_root + '.IVE'; maze = viz.add(maze_name); maze.visible(viz.OFF); yield maze.visible(viz.ON)
				
	#enable all of the global events
	joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON);
	quit_onkey.setEnabled(viz.ON); pos_timer.setEnabled(viz.ON)
		
	#reset and start the clock
	movement_time = TickTockTimer(); movement_time.StartTimer();

	#wait for "collision" signal
	yield signal.wait()
	
	#disable and quit
	disable()
	write_trial_data()
	maze.remove()

def disable():
	joy_timer.setEnabled(viz.OFF); coor_timer.setEnabled(viz.OFF); pos_timer.setEnabled(viz.OFF);
	write_onkey.setEnabled(viz.OFF); quit_onkey.setEnabled(viz.OFF); pos_move_timer.setEnabled(viz.OFF)
	time_timer.setEnabled(viz.OFF)
	
def display_fix():

	fixation_cross = viz.addText('+',viz.SCREEN)
	fixation_cross.fontSize(72)
	fixation_cross.setPosition(.5,.5)
	yield viztask.waitTime(5)
	yield fixation_cross.remove()

def move():
		#move to origin
		viz.MainView.setPosition(start_coords,viz.ABS_GLOBAL)
		viz.MainView.setEuler((0,0,0),viz.ABS_GLOBAL)
		viz.MainView.setEuler(start_ori,viz.BODY_ORI,viz.ABS_GLOBAL)

def learn_move():
		
		#declare globals
		global sub_trial_number; global movement_time; global trial_time
		
		#stop the trial timer until we are back in the maze
		trial_time.Pause()
		
		#disable events and turn maze off
		disable();
		write_trial_data()
		yield maze.visible(viz.OFF)
		
		#Display the insturctions
		instructions = viz.addText('Please follow the arrows again.',viz.SCREEN);
		instructions.fontSize(42); instructions.setPosition(.5,.5); instructions.alignment(viz.TEXT_CENTER_CENTER)
		yield viztask.waitKeyDown('m');
		yield instructions.remove()

		#show user fixation cross
		yield display_fix()
		
		#move the viewpoint and turn maze back on
		yield move()
		yield maze.visible(viz.ON)

		#enable events
		joy_timer.setEnabled(viz.ON); coor_timer.setEnabled(viz.ON); write_onkey.setEnabled(viz.ON);
		quit_onkey.setEnabled(viz.ON); pos_move_timer.setEnabled(viz.ON); time_timer.setEnabled(viz.ON)
		
		#start the clocks again
		movement_time = TickTockTimer(); movement_time.StartTimer(); trial_time.UnPause()
		
		#increase the sub_trial number by 1
		sub_trial_number = sub_trial_number + 1
		
def setup_view():

	#turn off headlight
	headLight = viz.MainView.getHeadLight(); headLight.disable()

	#setup view point collision with a large buffer to account for large maze size
	viz.MainView.collision(viz.ON); viz.collisionbuffer(10)

	#Create a larger FOV to make the maze seem wider
	viz.fov(80, 1.1)

	#Set position, orientation, and eyeheight, and stepsize
	viz.MainView.setPosition(start_coords,viz.ABS_GLOBAL)
	viz.MainView.setEuler((0,0,0),viz.ABS_GLOBAL)
	viz.MainView.setEuler(start_ori,viz.BODY_ORI,viz.ABS_GLOBAL)
	viz.eyeheight(40)
	viz.stepsize(10)
	
def update_joystick():
	#Function for updating the joystick. Modified from the Vizard help documents.
	#get how much joystick moved. Then get absolute value
	x,y,z = joy.getPosition()
	sign_y = cmp(y,0)
	sign_x = cmp(x,0)
	
	#Move the viewpoint 
	if abs(x) > .75:
		#adjust turn speed here
		viz.MainView.setEuler([x*.55,0,0],viz.BODY_ORI,viz.REL_GLOBAL)
		#viz.MainView.setEuler([x*2.0,0,0],viz.BODY_ORI,viz.REL_GLOBAL)
	if abs(y) > 0.4:
		#adjust movement speed here
		viz.MainView.move(0,0,-sign_y*.90,viz.BODY_ORI)
		#viz.MainView.move(0,0,-sign_y*5,viz.BODY_ORI)

def update_coordinates():
	#Function to get the current coordinates/time and append them to the coordinate array
	global coordinate_array
	elapsed = movement_time.GetTime()
	position = viz.MainView.getPosition(viz.ABS_GLOBAL)
	coordinate_array = append(coordinate_array,position)
	coordinate_array = append(coordinate_array,elapsed)

def write_trial_data():	
	
	#Get time elapsed for the global clock
	elapsed_time = movement_time.GetTime()
	
	#declare total distance variable
	total_distance = 0.0
	
	#get the number of elements in the coordinate_array
	array_size = coordinate_array.size
	
	#divide by 4 to get number of rows in a x by 4 array
	new_axis = array_size // 4
	
	#reshape the array
	resized_coordinate_array = resize(coordinate_array,(new_axis,4))

	#Calculate average velocity and total distance by loopoing throughe very element of resized_coordinate_array
	for row in range(new_axis):
		#Check to insure loop doesn't go outside of array index
		#Note: range() goes from 0 to new_axis - 1. So if new_axis = 8 it would go from 0 to 7.
		#The resized array goes from 0 to new_axis - 1 as well. So the last value that will go through this if statment
		#is the end to the last value of the array.
		if row < new_axis - 1:
			#calculate distance between current point and the next point
			x = pow(resized_coordinate_array[row+1,0]-resized_coordinate_array[row,0],2)
			y = pow(resized_coordinate_array[row+1,1]-resized_coordinate_array[row,1],2)
			z = pow(resized_coordinate_array[row+1,2]-resized_coordinate_array[row,2],2)
			distance = sqrt(x+y+z)
			total_distance = total_distance + distance
	average_velocity = total_distance / elapsed_time
	
	#Open output file
	file = open('C:\Experiments\AMBI2016\SNAP\Programs_Environments\\' + str(subject_id_data) + '.txt' ,'a')
	
	#Write the Maze Name
	file.write('\n' + 'Maze: ' + str(maze_root))

	#Write condition,phase and trial if is not a practice or visomotor maze
	if maze_root != 'VMS' and maze_root != 'PMS':
		file.write('\n' + 'Condition: ' + str(condition))
		file.write('\n' + 'Phase: ' + phase)
		file.write('\n' + 'Trial Number: ' + str(trial_number))
		#if it is a condition 1 learning phase trial, output the subtrial
		if condition == 1 and phase == 'Learning':
			file.write('\n' + 'Sub_Trial Number: ' + str(sub_trial_number))
		#if it is condition 2 and a test phase trial, output the object
		if condition == 2 and phase == 'Testing':
			file.write('\n' + 'Object: ' + trial_object)
		
	#Write out the rest of the data
	file.write('\n' + 'Movement Time: ' + str(elapsed_time))
	file.write(str('\n' + 'Average Velocity: ' + str(average_velocity)))
	file.write(str('\n' + 'Total Distance: ' + str(total_distance)))
	file.write('\n' + 'Coordinates: ' + '\n' + str(resized_coordinate_array))	
	file.close()
	
def starter():
	yield get_subject_info()
	yield task_choice()

def check_pos():
	#Get current cordinates. Check to see if they match the "collide coordinates". If they do,
	#send a signal
	x,y,z = viz.MainView.getPosition(viz.ABS_GLOBAL)
	if ((x>=collide_coords[0] and x<=collide_coords[1]) and (z>=collide_coords[2] and z<=collide_coords[3])):
		signal.send()

def check_pos_and_move():
	#Get currentcoordinates. Check to see if they match the "collide coordinates". If they do, 
	#call learn_move
	x,y,z = viz.MainView.getPosition(viz.ABS_GLOBAL)
	if ((x>=collide_coords[0] and x<=collide_coords[1]) and (z>=collide_coords[2] and z<=collide_coords[3])):
		viztask.schedule(learn_move())
		
def check_time():
	#wait until the total time in the trial has finished before sending signal
	if trial_time.GetTime() >= 300.0:
	#if trial_time.GetTime() >= 50.0:
		time_signal.send()
		
#Code for timer used through the maze.
#From http://code.activestate.com/recipes/577646-pythontimer/
class TickTockTimer:

	def StartTimer(self):
		self.TimerOffset = time.time()
		self.LastTicked = 0
		self.TimeWhenItWasPaused = 0
		self.paused = False
	
	def Tick(self):
		if self.paused is False:
			NewTicked = time.time() - self.TimerOffset
			diff = NewTicked - self.LastTicked
			self.LastTicked = NewTicked
			return diff
		else:
			print "Cannot Tick, Timer is paused"

	def GetTime(self):
		if self.paused is True:
			return self.TimeWhenItWasPaused
		else:
			return time.time() - self.TimerOffset
		
	def Pause(self):
		self.TimeWhenItWasPaused = time.time() - self.TimerOffset
		self.paused = True

	def UnPause(self):
		self.TimerOffset = time.time() - self.TimeWhenItWasPaused
		self.paused = False




# define/turn off global events
joy_timer = vizact.ontimer(0,update_joystick); joy_timer.setEnabled(viz.OFF)
pos_timer = vizact.ontimer(0,check_pos); pos_timer.setEnabled(viz.OFF)
pos_move_timer = vizact.ontimer(0,check_pos_and_move); pos_move_timer.setEnabled(viz.OFF)
coor_timer = vizact.ontimer(.25,update_coordinates); coor_timer.setEnabled(viz.OFF)
write_onkey = vizact.onkeydown('q',write_trial_data); write_onkey.setEnabled(viz.OFF)
quit_onkey = vizact.onkeydown('q',viz.quit); quit_onkey.setEnabled(viz.OFF)
time_timer = vizact.ontimer(0,check_time); time_timer.setEnabled(viz.OFF)

#lauch the program
viztask.schedule(starter())
