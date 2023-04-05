// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("MetaData", {
 	refresh(frm) {
        if(!frm.is_new()){
         frm.add_custom_button(
             __('Create Data Mapping'),function(){
                window.location.replace('/app/data-mapping/new-data-mapping-1?metadata='+frm.doc.name1)
               
              }
         );

         frm.add_custom_button(
            __('Fetch Source Fields'),function(){
                frm.save();
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

            }
 	},


    // before_save(frm){
    //     frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.set_origin', args:{
    //         'doc':frm.doc
    //     },
    //     callback:function(r){
    //         console.log(r.message)
    //         frm.reload_doc();
    //     }
    // });
    // fields_add: function(frm,cdt,cdn) { // "fields" is the name of the table field in MetaData, "_add" is the event
    //     // frm: current MetaData form
    //     // cdt: child DocType 'MetaDataReference'
    //     // cdn: child docname (something like 'a6dfk76')
    //     // cdt and cdn are useful for identifying which row triggered this event
    //     console.log('A row has been added to the links table ');
    //     frappe.msgprint('A row has been added to the links table');
    
    
    // },

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
