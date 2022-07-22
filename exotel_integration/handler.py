import frappe
import requests
from frappe import _

# Endpoints for webhook
#
# Incoming Call:
# <site>/api/method/exotel_integration.handler.handle_request/<key>

# Exotel Reference:
# https://developer.exotel.com/api/
# https://support.exotel.com/support/solutions/articles/48283-working-with-passthru-applet

from frappe.integrations.utils import create_request_log

@frappe.whitelist(allow_guest=True)
def handle_request(**kwargs):
	try:
		if not is_integration_enabled():
			return

		request_log = create_request_log(
			kwargs,
			request_description="Exotel Incoming Call",
			service_name="Exotel",
			request_headers=frappe.request.headers
		)
		request_log.status = "Completed"
		exotel_settings = get_exotel_settings()
		if not exotel_settings.enabled:
			return

		call_payload = kwargs
		status = call_payload.get("Status")
		direction = call_payload.get('Direction')
		if status == 'free' or direction != 'incoming':
			return

		if call_log := get_call_log(call_payload):
			update_call_log(call_payload, call_log=call_log)
		else:
			create_call_log(
				call_id=call_payload.get('CallSid'),
				from_number=call_payload.get('CallFrom'),
				to_number=call_payload.get('DialWhomNumber'),
				medium=call_payload.get('To'),
				status=get_call_log_status(call_payload)
			)
	except Exception as e:
		request_log.status = "Failed"
		request_log.error = frappe.get_traceback()
		frappe.db.rollback()
		frappe.log_error(title="Error while creating incoming call record")
		frappe.db.commit()
	finally:
		request_log.save(ignore_permissions=True)

def update_call_log(call_payload, status='Ringing', call_log=None):
	call_log = call_log or get_call_log(call_payload)
	status = get_call_log_status(call_payload)
	try:
		if call_log:
			call_log.status = status
			# resetting this because call might be redirected to other number
			call_log.to = call_payload.get('DialWhomNumber')
			call_log.duration = call_payload.get('DialCallDuration') or 0
			call_log.recording_url = call_payload.get('RecordingUrl')
			call_log.start_time = call_payload.get('StartTime')
			call_log.end_time = call_payload.get('EndTime')
			call_log.save(ignore_permissions=True)
			frappe.db.commit()
			return call_log
	except Exception as e:
		frappe.log_error(title="Error while updating incoming call record")
		frappe.db.commit()

def get_call_log_status(call_payload):
	status = call_payload.get('DialCallStatus')
	call_type = call_payload.get("CallType")
	dial_call_status = call_payload.get("DialCallStatus")

	if call_type == "incomplete" and dial_call_status == "no-answer":
		status = "No Answer"
	elif call_type == "client-hangup" and dial_call_status == "canceled":
		status = "Canceled"
	elif call_type == "incomplete" and dial_call_status == "failed":
		status = "Failed"
	elif call_type == "completed":
		status = "Completed"

	return status


def get_call_log(call_payload):
	call_log_id = call_payload.get("CallSid")
	if frappe.db.exists("Call Log", call_log_id):
		return frappe.get_doc("Call Log", call_log_id)

def create_call_log(call_id, from_number, to_number, medium,
	status='Ringing', call_type='Incoming', link_to_document=None):
	call_log = frappe.new_doc('Call Log')
	call_log.id = call_id
	call_log.to = to_number
	call_log.medium = medium
	call_log.type = call_type
	call_log.status = status
	setattr(call_log, 'from', from_number)
	if link_to_document:
		call_log.append('links', link_to_document)
	call_log.save(ignore_permissions=True)
	frappe.db.commit()
	return call_log


@frappe.whitelist()
def get_call_status(call_id):
	endpoint = get_exotel_endpoint("Calls/{call_id}.json".format(call_id=call_id))
	response = requests.get(endpoint)
	return response.json().get("Call", {}).get("Status")


@frappe.whitelist()
def make_a_call(to_number, caller_id=None, link_to_document=None):
	if not is_integration_enabled():
		frappe.throw(_('Please setup Exotel intergration'), title=_('Integration Not Enabled'))

	endpoint = get_exotel_endpoint('Calls/connect.json?details=true')
	cell_number = frappe.get_value('Employee', {
		'user_id': frappe.session.user
	}, 'cell_number')

	if not cell_number:
		frappe.throw(_('You do not have mobile number set in your Employee master'))

	try:
		response = requests.post(endpoint, data={
			'From': cell_number,
			'To': to_number,
			'CallerId': caller_id,
			'Record': 'true' if frappe.db.get_single_value('Exotel Settings', 'record_call') else 'false',
			'StatusCallback': get_status_updater_url(),
			'StatusCallbackEvents[0]': 'terminal'
		})
		response.raise_for_status()
	except requests.exceptions.HTTPError as e:
		if exc := response.json().get('RestException'):
			frappe.throw(bleach.linkify(exc.get('Message')), title=_('Exotel Exception'))
	else:
		res = response.json()
		call_payload = res.get('Call', {})
		if link_to_document:
			link_to_document = json.loads(link_to_document)
		create_call_log(
			call_id=call_payload.get('Sid'),
			from_number=call_payload.get('From'),
			to_number=call_payload.get('To'),
			medium=call_payload.get('PhoneNumberSid'),
			call_type="Outgoing",
			link_to_document=link_to_document
		)

	return response.json()

def get_status_updater_url():
	from frappe.utils.data import get_url
	webhook_key = frappe.db.get_single_value('Exotel Settings', 'webhook_key')
	return get_url(f'api/method/erpnext.erpnext_integrations.exotel_integration.update_call_status/{webhook_key}')


def get_exotel_settings():
	return frappe.get_single("Exotel Settings")


def whitelist_numbers(numbers, caller_id):
	endpoint = get_exotel_endpoint("CustomerWhitelist")
	return requests.post(
		endpoint,
		data={
			"VirtualNumber": caller_id,
			"Number": numbers,
		},
	)

@frappe.whitelist()
def get_all_exophones():
	endpoint = get_exotel_endpoint('IncomingPhoneNumbers.json')
	response = requests.get(endpoint)
	return [
		phone.get('IncomingPhoneNumber', {}).get('PhoneNumber')
		for phone in response.json().get('IncomingPhoneNumbers', [])
	]

def get_exotel_endpoint(action):
	settings = get_exotel_settings()
	return "https://{api_key}:{api_token}@api.exotel.com/v1/Accounts/{sid}/{action}".format(
		api_key=settings.api_key, api_token=settings.api_token, sid=settings.account_sid, action=action
	)

def validate_request():
	# workaround security since exotel does not support request signature
	# /api/method/<exotel-integration-method>/<key>
	webhook_key = frappe.db.get_single_value('Exotel Settings', 'webhook_key')
	path = frappe.request.path[1:].split("/")
	key = path[3] if len(path) == 4 and path[3] else ''
	is_valid = key and key == webhook_key

	if not is_valid:
		frappe.throw(_('Unauthorized request'), exc=frappe.PermissionError)

def is_integration_enabled():
	return frappe.db.get_single_value('Exotel Settings', 'enabled', True)