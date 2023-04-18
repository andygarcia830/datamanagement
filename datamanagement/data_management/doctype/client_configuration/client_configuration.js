// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Client Configuration", {
	refresh(frm) {

        show_access_buttons();

        function show_access_buttons() {
             frm.add_custom_button(
                __('Create Bucket'),function(){
                    
                    
                    frappe.confirm(__('Create Bucket?<br>'+frm.doc.client_namespace),()=>{
                       
                        frappe.call({method:'datamanagement.data_management.doctype.client_configuration.client_configuration.create_bucket', args:{
                                    'storage_type':frm.doc.storage_type,
                                    'name':frm.doc.client_namespace
                                },
                                callback:function(r){
                                    //frm.reload_doc();
                                }
                                })
                            },()=>

                            {
                                // action to perform if No is selected
                            }
                    )
                }
                ,__('Actions')
            );
            }


	},
});
