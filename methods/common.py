import subprocess
import threading
import time
import traceback

from utils.logger import log_info, log_error


def run_retrieval_command(command, success_keyword, timeout) -> bool:
    log_info(f"=========================================================\n"
          f"Executing: {command}")

    def target():
        # start bash command
        nonlocal process
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True  # Use universal_newlines instead of text
        )

        # print real-time output
        try:
            for line in iter(process.stdout.readline, ''):
                log_info(line)  # 实时输出
                if success_keyword in line:
                    process.terminate()  # 终止进程
                    nonlocal result
                    result = True
                    break
        except Exception as e:
            log_error(f"Error: {e}")

    process = None
    result = False

    # create and start thread
    thread = threading.Thread(target=target)
    thread.start()

    # wait threading executing, unitl timeout
    thread.join(timeout)

    # check timeout
    if thread.is_alive():
        log_info("Timeout reached. Terminating process.")
        if process:
            process.terminate()
        thread.join()  # ensure the thread has completed
        log_info(f"Finished Executing: {command}\n"
              f"=========================================================")
        return False

    log_info(f"Finished Executing: {command}\n"
          f"=========================================================")
    return result


def run_retrieval_command_legacy(command, success_keyword, timeout) -> bool:
    log_info(f"Executing: {command}...")
    data = None
    stdout_chunks = []
    stderr_chunks = []
    try:
        # 执行命令并设置超时时间
        data = subprocess.Popen(command, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                bufsize=0)
        start_time = time.time()
        while True:
            # 等待命令输出可读
            if data.stderr.readable():
                ret = data.stderr.read(100)
                stderr_chunks.append(ret)
                data.stderr.flush()
            # 检查命令是否结束
            if data.poll() is not None:
                break

            # 检查超时
            if time.time() - start_time > timeout:
                log_info("Timeout: OP ", time.time(), start_time)
                raise subprocess.TimeoutExpired(command, timeout)
            time.sleep(0.1)

        stdout = b''.join(stdout_chunks).decode('utf-8')
        stderr = b''.join(stderr_chunks).decode('utf-8')
        if success_keyword in stdout + stderr:
            return True
    except subprocess.TimeoutExpired as e:
        # 处理超时情况
        if data:
            data.kill()  # 终止进程
        stdout = b''.join(stdout_chunks).decode('utf-8')
        stderr = b''.join(stderr_chunks).decode('utf-8')
        if success_keyword in stderr + stdout:
            return True
    except Exception as e:
        log_error(f"{e} - {traceback.format_exc()}")
        return False
    return False
