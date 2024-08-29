import subprocess

from utils.logger import log_info, log_error


def exec_cmd(src_cmd, timeout=10):
    log_info(f"Process running  {src_cmd}")
    try:
        data = subprocess.Popen(src_cmd, shell=True, close_fds=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        stdout, stderr = data.communicate(timeout=timeout)
        stdout_ret = stdout.decode('utf-8', 'ignore')
        stderr_res = stderr.decode('utf-8', 'ignore')

        return stdout_ret, None

    except subprocess.TimeoutExpired as err:
        log_error("exec_cmd", err)

    return False, "Unknown Problem"


def make_table(result):
    # Split the input data into lines
    lines = result.strip().split('\n')

    # Extract the header
    header = lines[0].split(', ')

    # Extract the rows of data
    rows = [line.split(', ') for line in lines[1:]]

    # Format the header
    markdown_table = '| ' + ' | '.join(header) + ' |\n'
    markdown_table += '| ' + ' | '.join(['---'] * len(header)) + ' |\n'

    # Format each row
    for row in rows:
        markdown_table += '| ' + ' | '.join(row) + ' |\n'

    return markdown_table


