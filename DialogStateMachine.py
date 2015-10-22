#!/usr/bin/env python

__author__ = 'rhcuijpers'

#import roslib

#roslib.load_manifest('dialog_state_machine')
#import rospy
#import smach

from StartState import Start
from DoQuestionState import DoQuestion
from GetAnswerState import GetAnswer

class SMDialog():
    """
    Description:
    The class SMDialog implements a SMACH state machine for ROS that lets a Nao robot have dialogs with a person.
    The speech can be accompanied with gestures and eye LED patterns. At initialization it requires a file
    containing the dialog from david/lib/dialogs/ and the ip address of the robot.

    Usage:
    From the command line (assuming the hardcoded ip address "nao.local":
        $> ./DialogStateMachine.py
    or
        $> rosrun smach_tutorials sm_dialog_class.py
    As a module:
        from sm_dialog_class import SMDialog
        mysm=SMDialog(mydialogfile, mynaoip, mynaoport).sm_top
        mysm.execute()
    Output:
    The outputs are the output keys of the top-level state machine sm_top. They are:
    top_yes, top_no, top_abort
    """

    def __init__(self, dialog_filename, ip_address='localhost', port=9559, feedback_level=10, use_getch=True):

        """
        SMDialog class constructor
        """

        print '*** SMDialog: Entering constructor *** ' + dialog_filename
##
##        # Create a SMACH state machine
##        #        self._state_machine = smach.StateMachine(
        self.outcomes=['top_yes',
                      'top_no',
                      'top_aborted']
        self.userdata= {'reply':'','type':''}
        self.output_keys=self.userdata.keys()
        

##        # Open the container
##        with self._state_machine:
##            # Add states to the container
##            smach.StateMachine.add(
##                'START', Start(dialog_filename, ip_address, port, feedback_level),
##                transitions={'start_question': 'DO_QUESTION',
##                             'start_message': 'MESSAGE',
##                             'start_yes': 'top_yes',
##                             'start_no': 'top_no',
##                             'start_aborted': 'top_aborted'})
##
##            smach.StateMachine.add('DO_QUESTION', DoQuestion(feedback_level),
##                transitions={'do_succeeded': 'GET_ANSWER',
##                             'do_failed': 'top_aborted'})
##
##            smach.StateMachine.add('GET_ANSWER', GetAnswer(feedback_level, use_getch),
##                transitions={'get_succeeded': 'START',
##                             'get_failed': 'top_aborted'})
##
##            smach.StateMachine.add('MESSAGE', DoQuestion(feedback_level),
##                transitions={'do_succeeded': 'START',
##                             'do_failed': 'top_aborted'})
        self.start_node=Start(dialog_filename, ip_address, port, feedback_level)
        self.doquestion_node=DoQuestion(feedback_level)
        self.getanswer_node =GetAnswer(feedback_level, use_getch)

    def Run(self):
##        self._state_machine.execute()
        done=False
        while not done:
            result, self.userdata=self.start_node.execute(self.userdata)
            if result=='start_question':
                result, self.userdata=self.doquestion_node.execute(self.userdata)
            	if result=='do_succeeded':
                    result, self.userdata=self.getanswer_node.execute(self.userdata)
                    if result=='get_succeeded':
                        pass
                    elif result=='get_failed':
                        return 'top_aborted'
                elif result=='do_failed':
                    return 'top_aborted'
            elif result=='start_message':
                result, self.userdata=self.doquestion_node.execute(self.userdata)
                if result=='do_succeeded':
                    pass
                elif result=='do_failed':
                    return 'top_aborted'
            elif result=='start_yes':
                return 'top_yes'
            elif result=='start_no':
                return 'top_no'
            elif result=='start_aborted':
                return 'top_aborted'
        
        

    @property
    def sm_top(self):
        return self.start_node
