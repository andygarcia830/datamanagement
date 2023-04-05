// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("AWS Test", {
 	refresh(frm) {
        frm.add_custom_button(
            __('TEST'),function(){
                frappe.call({method:'datamanagement.data_management.services.services.test_aws', args:{
                    'name':frm.doc.name
                },
                callback:function(r){
                    console.log(r.message)
                    frappe.msgprint(r.message)

                }
               });
                }
        )
 	},
});
