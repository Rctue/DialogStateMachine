import os

def ReadConfigKey(key, configfile='/config/ksera_config.prop'):
    rospath=os.getenv('ROS_PACKAGE_PATH')
    for thepath in rospath.split(':'):
            if os.path.exists(thepath+configfile):
                    #print 'Reading: ' + thepath+configfile
                    theFile=open(thepath+configfile)
                    theContent=theFile.readlines()
                    for theline in theContent:
                            if theline.strip().startswith(key):
                                    keyvalue=theline.strip().split('=')
                                    return keyvalue
                    break

def ReadConfigFile(configfile='/config/ksera_config.prop'):

    keydict={}
    rospath=os.getenv('ROS_PACKAGE_PATH')
    for thepath in rospath.split(':'):
            if os.path.exists(thepath+configfile):
                    #print 'Reading: ' + thepath+configfile
                    theFile=open(thepath+configfile)
                    theContent=theFile.readlines()
                    for theline in theContent:
                            if not theline.find('=')<0 and not theline.strip().startswith('#'):
                                    keyvalue=theline.strip().split('=')
                                    keydict[keyvalue[0]]=keyvalue[1]
            break
    return keydict

if __name__ == "__main__":

    mykey='IP_NAO'
    mykeyvalue = ReadConfigKey(mykey)
    #print 'The value of %s is: %s\n'%(mykeyvalue[0], mykeyvalue[1])

    mydict=ReadConfigFile()
    #for akey in mydict:
        #print 'The value of %s is: %s'% (akey,mydict[akey])
