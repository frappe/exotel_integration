frappe.ui.form.on('Exotel Settings', {
	refresh: function(frm) {
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
	}
});