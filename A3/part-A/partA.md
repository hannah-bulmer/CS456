# Part A

## Describing the add-flow commands

I will go through the first command and describe what each field means in detail

1. 
```
$ofctl add-flow s0 \
    in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0A:FE:00:02,output=2 
```

We are looking at frames coming through the `s0` switch that carry the following characteristics

- `in_port=1` - matches to all frames coming in on port 1

- `ip` - matches this protocol

- `nw_src=10.0.0.2` - has the src IP addr of `10.0.0.2`

- `nw_dst=10.0.1.2` - has the dst IP addr of `10.0.1.2`

If a packet matches all of these things, then we apply the following actions:

1. `mod_dl_src:0A:00:0A:01:00:02` - modify the src MAC of the packet to `0A:00:0A:01:00:02`, which is the MAC addr of port 2 of the router

2. `mod_dl_dst:0A:00:0A:FE:00:02` - modify the dst MAC of the packet to `0A:00:0A:FE:00:02`, which is a MAC addr of a port in s1, so the packet will look to go there next

3. `output=2` - send the packet out of s0 on port 2


**Summary**:


This add flow command tells the switch `s0` that packets with network src `10.0.0.2` and dst `10.0.1.2` (coming from host 0 and going to host 1) that have come in through ingress port 1 should be sent out on ingress port 2, and change the src MAC to `0A:00:0A:01:00:02` (like it just came out of router s0) and the destination MAC `0A:00:0A:FE:00:02` (which is in s1, so it will go there next).
