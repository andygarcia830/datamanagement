// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

 frappe.ui.form.on("MetaData", {
 	refresh(frm) {
        if(!frm.is_new()){

            frm.add_custom_button(
                __('Reconstruct JSON'),function(){
                    frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.create_json', args:{
                        'name':frm.doc.name
                    },
                    callback:function(r){
                        console.log(r.message)
                        frm.reload_doc();
                    }
                });
                    }
                , __("Actions")
            );
    
            

            frm.add_custom_button(
                __('Fetch Source Fields'),function(){
                // frm.save();
                frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.fetch_source_fields', args:{
                    'name':frm.doc.name,
                    'source':frm.doc.source
                },
                callback:function(r){
                        
                    frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.create_json', args:{
                            'name':frm.doc.name
                        }
                    });
                frm.reload_doc();
                }
                });
                
                }
            , __("Actions")
            );

            frm.add_custom_button(
                __('Create Data Mapping'),function(){
                window.location.replace('/app/data-mapping/new-data-mapping-1?metadata='+frm.doc.name1)
                
                }
                , __("Actions")
        );
        
        
        if (frm.doc.datasource != null && frm.doc.datasource != '') {
                frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.fetch_tables', args:{
                    'name':frm.doc.datasource
                },
                callback:function(r){
                    console.log(r.message)
                    frm.set_df_property('datasource_table', 'options', r.message);
                }
            });
                
        }
        }
 	},


    // before_save(frm){
       
    
    // },

    after_save(frm){

    frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.set_origin', args:{
            'doc':frm.doc.name
        },
        callback:function(r){
            console.log(r.message)
            create_json()
        }
    });

    function create_json(){
        frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.create_json', args:{
            'name':frm.doc.name
        },
        callback:function(r){
            console.log(r.message)
            frm.reload_doc()
            
        }
    });

    }
    

    },

    validate(frm){

        if (frm.doc.fields != null && frm.doc.fields != ''){

            frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.validate_sources', args:{
                    'doc':frm.doc.name1,
                    'fields':frm.doc.fields
                },
                callback:function(r){
                    console.log(r.message)
                    if (r.message != null && r.message != '') {
                        frappe.validated=false
                        frappe.throw(__(r.message));
                    }

                }
            });
            
        }
        }  ,
    

   datasource(frm){
    if (frm.doc.datasource != null && frm.doc.datasource != '') {
        frappe.call({method:'datamanagement.data_management.doctype.metadata.metadata.fetch_tables', args:{
            'name':frm.doc.datasource
        },
        callback:function(r){
            console.log(r.message)
            frm.set_df_property('datasource_table', 'options', r.message);
        }
    });
        
}


   }

   
 });
