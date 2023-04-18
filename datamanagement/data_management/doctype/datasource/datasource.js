// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("DataSource", {
	refresh(frm) {

        show_access_buttons();

        function show_access_buttons() {
             frm.add_custom_button(
                __('Create Folders'),function(){
                    var folder=frm.doc.database_name
                    var subfolders=frm.doc.tables
                    var str = ''
                    for (var i=0; i < subfolders.length; i ++) {
                        str+="<br>"+folder+"/"+subfolders[i].table_name

                    }
                    frappe.confirm(__('Create Folders?'+str),()=>{
                       
                        frappe.call({method:'datamanagement.data_management.doctype.datasource.datasource.create_folders', args:{
                                    'name':frm.doc.name
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
