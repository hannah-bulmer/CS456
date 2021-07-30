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

# in_port = port message coming in from 
# nw_src = message incoming from host
# nw_dst = message destination host
# mod_dl_src = MAC addr coming from
# mod_dl_dst = MAC addr sending to
# output = on the switch, which out port to use

# --------------------------------------------------- h2 to h4

# for h2
$ofctl add-flow s2 \
    in_port=1,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

$ofctl add-flow s2 \
    in_port=4,ip,nw_src=10.0.4.2,nw_dst=10.0.2.2,actions=mod_dl_src:0A:00:02:01:00:01,mod_dl_dst:0A:00:02:02:00:00,output=1
    
# for h3
$ofctl add-flow s3 \
    in_port=2,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0E:01:00:03,mod_dl_dst:0A:00:0E:FE:00:02,output=3

$ofctl add-flow s3 \
    in_port=3,ip,nw_src=10.0.4.2,nw_dst=10.0.2.2,actions=mod_dl_src:0A:00:0D:FE:00:02,mod_dl_dst:0A:00:0C:FE:00:04,output=2


# for h4
$ofctl add-flow s4 \
    in_port=2,ip,nw_src=10.0.2.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:04:01:00:01,mod_dl_dst:0A:00:04:02:00:00,output=1

$ofctl add-flow s4 \
    in_port=1,ip,nw_src=10.0.4.2,nw_dst=10.0.2.2,actions=mod_dl_src:0A:00:0E:FE:00:02,mod_dl_dst:0A:00:0E:01:00:03,output=2




# --------------------------------------------------- h1 to h6
# s1 to s2, s1 to h1
$ofctl add-flow s1 \
    in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:0C:01:00:03,mod_dl_dst:0A:00:0D:01:00:03,output=3

$ofctl add-flow s1 \
    in_port=3,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1

# s2 to s3, s2 to s1
$ofctl add-flow s2 \
    in_port=3,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

$ofctl add-flow s2 \
    in_port=4,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0D:01:00:03,mod_dl_dst:0A:00:0C:01:00:03,output=3

# s3 to s6, s3 to s2
$ofctl add-flow s3 \
    in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:0F:01:00:04,mod_dl_dst:0A:00:0F:FE:00:02,output=4

$ofctl add-flow s3 \
    in_port=4,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0D:FE:00:02,mod_dl_dst:0A:00:0C:FE:00:04,output=2

# s6 to h6, s6 to s3
$ofctl add-flow s6 \
    in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.6.2,actions=mod_dl_src:0A:00:06:01:00:01,mod_dl_dst:0A:00:06:02:00:00,output=1

$ofctl add-flow s6 \
    in_port=1,ip,nw_src=10.0.6.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0F:FE:00:02,mod_dl_dst:0A:00:0F:01:00:04,output=2




# --------------------------------------------------- h0 to h3

# s0 to s2, s0 to h0
$ofctl add-flow s0 \
    in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.3.2,actions=mod_dl_src:0A:00:0B:01:00:03,mod_dl_dst:0A:00:0B:FE:00:02,output=3

$ofctl add-flow s0 \
    in_port=3,ip,nw_src=10.0.3.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1


# s2 to s3, s2 to s0
$ofctl add-flow s2 \
    in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.3.2,actions=mod_dl_src:0A:00:0C:FE:00:04,mod_dl_dst:0A:00:0D:FE:00:02,output=4

$ofctl add-flow s2 \
    in_port=4,ip,nw_src=10.0.3.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0B:FE:00:02,mod_dl_dst:0A:00:0B:01:00:03,output=2


# s3 to h3, s3 to s2
$ofctl add-flow s3 \
    in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.3.2,actions=mod_dl_src:0A:00:03:01:00:01,mod_dl_dst:0A:00:03:02:00:00,output=1

$ofctl add-flow s3 \
    in_port=1,ip,nw_src=10.0.3.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0D:FE:00:02,mod_dl_dst:0A:00:0C:FE:00:04,output=2



# ----------- end

for switch in s0 s1 s2 s3 s4 s6;
do
    echo "Flows installed in $switch:"
    $ofctl dump-flows $switch
    echo ""
done
