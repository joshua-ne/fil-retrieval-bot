import re
import traceback
from typing import Union, Tuple

from pydantic import BaseModel, Field

from utils.logger import log_info


class RetrievalQuery(BaseModel):
    mode: str = Field("auto", description="csv_file or auto")
    method: str = Field("", description="Retrieval method, currently boost or lassie")
    csv_file_url: str = Field("", description="csv file url")
    sp_list: list = Field(default_factory=list, description="list of SP to check")
    client: str = Field("", description="client address to check")
    start_datetime: str = Field("", description="start datetime to check")
    end_datetime: str = Field("", description="end datetime to check")
    limit: int = Field(5, description="number of tests to run")


# trigger:run_retrieval_test method=boost mode="auto" sp_list=f01989013,f01989014,f023422 client=f1188abvie limit=5
def parse_retrieval_query(instruction) -> Tuple[str, Union[None, RetrievalQuery]]:
    log_info(instruction)
    try:
        # Regular expression pattern to match parameters in the command
        pattern = r'(\w+)=(".*?"|\S+)'

        # Find all matches in the command
        matches = re.findall(pattern, instruction)

        # Initialize an empty dictionary to store the parameters
        params = {}

        for key, value in matches:
            # Remove surrounding quotes from the value if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            # Split comma-separated values for sp_list
            if key == "sp_list":
                params[key] = value.split(',')
            # Convert limit to an integer
            elif key == "limit":
                params[key] = int(value)
            else:
                params[key] = value

        # Create an instance of RetrievalQuery with the parsed parameters
        return "", RetrievalQuery(**params)
    except Exception as e:
        return f"error parsing: {e}, {traceback.format_exc()}", None

