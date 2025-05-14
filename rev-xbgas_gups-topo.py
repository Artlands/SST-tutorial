import os
import sst
import sys
import math
import argparse
from utils import *
from sst import merlin

parser = argparse.ArgumentParser(description="xBGAS GUPS simulation script")
parser.add_argument('--config', '-c', default='simulation.cfg', help='Configuration file')

args = parser.parse_args()
cfgFile = args.config

# Build configuration information
config = Config(cfgFile)

class EndpointCreator(merlin.EndPoint):
    def __init__(self, config):
        merlin.EndPoint.__init__(self)
        self.config = config
    
    def getName(self):
        return "Network Network Endpoint"

    def build( self, nID, extraKeys):
        xbgas_cpu = sst.Component(f"cpu{nID}", "revcpu.RevCPU")
        xbgas_cpu.addParams(self.config.getCpuConfig())

        # Setup the memory controllers
        lsq = xbgas_cpu.setSubComponent("memory", "revcpu.RevBasicMemCtrl")

        # Create the memHierarchy subcomponent
        miface = lsq.setSubComponent("memIface", "memHierarchy.standardInterface")

        # Create the L1 cache
        l1cache = sst.Component("l1cache" + str(nID), "memHierarchy.Cache")
        l1cache.addParams(self.config.getL1CacheConfig())

        # Create the L2 cache
        l2cache = sst.Component("l2cache" + str(nID), "memHierarchy.Cache")
        l2cache.addParams(self.config.getL2CacheConfig())
        
        # Create the memory controller in memHierarchy
        memctrl = sst.Component("memory" + str(nID), "memHierarchy.MemController")
        memctrl.addParams(self.config.getMemCtrlConfig())

        # Create the memory backend subcomponent
        memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
        memory.addParams(self.config.getMemoryConfig())
        
        # Setup the links
        # Connect CPU to L1
        link_miface_l1cache = sst.Link("link_miface_l1cache" + str(nID))
        link_miface_l1cache.connect((miface, "port", "1ns"), (l1cache, "high_network_0", "1ns"))

        # Connect L1 to L2
        link_l1cache_l2 = sst.Link("link_l1cache_l2" + str(nID))
        link_l1cache_l2.connect((l1cache, "low_network_0", "10ns"), (l2cache, "high_network_0", "10ns"))

        # Connect L2 to memory controller
        link_l2_mem = sst.Link("link_l2_mem" + str(nID))
        link_l2_mem.connect((l2cache, "low_network_0", "40ns"), (memctrl, "direct_link", "40ns"))

        # Create remote memory controllers
        rmt_lsq = xbgas_cpu.setSubComponent("remote_memory", "revcpu.RevBasicRmtMemCtrl")
        rmt_nic = rmt_lsq.setSubComponent("xbgasNicIface", "revcpu.XbgasNIC")
        rmt_nic_iface = rmt_nic.setSubComponent("iface", "merlin.linkcontrol")

        rmt_nic_iface.addParam("link_bw", self.config.link_bw)
        rmt_nic_iface.addParam("input_buf_size", self.config.input_buf_size)
        rmt_nic_iface.addParam("output_buf_size", self.config.output_buf_size)
        
        return( rmt_nic_iface, "rtr_port", self.config.link_lat )

sst.merlin._params.update(config.getNetworkConfig())

topoGen = merlin.topoTorus()
sst.merlin._params.update(config.getTorusParams())

# topoGen = merlin.topoFatTree()
# sst.merlin._params.update(config.getFatTreeParams())

topoGen.prepParams()
topoGen.setEndPoint(EndpointCreator(config))
topoGen.build()