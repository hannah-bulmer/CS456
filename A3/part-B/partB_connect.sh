#!/usr/bin/env bash

# Sets bridge s0 to use OpenFlow 1.3
ovs-vsctl set bridge s0 protocols=OpenFlow13 

# Sets bridge s1 to use OpenFlow 1.3
ovs-vsctl set bridge s1 protocols=OpenFlow13

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge s2 protocols=OpenFlow13 

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge r1 protocols=OpenFlow13 

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge r2 protocols=OpenFlow13 

# Print the protocols that each switch supports
for switch in s0 s1 s2 r1 r2;
do
    protos=$(ovs-vsctl get bridge $switch protocols)
    echo "Switch $switch supports $protos"
done

# Avoid having to write "-O OpenFlow13" before all of your ovs-ofctl commands.
ofctl='ovs-ofctl -O OpenFlow13'

#  ------------------- Alice talks to Carol -----------------------
# connect s0 to r1

# r1 to r1

# connect r1 to s1

# connect s1 to r2

# r2 to r2

# connect r2 to s2

# connect s2 to carol

#  ------------------- Carol talks to Alice -----------------------

# connect s2 to r2

# r2 to r2

# connect r2 to s1

# connect s1 to r1

# r1 to r1

# connect r1 to s0

# connect s0 to alice