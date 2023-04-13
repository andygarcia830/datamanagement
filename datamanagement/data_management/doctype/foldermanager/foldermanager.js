// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("FolderManager", {
	refresh(frm) {
        frm.disable_save();

        frappe.call({method:'datamanagement.data_management.services.services.fetch_resource_names', args:{
            'storage_type':frm.doc.storage_type
         },
         callback:function(r){
             console.log(r.message)
             frm.set_df_property('resource', 'options', r.message);
             frm.refresh_field('resource');
         }
        });


        
        frm.add_custom_button(
            __('Create Folder'),function(){
                frappe.prompt(__('Enter Folder Name'),({value})=>
                    frappe.call({method:'datamanagement.data_management.doctype.foldermanager.foldermanager.create_folder', args:{
                                'storage_type':frm.doc.storage_type,
                                'resource':frm.doc.resource,
                                'object':value
                            },
                            callback:function(r){
                                frm.is_dirty=false
                                frappe.call({method:'datamanagement.data_management.services.services.fetch_folder_names', args:{
                                    'storage_type':frm.doc.storage_type,
                                    'resource':frm.doc.resource
                                 },
                                 callback:function(r){
                                     console.log(r.message)
                                     frm.doc.folders=null;
                                     for (var i=0; i < r.message.length; i ++){
                                        var row = frappe.model.add_child(frm.doc, "Folder Objects", "folders");
                                        row.object = r.message[i];
                                        }
                                     refresh_field('folders');
                                 }
                                });
                        
                                
                            }
                            })
                    
                )
            }
            ,__('Actions')
        );
        


    },

	
    storage_type(frm) {
        frm.disable_save();

        frappe.call({method:'datamanagement.data_management.services.services.fetch_resource_names', args:{
            'storage_type':frm.doc.storage_type
         },
         callback:function(r){
             console.log(r.message)
             frm.set_df_property('resource', 'options', r.message);
             frm.refresh_field('resource');
         }
        });

	},

    resource(frm){
        frappe.call({method:'datamanagement.data_management.services.services.fetch_folder_names', args:{
            'storage_type':frm.doc.storage_type,
            'resource':frm.doc.resource
         },
         callback:function(r){
             console.log(r.message)
             frm.doc.folders=null;
             for (var i=0; i < r.message.length; i ++){
                var row = frappe.model.add_child(frm.doc, "Folder Objects", "folders");
                row.object = r.message[i];
                }
             refresh_field('folders');
         }
        });


    },

});
