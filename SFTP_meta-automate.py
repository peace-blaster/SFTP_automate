# __________                          ___.   .__                   __
# \______   \ ____ _____    ____  ____\_ |__ |  | _____    _______/  |_  ___________
#  |     ___// __ \\__  \ _/ ___\/ __ \| __ \|  | \__  \  /  ___/\   __\/ __ \_  __ \
#  |    |   \  ___/ / __ \\  \__\  ___/| \_\ \  |__/ __ \_\___ \  |  | \  ___/|  | \/
#  |____|    \___  >____  /\___  >___  >___  /____(____  /____  > |__|  \___  >__|
#                \/     \/     \/    \/    \/          \/     \/            \/


###########################################################################
##                                                                       ##
##                          SFTP Automater                               ##
##                                                                       ##
###########################################################################
##                                                                       ##
##      creates 1-click scripts for sending/recieving files via SFTP     ##
##                                                                       ##
##       USAGE: python3 SFTP_meta-automate.py -p /path/to/directory      ##
##                                                                       ##
###########################################################################

# imports
import os # for executing unix commands
import argparse # for CLI flags
from shutil import which # used

# get CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Full path to path to make scripts")
parser.add_argument("-c", "--anacron", help="Attempt to automatically add scripts to Anacron")
parser.add_argument("-s", "--systemd", help="Attempt to automatically set up scripts as systemd timers")
args=parser.parse_args()
anacron=False
systemd=False
if not args.path:
    print("main path not provided! using current directory")
    # get current path:
    mainPath=os.path.abspath(os.getcwd())
else:
    mainPath=args.path
if args.anacron:
    anacron=True
if args.systemd:
    systemd=True

# see if commands exist on system:
def findCommand(cmd):
    # check output of unix 'which' using shutil:
    return which(cmd) is not None #returns Boolean

# make SFTP object:
class SFTP_obj:
    def __init__(self, useMode, name, user, password, host, port='22', scriptPath='.', remotePath='.', localPath='.'):
            tst=findCommand('lftp')
            if not tst:
                print('lftp is either not installed, or not in PATH. Contact your system administrator to address this.')
                raise RuntimeError('lftp unavailable')
                return 0 # should quit attempting to build object

        # fetch connection info, others
        self.useMode=useMode
        self.user=user
        self.password=password
        self.host=host
        self.port=port
        self.name=name
        self.script=''
        self.remotePath=remotePath #can't validate this sadly

        # validate localPath
        if os.path.exists(localPath):
            self.localPath=localPath
        else:
            print('Put path is invalid- cannot save data when script runs')
            raise FileNotFoundError('local path is invalid')
            return 0 # should quit attempting to build object
        # validate scriptPath
        if os.path.exists(scriptPath):
            self.scriptPath=scriptPath
        else:
            print('Write path for script is invalid- cannot create script')
            raise FileNotFoundError('Write path for script is invalid')
            return 0 #should quit attempting to build object

    # make script for LFTP pull
    def makeScript_LFTP_pull(self):
        # This will be very long- spacing it out like this for readability
        # It's likely the generated script will need to be editted later, so it needs to be easy to work with
        self.script="#!/bin/bash\n"
        self.script=self.script+"\n"
        self.script=self.script+"#######################################\n"
        self.script=self.script+"##                                   ##\n"
        self.script=self.script+"##  GENERATED SCRIPT FOR {}   ##\n".format(self.name.upper())
        self.script=self.script+"##                                   ##\n"
        self.script=self.script+"#######################################\n"
        self.script=self.script+"# Notes:\n"
        self.script=self.script+"# - Be careful with permissions on this file! Contains sensitive info\n"
        self.script=self.script+"# - Set up without CLI args for security\n"
        self.script=self.script+"# - Will be auto-generated from parent script\n"
        self.script=self.script+"\n"
        self.script=self.script+"# info:\n"
        self.script=self.script+"#URL of remote server:\n"
        self.script=self.script+"sftpServer={}\n".format(self.host)
        self.script=self.script+"#user for remote server:\n"
        self.script=self.script+"sftpUser={}\n".format(self.user)
        self.script=self.script+"#password for remote server:\n"
        self.script=self.script+"sftpPass={}\n".format(self.password)
        self.script=self.script+"#path to files on remote server:\n"
        self.script=self.script+"remotePath={}\n".format(self.remotePath)
        self.script=self.script+"#path to where you want files locally\n"
        self.script=self.script+"localPath={}\n".format(self.localPath)
        self.script=self.script+"\n"
        self.script=self.script+"# connect to server\n"
        self.script=self.script+"lftp -u $sftpUser,$sftpPass sftp://$sftpServer <<EOF\n"
        self.script=self.script+"mirror --parallel=10 $remotePath $localPath\n"
        self.script=self.script+"exit\n"
        self.script=self.script+"EOF\n"

    # make script for LFTP push
    def makeScript_LFTP_push(self):
        # This will be very long- spacing it out like this for readability
        # It's likely the generated script will need to be editted later, so it needs to be easy to work with
        self.script="#!/bin/bash\n"
        self.script=self.script+"\n"
        self.script=self.script+"#######################################\n"
        self.script=self.script+"##                                   ##\n"
        self.script=self.script+"##  GENERATED SCRIPT FOR {}   ##\n".format(self.name.upper())
        self.script=self.script+"##                                   ##\n"
        self.script=self.script+"#######################################\n"
        self.script=self.script+"# Notes:\n"
        self.script=self.script+"# - Be careful with permissions on this file! Contains sensitive info\n"
        self.script=self.script+"# - Set up without CLI args for security\n"
        self.script=self.script+"# - Will be auto-generated from parent script\n"
        self.script=self.script+"\n"
        self.script=self.script+"# info:\n"
        self.script=self.script+"#URL of remote server:\n"
        self.script=self.script+"sftpServer={}\n".format(self.host)
        self.script=self.script+"#user for remote server:\n"
        self.script=self.script+"sftpUser={}\n".format(self.user)
        self.script=self.script+"#password for remote server:\n"
        self.script=self.script+"sftpPass={}\n".format(self.password)
        self.script=self.script+"#path to files on remote server:\n"
        self.script=self.script+"remotePath={}\n".format(self.remotePath)
        self.script=self.script+"#path to where you want files locally\n"
        self.script=self.script+"localPath={}\n".format(self.localPath)
        self.script=self.script+"\n"
        self.script=self.script+"# connect to server\n"
        self.script=self.script+"lftp -u $sftpUser,$sftpPass sftp://$sftpServer << --EOF--\n"
        self.script=self.script+"mirror --parallel=10 --reverse $localPath $remotePath\n"
        self.script=self.script+"exit\n"
        self.script=self.script+"--EOF--\n"

    # make script:
    def makeScript(self):
        if self.useMode=='pull':
            self.makeScript_LFTP_pull()
            self.outputScript()
        if self.useMode=='push':
            self.makeScript_LFTP_push()
            self.outputScript()

    # output script to filesystem
    def outputScript(self):
        # create file:
        fileLink=open('{name}_{tool}_script.sh'.format(name=self.name, tool=self.tool),'w+')
        fileLink.write(self.script)
        fileLink.close()
        # make it executable, user-only for security:
        os.system('chmod 600 {name}_{tool}_script.sh'.format(name=self.name, tool=self.tool))
        os.system('chmod +x {name}_{tool}_script.sh'.format(name=self.name, tool=self.tool))

# main loop:
# object to track scripts created:
scripts=[]
# outer loop maintains menu, inner refreshes
while True:
    # itemLoop loops for a single script creation
    itemLoop=True
    # initialize variables:
    name=''
    user=''
    password=''
    host=''
    port='22'
    scriptPath='.'
    localPath='.'
    remotePath='.'
    useMode=''
    #
    prompt=input('Add another job? (y/n)')
    if prompt.lower()=='y':
        # get connection name:
        prompt=input('Connection name:\n')
        if prompt:
            name=prompt
        # get host URL:
        prompt=input("Host URL:\n")
        if prompt:
            host=prompt
        # get username:
        prompt=input("Username:\n")
        if prompt:
            user=prompt
        # get password:
        prompt=input("Password (make sure these the script is stored securely!):\n")
        if prompt:
            password=prompt
        # get port:
        prompt=input("Host port (usually 22):\n")
        if prompt:
            port=prompt
        # get localPath:
        prompt=input("Path to local files:\n")
        if prompt:
            localPath=prompt
        # get remotePath:
        prompt=input("Path on remote server:\n")
        if prompt:
            remotePath=prompt
        # get scriptPath:
        prompt=input("Path to put scripts:\n")
        if prompt:
            scriptPath=prompt
        # get mode:
        prompt=input("Push or pull?\n 1.) push\n 2.) pull\n 3.) quit\n")
        if prompt.lower() not in ['1','2','3','q']:
            print("invalid selection!")
        else:
            if prompt=='1':
                useMode='push'
            if prompt=='2':
                useMode='pull'
            if prompt=='3' or prompt.lower()=='q':
                continue
        print('/-------------------------------------')
        print('--------------------------------------')
        print('|| - name: '+name+'\n||')
        print('|| - user: '+user+'\n||')
        print('|| - password: '+password+'\n||')
        print('|| - host: '+host+'\n||')
        print('|| - port: '+port+'\n||')
        print('|| - script path: '+scriptPath+'\n||')
        print('|| - local path:# NOTE: '+localPath+'\n||')
        print('|| - remote path: '+remotePath+'\n||')
        print('|| - mode: '+useMode+'\n||')
        print('------------------------# NOTE: --------------')
        print('\\-------------------------------------')
        prompt=input('\n\n\nis this correct? (y/n)\n')
        if prompt.lower()=='y':
            obj=SFTP_obj(useMode, name, tool, user, password, host, port=port, scriptPath=scriptPath, remotePath=remotePath, localPath=localPath)
            obj.makeScript()
            print('Created script {name}_{tool}_script.sh'.format(name=name, tool=tool))
            scripts.append('Created script {name}_{tool}_script.sh'.format(name=name, tool=tool))
    else:
        if anacron:
            print('Attempting to set up anacron automatically...')
            #fill this in using scripts list
        elif systemd:
            print('Attempting to set up systemd automatically...')
            #fill this in using scripts list
        else:
            print('done! Cheers')
            quit()
