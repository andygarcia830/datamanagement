// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("MetaData", {
 	refresh(frm) {
         frm.add_custom_button(
             __('Create Data Mapping'),function(){
                window.location.replace('/app/data-mapping/new-data-mapping-1?metadata='+frm.doc.name1)
               
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
                   frm.reload_doc();
               }
              });
              
             }
        );

 	},

    after_save(frm){
        frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.create_json', args:{
            'name':frm.doc.name
        },
        callback:function(r){
            console.log(r.message)
            frm.reload_doc();
        }
    });
    },
 });
