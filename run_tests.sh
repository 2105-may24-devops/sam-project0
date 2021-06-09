#!/bin/bash
#set -x
python account.py
python customer.py
python bank.py
python manager.py < test_stdin_create_bank_and_customer_with_account_log.txt
python manager.py < test_stdin_show_customer_log.txt
