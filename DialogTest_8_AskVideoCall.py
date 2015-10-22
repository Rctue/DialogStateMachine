#!/usr/bin/env python
from sre_parse import isdigit
import sys

__author__ = 'jpijper'


import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach_ros

from DialogStateMachine_ismb import SMDialog

def main():
    # To restrict the amount of feedback to the screen, a feedback level can be given on the command line.
    # Level 0 means show only the most urgent feedback and the higher the level, the more is shown.
    feedback_level = int(sys.argv[1]) if len(sys.argv) > 1 and isdigit(sys.argv[1]) else 10

    rospy.init_node('sm_dialog_ask_video_call')
    sm_top = SMDialog("ask_video_call.csv", "192.168.0.5", use_getch=False).sm_top

    ## inserted for smach_viewer
    # Create and start the introspection server
    #sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_ROOT')
    #sis.start()
    ## end insert
    
    # Execute SMACH plan
    outcome = sm_top.execute()

    ## inserted for smach_viewer
    # Wait for ctrl-c to stop the application
    #rospy.spin()
    #sis.stop()
    ## end insert

if __name__ == '__main__':
    main()
