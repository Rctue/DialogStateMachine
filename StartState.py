import random
#import nao
import nao_nocv as nao
##import roslib; roslib.load_manifest('dialog_state_machine')
##import rospy
##import smach
##import smach_ros

import os

__author__ = 'rhcuijpers'

class Start():

    def __init__(self, dialog_filename, nao_ip, nao_port, feedback_level=10):

        print '*** StartState: Entering constructor ***'

##        smach.State.__init__(self,
        self.outcomes = ['start_question', 'start_message', 'start_yes', 'start_no', 'start_aborted']
        self.input_keys = ['type', 'reply']
        self.output_keys = ['type', 'text', 'gesture', 'eyeleds', 'dialog_replies']
        self.userdata={}
        for key in self.output_keys : self.userdata[key]=''
        
        self._feedback_level = feedback_level
        self._trial_count = 0
        self._message_logic = {}
        self._filename = dialog_filename
        csv_file = nao.LoadDialog(self._filename)
        self._dialog, self._dialog_logic, self._message_logic, self._current_dialog_key = self._init_dialog(csv_file)

        # Check environment variable to see if this is a naoqi simulation.
        self._naoqi_simulation = os.getenv('NAOQI_SIMULATION') is not None

        # Dialogs that just report something have an empty dialog_logic.
        self._dialog_replies = []
        if self._current_dialog_key in self._dialog_logic:
            self._dialog_replies = self._dialog_logic.get(self._current_dialog_key).keys()

        # Initialize proxies. If a naoqi simulation is used, use only a subset of all proxies
        motion_proxy = 3
        memory_proxy = 4
        led_proxy = 7
        all_proxies = 0
        print ''
        proxy_list = [motion_proxy, memory_proxy, led_proxy] if self._naoqi_simulation else [all_proxies]
        nao.InitProxy(nao_ip, proxy_list, nao_port)
        print ''

    def _log(self, log_level, log_string):
        if log_level <= self._feedback_level:
            print(log_string)

    def _init_dialog(self, csv_reader):
        addKeys = False
        addLogic = False
        addMessageLogic = False
        firstLine = False
        logic = {}
        dlg = {}
        dlg_first = ''
        messageLogic = {}
        print ''
        for row in csv_reader:
            if row[0] == '':
                continue
            if row[0] == "dialog_keys":
                firstLine = True
                addKeys = True
                addLogic = False
                addMessageLogic = False
                continue
            if row[0] == "dialog_logic":
                addLogic = True
                addKeys = False
                addMessageLogic = False
                continue
            if row[0] == "message_logic":
                addLogic = False
                addKeys = False
                addMessageLogic = True
                continue
            if addKeys:
                temp = row[4:]
                while temp.count(''):
                    temp.remove('')
                dlg[row[0]] = [row[1], row[2], row[3], temp]
                self._log(3, "Parsing keys: " + ', '.join(row))
                if firstLine:
                    dlg_first = row[0]
                    firstLine = False
                continue
            if addLogic:
                while row.count(''):
                    row.remove('')
                logic[row[0]] = dict(zip(row[1::2], row[2::2]))
                self._log(3, "Parsing logic: " + ', '.join(row))
                continue
            if addMessageLogic:
                while row.count(''):
                    row.remove('')
                messageLogic[row[0]] = row[1:]
                self._log(3, "Parsing message logic: " + ', '.join(row))
                continue
        print ''
        return dlg, logic, messageLogic, dlg_first

    def execute(self, inputdata={'type':'','reply':''}):
        try:
            print ''
            self._log(1, '>>> Entering Start (' + self._filename + ')')
            for key in inputdata:
                if key in self.userdata:
                    self.userdata[key]=inputdata[key]
                    
            self._log(2, "inputdata.type = '" + inputdata['type'] + "', " + "inputdata.reply = '" + inputdata['reply'] + "'")
            self._log(3, 'self.current_dialog_key = ' + self._current_dialog_key)
            self._log(3, 'dialog keys = ' + str(self._dialog.keys()))
            self._log(3, 'dialog_logic keys = ' + str(self._dialog_logic.keys()))
            self._log(3, 'message_logic keys = ' + str(self._message_logic.keys()))
            self._log(3, 'self.trial_count = ' + str(self._trial_count))

            next_dialog_key = 'none'
##            if self._dialog_logic.get(self._current_dialog_key) is not None:
##                next_dialog_key = self._dialog_logic.get(self._current_dialog_key).get(inputdata['reply'])

            # Type is empty -> First entry
            if inputdata['type'] == '':
                # first time entry so proceed with self.dialog_current
                next_dialog_key = self._current_dialog_key
                pass

            # Type is message
            elif inputdata['type'] == 'message':

                if self._current_dialog_key in self._message_logic:
                    next_dialog_key = random.choice(self._message_logic.get(self._current_dialog_key))
                else:
                    # do default mapping ...
                    # ... for messages
                    self._log(3,'warning: no explicit end state for message, defaulting to "yes".')
                    return 'start_yes', self.userdata
                    
            # Type is question
            elif inputdata['type'] == 'question':
                if self._current_dialog_key in self._dialog_logic:
                    if inputdata['reply'] == 'did not understand':
                        # the special case 'did not understand' repeated 3 times before it is mapped according to the dialog_logic
                        if self._trial_count > 2:
                            self._trial_count = 0
                            if inputdata['reply'] in self._dialog_logic.get(self._current_dialog_key):
                                next_dialog_key=self._dialog_logic.get(self._current_dialog_key).get(inputdata['reply'])
                            else:
                                # if reply is not found, do the default mapping
                                return 'start_no', self.userdata
                        else:
                            # repeat question
                            self._trial_count +=1
                            next_dialog_key = self._current_dialog_key
                    elif inputdata['reply'] in self._dialog_logic.get(self._current_dialog_key):
                        # the normal case 
                        next_dialog_key=self._dialog_logic.get(self._current_dialog_key).get(inputdata['reply'])
                    else:
                        # repeat question if unexpected answer is given
                        next_dialog_key = self._current_dialog_key
                        pass

                else:
                    # do default mapping ...
                    # ... for questions
        
#                    # Reply is empty
#                    if inputdata['reply'] == '':
#                        pass

                    # Reply is yes
                    if inputdata['reply'] == 'yes':
                        return 'start_yes', self.userdata

                    # Reply = no
                    elif inputdata['reply'] == 'no':
                        return 'start_no', self.userdata

                    # Reply is Did not understand
                    elif inputdata['reply'] == 'did not understand':
                        if self._trial_count > 2:
                            self._trial_count = 0
                            return 'start_no', self.userdata
                        else:
                            self._trial_count += 1

                    # Reply is Repeat
                    elif inputdata['reply'] == 'repeat':
                        pass

                    # Unexpected reply
                    else:
                        inputdata['reply'] = 'did not understand'
                        if self._trial_count > 2:
                            self._trial_count = 0
                            return 'start_no', self.userdata
                        else:
                            self._trial_count += 1
                        pass
                    #repeat question
                    next_dialog_key = self._current_dialog_key

            # Unrecognized type
            else:
                next_dialog_key = self._current_dialog_key
                pass

            self._log(3, 'next_dialog_key: ' + str(next_dialog_key))

            # In the message_logic, the next dialog key may have been set to one of the special
            # values endYes or endNo. In this case, the dialog ends with the appropriate return value.
            if next_dialog_key == 'endYes':
                return 'start_yes', self.userdata
            elif next_dialog_key == 'endNo':
                return 'start_no', self.userdata
            else:
                # prepare next Query
                self._current_dialog_key = next_dialog_key
                next_query = self._dialog.get(self._current_dialog_key)
                ## print next_query
                # otherwise perform next_query
                self.userdata['type'] = next_query[0]
                self.userdata['gesture'] = next_query[1]
                self.userdata['eyeleds'] = next_query[2]
                self.userdata['text'] = random.choice(next_query[3])
                #ud.emotion=next_query[4]

                if next_query[0] == 'question':
                    self._dialog_replies = self._dialog_logic.get(self._current_dialog_key).keys()
                    self.userdata['dialog_replies'] = self._dialog_replies
                    return 'start_question', self.userdata

                elif next_query[0] == 'message':
                    self.userdata['dialog_replies'] = ''
                    return 'start_message', self.userdata

        except Exception as e:
            self._log(0, '>>> Start failed with error ' + str(e))
            return 'start_aborted', self.userdata



