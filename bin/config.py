#!/usr/bin/env python3

# This is a variable configuration file

basedir="/home/gerson/recoger"
bindir=basedir+"/bin"
queuedir=basedir+"/queue"
logdir=basedir+"/logs"
donedir=basedir+"/done"

# This configuration are used to contro the master flow of product

# This is max distance to acknoledge somebody is close to the sensor
# trig_dist_max=1000
trig_dist_max=500

# This is how many sensor readers until it is close enough
maxtrig=10

# This config is to stop gracefuly the service
stopme=bindir+"/stopme"
