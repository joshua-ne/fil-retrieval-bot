from typing import Tuple

from methods.boost import boost_retrieval
from methods.lassie import lassie_retrieval, parse_provider_for_lassie


def not_supported_retrieval(sp, data_cid) -> bool:
    return False


switch_dict = {
    "boost": boost_retrieval,
    "lassie": lassie_retrieval
}


def process_one_retrieve(provider, data_cid, method) -> bool:
    return switch_dict.get(method, not_supported_retrieval)(provider, data_cid)


def convert_sp_to_provider(sp, method):
    if method == "boost":
        return sp
    elif method == "lassie":
        return parse_provider_for_lassie(sp)


def process_one_sp(sp, data_cid_list, method) -> Tuple[int, int]:
    provider = convert_sp_to_provider(sp, method)
    if not provider:
        return 0, len(data_cid_list)
    success, fail = 0, 0
    for cid in data_cid_list:
        if process_one_retrieve(provider, cid, method):
            success += 1
        else:
            fail += 1
    return success, fail
