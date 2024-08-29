from retrieval_query import parse_retrieval_query
from retrieval_test import run_auto_retrieval_test

if __name__ == "__main__":
    instruction = ("trigger:run_retrieval_test method=boost sp_list=f01111110,f01909705,f023422 "
                  "client=f14zmgrcgayihubfptjpn42xs2tgk7cpkjxgnjsyq limit=30")

    eq, q = parse_retrieval_query(instruction)
    print(eq, q)
    er, r = run_auto_retrieval_test(q)
    print(er, r)