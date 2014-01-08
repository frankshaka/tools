#!/bin/bash
#####################################
# vm.sh
# ------
# A convenient script that manages virtual machines based on VirtualBox.
#
# To install this script:
#
#     $ sudo cp vm.sh /usr/local/bin/vm && sudo chmod +x /usr/local/bin/vm
#
# Usage:
#
#     $ vm start VirtualMachineName
#
######################################

CMD=$1
VM_NAME=$2

if [ "start" = "$1" ]; then
    VBoxManage startvm "$2" -type headless
elif [ "stop" = "$1" ]; then
    VBoxManage controlvm "$2" savestate
elif [ "shutdown" = "$1" ]; then
    VBoxManage controlvm "$2" poweroff
elif [ "list" = "$1" ]; then
    echo "==============  VMs =============="
    VBoxManage list vms
    echo "==============  Running VMs  =============="
    VBoxManage list runningvms
elif [ "state" = "$1" ]; then
    VBoxManage showvminfo "$2" | grep "^State"
elif [ "info" = "$1" ]; then
    VBoxManage showvminfo "$2"
else
    echo "Unrecognized command: $1"
    echo "Available commands: list, start, stop, shutdown, state, info"
fi
