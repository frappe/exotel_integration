# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
import requests
from frappe import _
from frappe.model.document import Document


class ExotelSettings(Document):
	def validate(self):
		self.verify_credentials()
		self.set_webhook_key()

	def verify_credentials(self):
		if self.enabled:
			response = requests.get(
				"https://api.exotel.com/v1/Accounts/{sid}".format(sid=self.account_sid),
				auth=(self.api_key, self.get_password("api_token")),
			)
			if response.status_code != 200:
				frappe.throw(
					_(f"Please enter valid exotel Account SID, API key & API token: {response.reason}"),
					title=_("Invalid credentials"),
				)

	def set_webhook_key(self):
		if not self.webhook_key:
			key = frappe.generate_hash(length=20)
			self.webhook_key = key
