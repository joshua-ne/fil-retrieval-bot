import os

from methods.common import run_retrieval_command


def boost_retrieval(provider, data_cid) -> bool:
    retrieval_cmd = f"boost --vv retrieve --provider {provider} {data_cid}"
    res = run_retrieval_command(retrieval_cmd, "iB", 10)
    # os.system(f"rm {data_cid}.car")
    return res
