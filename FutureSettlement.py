# -*- coding:utf-8 -*-
# TianxiaoHu, HansXCao, 20161230
# 期货公司结算单数据提取

import re
import pandas as pd

"""
Useage:
filepath = u"D:\南华期货结算记录\结算单_20161116.txt"
client_info, account_summary, transaction_record = get_data(filepath)
print client_info, account_summary, transaction_record
"""
global mode
mode = '0'

def separate_text(filepath):
	rawtext = open(filepath).read()
	rawtext = rawtext.decode("gbk").encode('utf-8')
	global mode 
	if '出入金明细' in rawtext and '成交记录' not in rawtext:
		separator = '资金状况  币种：人民币  Account Summary  Currency：CNY|出入金明细 Deposit/Withdrawal'
		mode = '1'
	elif '出入金明细' in rawtext and '成交记录' in rawtext:
		mode = '2'
		separator = '资金状况  币种：人民币  Account Summary  Currency：CNY|出入金明细 Deposit/Withdrawal|成交记录 Transaction Record|平仓明细 Position Closed |'
	elif '出入金明细' not in rawtext:
		mode = '3'
		separator = '资金状况  币种：人民币  Account Summary  Currency：CNY|成交记录 Transaction Record|平仓明细 Position Closed|'
	elif '成交记录' not in rawtext:
		mode = '4'
	return re.split(separator, rawtext)


def get_client_info(separated):
	client_info = separated
	client_info = client_info.split('Settlement Statement(MTM)')[1]
	client_info = client_info.replace('\r\n', '|')
	client_info = client_info.replace(' '*5, '|')
	client_info = client_info.split('|')
	res = {}
	for i in client_info:
		if len(i) > 10:
			res[i.split('：')[0]] = i.split('：')[1]
	return pd.DataFrame(res, index = [' '])


def get_account_summary(separated):
	account_summary = separated
	account_summary = account_summary.split('\r\n')
	account_summary = account_summary[2: -2]

	account_dict = {}
	for row in account_summary:
		temp = re.split('\s{2,}', row)
		#print temp
		if temp == ['']:
			continue
		account_dict[temp[0].replace('：', '')] = temp[1]
		account_dict[temp[2].replace('：', '')] = temp[3]
	return pd.DataFrame(account_dict, index=[' '])


def get_transaction_record(separated):
	transaction_record = separated
	transaction_record = transaction_record.split('-' * 183)
	
	header = transaction_record[1]
	header = header.split('\r\n')
	header_cn = header[1].replace(' ', '').split('|')
	header_en = header[2].replace(' ', '').split('|')
	header_cn = header_cn[1:-1]
	header_en = header_en[1:-1]
	header = [header_cn[i] + ' ' + header_en[i] for i in range(len(header_cn))]

	transaction_record_df = pd.DataFrame(columns = header)

	content = transaction_record[2]
	content = content.split('\r\n')
	content = content[1: -1]
	for row in content:
		l = row.replace(' ', '').split('|')
		l = l[1: -1]
		transaction_record_df.ix[str(transaction_record_df.shape[0] + 1)] = l
	return transaction_record_df


def get_data(filepath):
	"""
	args:
	filepath - .txt file path

	return:
	client_info - pd.DataFrame 
	account_summary - pd.DataFrame 
	transaction_record - pd.DataFrame 
	"""
	separated = separate_text(filepath)
	global mode 
	if mode == '1':
		client_info = get_client_info(separated[0])
		account_summary = pd.DataFrame()
		transaction_record = pd.DataFrame()
		return client_info, account_summary, transaction_record
	elif mode == '2':
		client_info = get_client_info(separated[0])
		account_summary = get_account_summary(separated[2])
		transaction_record = get_transaction_record(separated[3])
	elif mode == '3':
		client_info = get_client_info(separated[0])
		account_summary = get_account_summary(separated[1])
		transaction_record = get_transaction_record(separated[2])
	return client_info, account_summary, transaction_record


