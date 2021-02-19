#!/bin/bash

#######################################
##                                   ##
##  GENERATED SCRIPT FOR TST   ##
##                                   ##
#######################################
# Notes:
# - Be careful with permissions on this file! Contains sensitive info
# - Set up without CLI args for security
# - Will be auto-generated from parent script

# info:
#URL of remote server:
sftpServer=127.0.0.1
#user for remote server:
sftpUser=peaceblaster
#password for remote server:
sftpPass=Password
#path to files on remote server:
remotePath=/home/peaceblaster/TST2
#path to where you want files locally
localPath=/home/peaceblaster/TST1

# connect to server
lftp -u $sftpUser,$sftpPass sftp://$sftpServer << --EOF--
mirror --parallel=10 --reverse $localPath $remotePath
exit
--EOF--
