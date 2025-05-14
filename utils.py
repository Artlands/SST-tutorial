import os
import sst
import configparser
 

class Config:
  def __init__(self, cfgFile, **kwargs):
    cp = configparser.ConfigParser()
    if not cp.read(cfgFile):
      raise Exception("Failed to read config file: " + cfgFile)
    
    self.verbose = "verbose" in kwargs and kwargs["verbose"]
    
    # CPU Config
    self.clock              = cp.get('CPU', 'clock')
    self.program            = cp.get('CPU', 'program')
    self.memSize            = cp.get('CPU', 'memSize')
    self.shared_memory_size = cp.get('CPU', 'shared_memory_size')
    
    # L1 Cache Config
    self.l1_cache_frequency       = cp.get('L1Cache', 'cache_frequency')
    self.l1_access_latency_cycles = cp.get('L1Cache', 'access_latency_cycles')
    self.l1_cache_size            = cp.get('L1Cache', 'cache_size')
    self.l1_cache_line_size       = cp.get('L1Cache', 'cache_line_size')
    self.l1_associativity         = cp.get('L1Cache', 'associativity')
    self.l1_replacement_policy    = cp.get('L1Cache', 'replacement_policy')
    self.l1_coherence_protocol    = cp.get('L1Cache', 'coherence_protocol')

    # L2 Cache Config
    self.l2_cache_frequency       = cp.get('L2Cache', 'cache_frequency')
    self.l2_access_latency_cycles = cp.get('L2Cache', 'access_latency_cycles')
    self.l2_mshr_latency_cycles   = cp.get('L2Cache', 'mshr_latency_cycles')
    self.l2_cache_size            = cp.get('L2Cache', 'cache_size')
    self.l2_cache_line_size       = cp.get('L2Cache', 'cache_line_size')
    self.l2_associativity         = cp.get('L2Cache', 'associativity')
    self.l2_replacement_policy    = cp.get('L2Cache', 'replacement_policy')
    self.l2_coherence_protocol    = cp.get('L2Cache', 'coherence_protocol')

    # # MemCtrl Config
    # self.addr_range_start    = cp.get('MemoryCtrl', 'addr_range_start')
    # self.backing             = cp.get('MemoryCtrl', 'backing')

    # Memory Config
    self.memory_access_time = cp.get('Memory', 'access_time')
    
    # Network Config
    self.link_lat        = cp.get('Network', 'link_lat')
    self.link_bw         = cp.get('Network', 'link_bw')
    self.flit_size       = cp.get('Network', 'flit_size')
    self.xbar_bw         = cp.get('Network', 'xbar_bw')
    self.input_latency   = cp.get('Network', 'input_latency')
    self.output_latency  = cp.get('Network', 'output_latency')
    self.input_buf_size  = cp.get('Network', 'input_buf_size')
    self.output_buf_size = cp.get('Network', 'output_buf_size')

    # Network Topology
    if cp.has_section('Torus'):
      self.num_dims    = cp.get('Torus', 'num_dims')
      self.shape       = cp.get('Torus', 'shape')
      self.width       = cp.get('Torus', 'width')
      self.local_ports = cp.get('Torus', 'local_ports')
      self.cpus_per_group = self.local_ports
    
    if cp.has_section('FatTree'):
      self.shape = cp.get('FatTree', 'shape')
    
    if cp.has_section('DragonFly'):
      self.groups            = cp.get('DragonFly', 'group_count')
      self.hosts_per_router  = cp.get('DragonFly', 'hosts_per_router')
      self.routers_per_group = cp.get('DragonFly', 'routers_per_group')
      self.intergroup_links  = cp.get('DragonFly', 'intergroup_links')
    
  def getCpuConfig(self):
    params = dict({
      "verbose"            : 1,                             # Verbosity
      "clock"              : self.clock,                    # Clock
      "program"            : self.program,                  # Target executable
      "memSize"            : int(self.memSize),             # Memory size in bytes
      "startAddr"          : "[0:0x00000000]",              # Starting address for core 0
      "machine"            : "[0:RV64GC_Xbgas]",            # Machine type
      "memCost"            : "[0:1:10]",                    # Memory loads required 1-10 cycles
      "enable_xbgas"       : 1,                             # Enable XBGAS support
      "enableMemH"         : 1,                             # Enable memH support
      "shared_memory_size" : int(self.shared_memory_size),  # Shared memory size
      "splash"             : 0                              # Display the splash message
    })
    return params
  
  def getL1CacheConfig(self):
    params = dict({
      "L1"                    : 1,
      "cache_frequency"       : self.l1_cache_frequency,
      "access_latency_cycles" : self.l1_access_latency_cycles,
      "cache_size"            : self.l1_cache_size,
      "cache_line_size"       : self.l1_cache_line_size,
      "associativity"         : self.l1_associativity,
      "replacement_policy"    : self.l1_replacement_policy,
      "coherence_protocol"    : self.l1_coherence_protocol,
    })
    return params

  def getL2CacheConfig(self):
    params = dict({
      "L1"                    : 0,  # Not an L1
      "cache_frequency"       : self.l2_cache_frequency,
      "access_latency_cycles" : self.l2_access_latency_cycles,
      "mshr_latency_cycles"   : self.l2_mshr_latency_cycles,
      "cache_size"            : self.l2_cache_size,
      "cache_line_size"       : self.l2_cache_line_size,
      "associativity"         : self.l2_associativity,
      "replacement_policy"    : self.l2_replacement_policy,
      "coherence_protocol"    : self.l2_coherence_protocol,
    })
    return params
  
  def getMemCtrlConfig(self):
    params = dict({
      "clock"            : self.clock,
      "addr_range_start" : 0,
      "addr_range_end"   : int(self.memSize) - 1,
      "backing"          : "malloc"
    })
    return params

  def getMemoryConfig(self):
    params = dict({
      "access_time" : self.memory_access_time,
      "mem_size"    : "8GB"
    })
    return params

  def getNetworkConfig(self):
    params = dict({
      "link_lat"        : self.link_lat,
      "link_bw"         : self.link_bw,
      "flit_size"       : self.flit_size,
      "xbar_bw"         : self.xbar_bw,
      "input_latency"   : self.input_latency,
      "output_latency"  : self.output_latency,
      "input_buf_size"  : self.input_buf_size,
      "output_buf_size" : self.output_buf_size,
      "xbar_arb"        : "merlin.xbar_arb_lru"
    })
    return params
  
  def getFatTreeParams(self):
    params = dict({
      "fattree.shape" : self.shape,
    })
    return params
    
  def getTorusParams(self):
    params = dict({
      "num_dims"          : self.num_dims,
      "torus.shape"       : self.shape,
      "torus.width"       : self.width,
      "torus.local_ports" : self.local_ports,
    })
    return params
  
  def getDragonFlyParams(self):
    params = dict({
      "dragonfly.hosts_per_router" : self.hosts_per_router,
      "dragonfly.routers_per_group": self.routers_per_group,
      "dragonfly.intergroup_links" : self.intergroup_links,
      "dragonfly.num_groups"       : self.groups,
      "dragonfly.algorithm"        : "minimal",
    })
    return params
  