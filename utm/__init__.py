# DO NOT EDIT THE FOLLOWING LINE
import pkg_resources; __version__ = pkg_resources.require("utm")[0].version

# Generic config loading
import os

# -- Setup Configuration
from configuration import Configuration

# -- Setup dirs
configuration = Configuration.load(os.path.join(os.path.dirname(__file__), "config.global.yaml"))
                                   
try:
    # Load any local configuration
    local_config = Configuration.resolve(__name__, name="config.local.yaml")
    configuration  << Configuration.load(local_config)
except:
    print "No local configuration found, continuing..."


