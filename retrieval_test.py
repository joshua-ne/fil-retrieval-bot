import json
import traceback
from typing import Tuple

import requests

from retrieval_query import RetrievalQuery
from retrieve import process_one_sp
from utils.utils import make_table


def collect_retrieves_from_api(sp_list: list, client: str, limit: int, start_datetime: str, end_datetime: str) -> dict:
    print(f"sp_list: {sp_list}, client: {client}, limit: {limit}")
    url = "http://filproof.com/api/get_datacid_list"
    sp_cids = {}
    for sp in sp_list:
        data = {
            "client": client,
            "SP": sp,
            "start": start_datetime,
            "end": end_datetime,
            "limit": limit
        }
        print(data)
        response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code == 200 and response.json().get("Data"):
            sp_cids[sp] = response.json().get("Data")
            print(f"{sp}: {sp_cids[sp]}")
        else:
            sp_cids[sp] = []
        # TODO handle errors
    return sp_cids


def run_auto_retrieval_test(retrieval_query) -> Tuple[str, str]:
    try:
        retrieves = collect_retrieves_from_api(retrieval_query.sp_list, retrieval_query.client, retrieval_query.limit,
                                               retrieval_query.start_datetime, retrieval_query.end_datetime)
        results = [f"miner_id, retrieval_rate, retrieval_success_counts, retrieval_fail_counts"]
        for miner_id, data_cid_list in retrieves.items():
            if len(data_cid_list) == 0:
                result = f"{miner_id}, NA, {0}, {0}"
            else:
                success_count, fail_count = process_one_sp(miner_id, data_cid_list, retrieval_query.method)
                result = f"{miner_id}, {int(100 * success_count / (success_count + fail_count))}%, {success_count}, {fail_count}"
            results.append(result)
        results = '\n'.join(results)
        return "", make_table(results)
    except Exception as e:
        return f"error running test: {e} - {traceback.format_exc()}", ""


def run_csv_file_retrieval_test(retrieval_query) -> Tuple[str, str]:
    return "to be implemented...", ""


def run_retrieval_test(retrieval_query: RetrievalQuery) -> Tuple[str, str]:
    if retrieval_query.mode == "auto":
        return run_auto_retrieval_test(retrieval_query)
    elif retrieval_query.mode == "csv_file":
        return run_csv_file_retrieval_test(retrieval_query)
    else:
        return f"not supported mode: {retrieval_query.mode}", ""
