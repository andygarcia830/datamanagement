// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("MetaData", {
 	refresh(frm) {
         frm.add_custom_button(
             __('Generate JSON'),function(){
                frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.create_json', args:{
                    'name':frm.doc.name
                },
                callback:function(r){
                    console.log(r.message)
                }
               });
              }
         );

         frm.add_custom_button(
            __('Fetch Source Fields'),function(){
               frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.fetch_source_fields', args:{
                   'name':frm.doc.name,
                   'source':frm.doc.source
               },
               callback:function(r){
                   console.log(r.message)
               }
              });
             }
        );

 	},
 });
