import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def add_exotel_option():
	options = (frappe.get_meta("Communication Medium").get_field("communication_channel").options).split("\n")
	if "Exotel" not in options:
		options.append("Exotel")
		make_property_setter(
			"Communication Medium",
			"communication_channel",
			"options",
			"\n".join(options),
   			"Text",
			validate_fields_for_doctype=False
		)

def remove_exotel_option():
	options = (frappe.get_meta("Communication Medium").get_field("communication_channel").options).split("\n")
	if "Exotel" in options:
		options.remove("Exotel")
		make_property_setter(
      		"Communication Medium",
        	"communication_channel",
         	"options",
			"\n".join(options),
			"Text",
			validate_fields_for_doctype=False
		)
