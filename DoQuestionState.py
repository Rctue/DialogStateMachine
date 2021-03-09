import os
import time
#import nao
import nao_nocv as nao
##import rospy
##import smach

__author__ = 'rhcuijpers'
__debug_no_nao__=False

class DoQuestion():
    def __init__(self, feedback_level=10):
        self.outcomes = ['do_succeeded', 'do_failed']
        self.input_keys = ['type', 'text', 'gesture', 'eyeleds', 'dialog_replies'] #,'emotion']
        self.output_keys = ['type', 'reply']

        self._feedback_level = feedback_level
        self._naoqi_simulation = os.getenv('NAOQI_SIMULATION') is not None
        self.userdata={}
        for key in self.output_keys : self.userdata[key]=''

    def _log(self, log_level, log_string):
        if log_level <= self._feedback_level:
            print(log_string)

    def execute(self, inputdata):
        try:
            print ''
            self._log(1, '>>> Entering DoQuestion\n')
            sleep_time = 0.0
            for key in inputdata:
                if key in self.output_keys:
                    self.userdata[key]=inputdata[key] ## copy inputs from previous states to outputs of this state
            self.userdata['reply']=''

            # Colors
            FAIL = '\033[91m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            OKBLUE = '\033[94m'
            HEADER = '\033[95m'
            BOLD = '\033[1m'
            ENDC = '\033[0m'

            if 'text' in inputdata:
                text_to_display = BOLD + FAIL + str(inputdata['text']).upper() + ENDC
                self._log(1, '>>> Nao: ' + text_to_display + ' <<<')
                if not self._naoqi_simulation:
                    if __debug_no_nao__==False: nao.Say(inputdata['text'])
                time.sleep(0.1)
#marco                sleep_time = max(sleep_time, 1 + len(inputdata.text) / 14) #defines 80 signs as 1s
		sleep_time = max(sleep_time, 1 + len(inputdata['text']) / 20) #defines 80 signs as 1s
                pass
            if 'eyeleds' in inputdata:
                self._log(2, '>>> Nao-LEDS: ' + str(inputdata['eyeleds']))
                try:
                    if inputdata['eyeleds'] != '':
                        if __debug_no_nao__==False: nao.RunLED(inputdata['eyeleds'])
                        time.sleep(0.1)
                except Exception as e:
                    self._log(0, '>>> Could not do LED script: ' + str(e))
                    return 'do_failed', self.userdata
                pass
            if 'gesture' in inputdata:
                self._log(1, '>>> Nao-gesture: ' + str(inputdata['gesture']))
                try:
                    if inputdata['gesture'] != '':
                        if __debug_no_nao__==False: nao.RunMovement(inputdata['gesture'], True, False)
                        time.sleep(0.1)
                        sleep_time = max(sleep_time, 3)
                except Exception as e:
                    self._log(0, '>>> Could not do Movement script: ' + str(e))
                    return 'do_failed', self.userdata
                pass
            time.sleep(sleep_time)

        except Exception as e:
            self._log(0, '>>> DoQuestion failed with error ' + str(e))
            return 'do_failed', self.userdata

        return 'do_succeeded', self.userdata

