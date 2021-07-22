#!/usr/bin/env bash

# Sets bridge s0 to use OpenFlow 1.3
ovs-vsctl set bridge s0 protocols=OpenFlow13 

# Sets bridge s1 to use OpenFlow 1.3
ovs-vsctl set bridge s1 protocols=OpenFlow13

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge s2 protocols=OpenFlow13 

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge s3 protocols=OpenFlow13 

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge s4 protocols=OpenFlow13 

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge s6 protocols=OpenFlow13 

# Print the protocols that each switch supports
for switch in s0 s1 s2 s3 s4 s6;
do
    protos=$(ovs-vsctl get bridge $switch protocols)
    echo "Switch $switch supports $protos"
done

# Avoid having to write "-O OpenFlow13" before all of your ovs-ofctl commands.
ofctl='ovs-ofctl -O OpenFlow13'

# --------------------------------------------------- h2 to h4
# link from h2 to s2 to s3
# send from s2 to s3
$ofctl add-flow s2 \
    in_port=1,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

# link from s3 to s4
# come from 2, send from s3 to s4 on 3
$ofctl add-flow s3 \
    in_port=2,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0E:01:00:03,mod_dl_dst:0A:00:0E:FE:00:02,output=3

# link from s4 to h4
# come from 2, send from s4 to h4 on 1
$ofctl add-flow s4 \
    in_port=2,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:04:01:00:01,mod_dl_dst:0A:00:04:02:00:00,output=1



# in_port = port message coming in from 
# nw_src = message incoming from host
# nw_dst = message destination host
# mod_dl_src = MAC addr coming from
# mod_dl_dst = MAC addr sending to
# output = on the switch, which out port to use



# link h4 to h2

# link h1 to h6

# link h6 to h1

# link h0 to h3

# link h3 to h0

for switch in s0 s1 s2 s3 s4 s6;
do
    echo "Flows installed in $switch:"
    $ofctl dump-flows $switch
    echo ""
done
