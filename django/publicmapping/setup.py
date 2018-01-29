#!/usr/bin/python
"""
Set up DistrictBuilder.

This management command will examine the main configuration file for
correctness, import geographic levels, create spatial views, create
geoserver layers, and construct a default plan.

This file is part of The Public Mapping Project
https://github.com/PublicMapping/

License:
    Copyright 2010-2012 Micah Altman, Michael McDonald

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Author:
    Andrew Jennings, David Zwarg
"""

from optparse import OptionParser
import sys
from redistricting import StoredConfig
import logging

logging.basicConfig(format='%(message)s')
logging._srcFile = None
logging.logThreads = 0
logging.logProcesses = 0

logger = logging.getLogger()

def main():
    """
    Main method to start the setup of DistrictBuilder.
    """
    usage = "usage: %prog [options] SCHEMA CONFIG"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbosity', dest="verbosity",
            help="Verbosity level; 0=minimal output, 1=normal output, 2=all output",
            default=1, type="int")

    (options, args) = parser.parse_args()

    setup_logging(options.verbosity)

    if len(args) != 2:
        logger.warning("""
ERROR:

    This script requires a configuration file and a schema. Please check
    the command line arguments and try again.
""")
        sys.exit(1)

    try:
        config = StoredConfig(args[1], schema_file=args[0])
    except Exception as e:
        logger.exception("Error initializing config")
        sys.exit(1)

    if not config.validate():
        logger.info("Configuration could not be validated.")
        sys.exit(1)

    logger.info("Validated config.")

    status = config.write_settings()
    if status:
        logger.info("Generated Django settings.")
    else:
        logger.info("Failed to generate settings.")
        sys.exit(1)

    # Success! Exit-code 0
    sys.exit(0)

def setup_logging(verbosity):
    """
    Setup logging for setup.
    """
    if verbosity > 1:
        logger.setLevel(logging.DEBUG)
    elif verbosity > 0:
        logger.setLevel(logging.INFO)

if __name__ == "__main__":
    main()

