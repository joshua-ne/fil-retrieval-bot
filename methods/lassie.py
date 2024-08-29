import os
import re
from typing import Union

from methods.common import run_retrieval_command
from utils.logger import log_error
from utils.utils import exec_cmd


def lassie_retrieval(provider, data_cid) -> bool:
    retrieval_cmd = f"lassie fetch --progress --providers {provider} -o /dev/null {data_cid}"
    res = run_retrieval_command(retrieval_cmd, "iB", 10)
    # os.system(f"rm {data_cid}.car")
    return res


def parse_provider_for_lassie(miner_id, timeout=10) -> Union[None, str]:
    peerid_pattern = r"PeerID:\s+(\S+)"
    multiaddrs_pattern = r"Multiaddrs:\s+(\S+)"

    miner_info_cmd = f"lotus state miner-info {miner_id}"
    text, err = exec_cmd(miner_info_cmd, timeout)
    if err:
        log_error(f"{miner_id} Parsing failed")
        return None
    else:
        peerid_match = re.search(peerid_pattern, text)
        if peerid_match:
            peerid = peerid_match.group(1)
        else:
            peerid = None

        # Extract Multiaddrs
        multiaddrs_match = re.search(multiaddrs_pattern, text)
        if multiaddrs_match:
            multiaddrs = multiaddrs_match.group(1)
        else:
            multiaddrs = None

        if multiaddrs and peerid:
            provider = multiaddrs + "/p2p/" + peerid
        else:
            provider = None
    return provider



