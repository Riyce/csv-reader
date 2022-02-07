import csv
import os.path
import socket
from pathlib import Path
from time import time
from typing import Dict

from config import BASE_DIR


def get_file_name(filename: str) -> str:
	now = int(time())
	return f"{now}-{filename}"


class CSVWorker:
	DIALECT_PARAMS = dict(
		delimiter=";",
		fieldnames=["ip", "mask", "subnet", "num", "user", "error"]
	)
	IP_ERROR = "IP err"
	MASK_ERROR = "Mask err"
	SUBNET_ERROR = "Subnet err"
	INCORRECT_SUBNET_ERROR = "Subnet incorrect"
	NUM_ERROR = "Num err"

	def __init__(self, file) -> None:
		self.file = file
		self.filename = os.path.basename(file)
		self.nums = set()
		self.nums_count = 0

	@staticmethod
	def is_valid_ip(ip: str) -> bool:
		try:
			socket.inet_aton(ip)
			return True
		except socket.error:
			return False

	@staticmethod
	def get_subnet_address(ip: str, mask: str) -> str:
		if mask and ip:
			ip_list = ip.split(".")
			mask_list = mask.split(".")
			sub_list = []
			for num in range(len(ip_list)):
				try:
					sub_octet = int(ip_list[num]) & int(mask_list[num])
				except IndexError:
					return ""
				sub_list.append(str(sub_octet))
			return ".".join(sub_list)
		return ""

	def is_correct_subnet(self, ip: str, mask: str, subnet: str) -> bool:
		if mask and ip:
			if self.get_subnet_address(ip, mask) == subnet:
				return True
		return False

	@staticmethod
	def is_valid_num(num: str) -> bool:
		try:
			int(num)
			return True
		except ValueError:
			return False

	def upgrade_row(self, row: Dict[str, str]) -> Dict[str, str]:
		for key, value in row.items():
			if key == "ip":
				if not self.is_valid_ip(value):
					row["error"] = self.IP_ERROR
					break
			elif key == "mask":
				if not self.is_valid_ip(value):
					row["error"] = self.MASK_ERROR
					break
			elif key == "subnet":
				if value:
					if not self.is_valid_ip(value):
						row["error"] = self.SUBNET_ERROR
						break
					if not self.is_correct_subnet(row["ip"], row["mask"], value):
						row["error"] = self.INCORRECT_SUBNET_ERROR
						break
				else:
					row["subnet"] = self.get_subnet_address(row["ip"], row["mask"])
			elif key == "num":
				if value:
					if not self.is_valid_num(value):
						row["error"] = self.NUM_ERROR
						break
					self.nums.add(int(value))
					if self.nums_count == len(self.nums):
						new_value = max(self.nums) + 1
						row["num"] = new_value
						self.nums.add(new_value)
						self.nums_count += 1
				else:
					new_value = max(self.nums) + 1
					row["num"] = new_value
					self.nums.add(new_value)
					self.nums_count += 1
		return row

	def process(self) -> Path:
		new_file = BASE_DIR.joinpath("media", "upgraded", self.filename)
		with open(new_file, "w") as _:
			pass
		with open(self.file, mode="r", encoding="cp1251") as file:
			reader = csv.DictReader(file, **self.DIALECT_PARAMS)
			for row in reader:
				new_row = self.upgrade_row(row)
				with open(new_file, "a") as new_csv_file:
					writer = csv.DictWriter(new_csv_file, **self.DIALECT_PARAMS)
					writer.writerow(new_row)
		return new_file
