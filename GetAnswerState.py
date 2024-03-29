import os
from getch import getch_noblock
##import rospy
#import smach
#from smach_tutorials.srv import *

__author__ = 'rhcuijpers'

class GetAnswer():
    """
    The GetAnswer class represents a SMACH state.
    """

    def _log(self, log_level, log_string):
        if log_level <= self._feedback_level:
            print(log_string)

    def __init__(self, feedback_level=10, use_getch=True,NAOQI_SIMULATION = False):
        """
        Constructor.
        """

#        smach.State.__init__(self,
        self.outcomes=['get_succeeded', 'get_failed']
        self.input_keys=['dialog_replies', 'type']
        self.output_keys=['reply', 'type']
        self.userdata={}
        for key in self.output_keys : self.userdata[key]=''
        

        # Set desired feedback level.
        self._feedback_level = feedback_level  # Everything with log level 0 or higher is printed.
#        self._naoqi_simulation = os.getenv('NAOQI_SIMULATION') is not None
        self._naoqi_simulation = NAOQI_SIMULATION

        # If speech recognition fails, the desired recognition result can be given through
        # the keyboard. In interactive sessions, this is done using getch_noblock() which results in unbuffered
        # character input without the need to use the Enter key. But e.g. in debug sessions this may not work
        # and raw_input() is used instead.
        self._use_getch = use_getch

        # Get the speech recognition engine going.

        # Speech recognition removed from trials

        #self._log(3, 'Waiting for service /ASRsphinx to start.')
        #rospy.wait_for_service('ASR_Srv_result')
        #self._log(3, 'Service /ASRsphinx has started.')
        #try:
        #    self._recBuffer = rospy.ServiceProxy('ASR_Srv_result', srv_ASRBuffer)
        #except rospy.ServiceException as e:
        #    self._log(0, 'Service call failed: ' + str(e))

    def execute(self, inputdata):
        """
        This method is called when a state machine transfers control to this state.
        @param userdata: The input and output data of the state, as enumerated in input_keys and output_keys.
        @return: One of the two possible state outcomes: 'get_succeeded' or 'get_failed'
        """

        try:
            print ''
            self._log(1, '>>> Entering GetAnswer')
            for key in inputdata:
                if key in self.userdata:
                    self.userdata[key]=inputdata[key]
            
            self.userdata['reply'] = 'repeat'
            #print "The current Query type is: ", ud.type #ud.type='question'

            # Speech recognition removed from trials. In 

            #if not self._naoqi_simulation:
            #    # Speech recognition is started here and the system appears to do nothing for a while.
            #    self._log(1, '>>> Performing speech recognition: speak or wait .....\n')
            #    rcRes = self._recBuffer(4)
            #    recognition_result = rcRes.msg
            #else:
            #    self._log(1, '>>> Skipping speech recognition')
            #    recognition_result = 'did not understand'

            #rcRes = self._recBuffer(4)
            #recognition_result = rcRes.msg
	    
            # The following line was present in the original version of this program. This function was 
            # already hard coding the result of the speech  recognition 
            recognition_result = 'did not understand'
            self._log(0, '>>> I understood: ' + str(recognition_result))

            # Use the recognition result to set self.userdata['reply'].
            c = 'd'
            if recognition_result == 'ja bitte' or recognition_result == 'ja':
                self.userdata['reply'] = 'yes'
                c = 'y'
            elif recognition_result == 'nein danke' or recognition_result == 'nein':
                self.userdata['reply'] = 'no'
                c = 'n'
            elif recognition_result == 'did not understand':
                self.userdata['reply'] = 'did not understand'
                c = 'd'
            elif recognition_result == 'nao stop':
                self.userdata['reply'] = 'abort'
                c = 'a'
                return 'get_failed', self.userdata

            # Here, the experimenter gets the opportunity to use the keyboard to give an answer.
            # In interactive mode, 5 seconds are allowed to do this. If nothing is entered by then,
            # the speech recognition result stands.
            self._log(1, 'Interactive: you have 5 seconds to enter something .....') if self._use_getch else self._log(0, 'Not interactive')
            self._log(1, '>>> You can press (y)es, (n)o, (r)epeat or (a)bort.')
            print chr(7)  # Beep

            pause_duration = 5.0 # seconds

            # If speech recognition fails, the desired recognition result can be given through the keyboard.
            # In interactive sessions (the default), this is done using getch_noblock() which results in unbuffered
            # character input without the need to use the Enter key. But e.g. in debug sessions this may not work
            # and raw_input() is used instead.
            if self._use_getch:
                c = getch_noblock(c, pause_duration, ['y', 'n', 'r', 'a']) # getch() blocks, so the whole timer stuff has no effect.
            else:
                c = raw_input('You must use the Enter key: ')

            # Use the received character input to set (userdata.)reply.
            if c == 'y': reply = 'yes'
            elif c == 'n': reply = 'no'
            elif c == 'r': reply = 'repeat'
            elif c == 'a': reply = 'abort'
            else: reply = 'did not understand' # This includes empty string and d

            # Give feedback.
            self._log(2, 'You pressed: ' + reply)

            if reply == 'abort':
                return 'get_failed', self.userdata
            else:
                self.userdata['reply'] = reply

        except Exception as e:
            self._log(0, '>>> GetAnswer failed with error ' + str(e))
            return 'get_failed', self.userdata

        return 'get_succeeded', self.userdata

