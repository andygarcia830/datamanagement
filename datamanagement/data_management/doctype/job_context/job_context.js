// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Context", {
	refresh(frm) {
        frappe.call({method:'datamanagement.data_management.doctype.job_context.job_context.fetch_client_data', args:{
        },
        callback:function(r){
            console.log(r.message);
            frm.set_value("client_namespace",r.message.client_namespace);
            frm.set_value("storage_type",r.message.storage_type);
            
        }
        })

	},
});
