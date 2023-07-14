frappe.ui.form.on('Exotel Settings', {
	refresh: function(frm) {
		frm.trigger("migration_warning");

		if (frm.doc.webhook_key) {
			const key = frm.doc.webhook_key;
			const site = window.location.origin;

			frm.get_field('integration_info').$wrapper.html(`
				<hr>
				<b>Note:</b> Use following link to setup call popup<br><br>
				<code style="word-break: break-all; cursor: copy;">${site}/api/method/exotel_integration.handler.handle_request?key=${key}</code><br><br>
			`).find('code').click(e => {
				let text = $(e.currentTarget).text();
				frappe.utils.copy_to_clipboard(text);
			});
		}
	},

	migration_warning: function(frm) {
		// Migrating users from ERPNext might not have the key but integration will still be enabled
		// Warn such user to reconfigure exotel.
		if (!frm.doc.webhook_key && frm.doc.enabled) {
			frm.dirty();
			frm.dashboard.add_comment(__("Exotel is not configured properly, please re-save the document and update the call popup link on Exotel."), "red");
		}
	}
});