# Part A

## Describing the add-flow commands

I will go through each command in order and describe what it is doing:


1. 
```
$ofctl add-flow s0 \
    in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0A:FE:00:02,output=2 

```
This add flow command tells the switch `s0` that packets with network src `10.0.0.2` and dst `10.0.1.2` (coming from host 0 and going to host 1) that have come in through ingress port 1 should be sent out on ingress port 2 that has MAC `0A:00:0A:01:00:02` to destination MAC `0A:00:0A:FE:00:02` (which is in s1)

2. 
```
$ofctl add-flow s0 \
    in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1 
```
This add flow command tells the switch `s0` that packets with network src `10.0.1.2` and dst `10.0.0.2` (coming from host 1 and going to host 0) that have come in through ingress port 2 should be sent out on ingress port 1 that has MAC `0A:00:00:01:00:01` to destination MAC `0A:00:00:02:00:00` (which is h0).

3.
```
$ofctl add-flow s1 \
    in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1 

```
This add flow command tells the switch `s1` that packets with network src `10.0.0.2` and dst `10.0.1.2` (coming from host 0 and going to host 1) that have come in through ingress port 2 should be sent out on ingress port 1 that has MAC `0A:00:01:01:00:01` to destination MAC `0A:00:01:02:00:00` (which is host 1).

4.
```
$ofctl add-flow s1 \
    in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0A:FE:00:02,mod_dl_dst:0A:00:0A:01:00:02,output=2 

```
This add flow command tells the switch `s1` that packets with network src `10.0.1.2` and dst `10.0.0.2` (coming from host 1 and going to host 0) that have come in through ingress port 1 should be sent out on ingress port 2 that has MAC `0A:00:0A:FE:00:02` to destination MAC `0A:00:0A:01:00:02` (which is s0).