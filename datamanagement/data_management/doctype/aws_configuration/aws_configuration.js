// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("AWS Configuration", {
	after_save(frm) {
        frappe.call({method:'datamanagement.data_management.doctype.aws_configuration.aws_configuration.import_aws_credentials', args:{
        },
        callback:function(r){
            console.log(r.message)
        }
    });

	},
});
