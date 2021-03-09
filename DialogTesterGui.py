#!/usr/bin/env python
from sre_parse import isdigit
import sys
import os
from Tkinter import *

#import roslib; roslib.load_manifest('smach_tutorials')
#import rospy
#import smach_ros
from DialogStateMachine import SMDialog

global var1
global NAOQI_SIMULATION
NAOQI_SIMULATION = False


def start_dialog(feedback_level=10):

    # Get the selected filename.
    global var1
    filename = var1.get()

    sm_dialog = SMDialog(filename, '192.168.0.112', feedback_level=feedback_level, use_getch=False) #'192.168.0.115'
    outcome = sm_dialog.Run()
    print '\n\n**************** END OF DIALOG **********************\n'

#if __name__ == '__main__':

# To restrict the amount of feedback to the screen, a feedback level can be given on the command line.
# Level 0 means show only the most urgent feedback and the higher the level, the more is shown.
feedback_level = int(sys.argv[1]) if len(sys.argv) > 1 and isdigit(sys.argv[1]) else 10

dialog_configuration_file_path = '/dialogs/'
rospath=os.getcwd() #getenv('ROS_PACKAGE_PATH')
for thepath in rospath.split(':'):
    if os.path.exists(thepath+dialog_configuration_file_path):
        dialog_configuration_files = [f for f in os.listdir(thepath+dialog_configuration_file_path) if f.endswith('.csv')]
        break

root = Tk()
root.title('Dialog tests')
root.geometry('200x85-50+200')
frame = Frame(root)
frame.pack()

var1 = StringVar()
var1.set(dialog_configuration_files[0])
menu = apply(OptionMenu, (frame, var1) + tuple(dialog_configuration_files))
menu.grid(pady = 5)

button_dialog_1 = Button(frame, text='Start dialog', command=start_dialog)
button_dialog_1.grid(pady = 5)

# Start a ROS node with a meaningful name.
#ros_node_name = 'Dialog_testing_node'
#rospy.init_node(ros_node_name)

root.mainloop()



#    dialog_test_1_ask_measurement(feedback_level)

#    rospy.init_node('sm_dialog_ask_measurement')
#    sm_dialog = SMDialog(
#        'ask_measurement.csv',
#        'localhost',
#        feedback_level=feedback_level)

    ## inserted for smach_viewer
    # Create and start the introspection server
    #sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_ROOT')
    #sis.start()
    ## end insert
    
    # Execute SMACH plan
#    outcome = sm_dialog.sm_top.execute()

    ## inserted for smach_viewer
    # Wait for ctrl-c to stop the application
    #rospy.spin()
    #sis.stop()
    ## end insert


