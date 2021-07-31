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
$ofctl add-flow s0 \
    in_port=1,actions=output:2


# r1 to s1
$ofctl add-flow r1 \
    in_port='r1-eth1',ip,nw_src=10.1.1.17,nw_dst=10.6.6.69,actions=mod_dl_src:0A:00:0E:FE:00:02,mod_dl_dst:0A:00:01:01:00:01,output='r1-eth2'


# connect s1 to r2
$ofctl add-flow s1 \
    in_port=1,actions=output:3


# r2 to s2
$ofctl add-flow r2 \
    in_port='r2-eth1',ip,nw_src=10.1.1.17,nw_dst=10.6.6.69,actions=mod_dl_src:0A:00:10:FE:00:02,mod_dl_dst:0A:00:02:01:00:01,output='r1-eth2'


# connect s2 to carol
$ofctl add-flow s2 \
    in_port=1,actions=output:2

#  ------------------- Carol talks to Alice -----------------------

# connect s2 to r2
$ofctl add-flow s2 \
    in_port=2,actions=output:1


# r2 to s1
$ofctl add-flow r2 \
    in_port='r2-eth2',ip,nw_src=10.6.6.69,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:05:01:00:01,mod_dl_dst:0A:00:0C:01:00:03,output='r2-eth1'


# connect s1 to r1
$ofctl add-flow s1 \
    in_port=3,actions=output:1


# r1 to s0
$ofctl add-flow r1 \
    in_port='r1-eth2',ip,nw_src=10.6.6.69,nw_dst=10.1.1.17,actions=mod_dl_src:0A:00:04:01:00:01,mod_dl_dst:0A:00:0A:01:00:02,output='r1-eth1'


# connect s0 to alice
$ofctl add-flow s0 \
    in_port=2,actions=output:1


for switch in s0 s1 s2 r1 r2;
do
    echo "Flows installed in $switch:"
    $ofctl dump-flows $switch
    echo ""
done
