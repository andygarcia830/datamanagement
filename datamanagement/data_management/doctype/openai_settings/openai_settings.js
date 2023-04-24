// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("OpenAI Settings", {
	after_save(frm) {
        frappe.call({method:'datamanagement.data_management.doctype.openai_settings.openai_settings.set_key', args:{
            'key':frm.doc.openai_api_key
        },
        callback:function(r){
            
        }
        });

	},
});
