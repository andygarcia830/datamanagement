// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Folder", {

   

    resource(frm){
        frappe.call({method:'datamanagement.data_management.services.services.fetch_folder_names', args:{
            'storage_type':frm.doc.storage_type,
            'resource':frm.doc.resource
         },
         callback:function(r){
             console.log(r.message)
            frm.set_df_property('folder', 'options', r.message);
            frm.refresh_field('folder');
         }
        });


    },

    refresh(frm){
        if(frappe.session.user != "Administrator" && frm.doc.metadata != null){
            frm.disable_save();
        }

        

        frappe.call({method:'datamanagement.data_management.services.services.fetch_resource_names', args:{
            'storage_type':frm.doc.storage_type
         },
         callback:function(r){
             console.log(r.message)
             frm.set_df_property('resource', 'options', r.message);
             frm.refresh_field('resource');
         }
        });

        if (frm.doc.resource != null){

            frappe.call({method:'datamanagement.data_management.services.services.fetch_folder_names', args:{
                'storage_type':frm.doc.storage_type,
                'resource':frm.doc.resource
            },
            callback:function(r){
                console.log(r.message)
                frm.set_df_property('folder', 'options', r.message);
                frm.refresh_field('folder');
            }
            });

        }

        if (frm.doc.name1 != null){
            frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.get_subfolder_names', args:{
                'name':frm.doc.name1
            },
            callback:function(r){
                console.log(r.message)
                frm.set_df_property('resource', 'options', r.message);
                frm.refresh_field('resource');
            }
            });
        }

        var has_access=0

 
        frm.add_custom_button(
            __('Reload Objects'),function(){
                frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_objects', args:{
                    'storage_type':frm.doc.storage_type,
                    'name':frm.doc.name1
               },
               callback:function(r){
                   console.log(r.message);
                   frm.reload_doc();
               }
               })
        }
        ,__('Actions')
        );
        
        if(frm.doc.metadata != null) {
            frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_access', args:{
                'metadata':frm.doc.metadata
            },
            callback:function(r){
                console.log(r.message)
                frm.set_value('data_owner', r.message.data_owner);
                frm.set_value('data_stewards', r.message.data_stewards);
                //console.log("OWNER="+r.message.data_owner+" USER=" + frappe.session.user);
                var gave_access=0;
                if(r.message.data_owner == frappe.session.user){
                    frm.enable_save();
                    show_access_buttons()
                    }
                for (var i=0; i < r.message.data_stewards.length && gave_access==0; i ++){
                    if (r.message.data_stewards[i].steward==frappe.session.user){
                        show_access_buttons();
                        gave_access=1;

                    }
                }
            
                }
            });
        }
        
        function show_access_buttons() {
        frm.add_custom_button(
            __('Upload Object'),function(){
                frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.get_subfolder_names', args:{
                    'name':frm.doc.name1
               },
               callback:function(r){
                   console.log(r.message)
                   let d = new frappe.ui.Dialog({
                    title: 'Enter details',
                    fields: [
                        {
                            label: 'Sub Directory',
                            fieldname: 'subdirectory',
                            fieldtype: 'Select',
                            options: r.message,
                            default: '/'


                        },
                        {
                            label: 'File',
                            fieldname: 'file',
                            fieldtype: 'Attach'
                        },


                    ],
                    primary_action_label: 'Submit',
                    primary_action(values) {
                        console.log(values);
                        d.hide();
                        frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.upload_object', args:{
                            'storage_type':frm.doc.storage_type,
                            'name':frm.doc.name1,
                            'file':values.file,
                            'subdirectory':values.subdirectory
                       },
                       callback:function(r){
                           console.log(r.message);
                           frm.reload_doc();
                       }
                       })
                    }
                });
                
                d.show();
               
               
               
                }
               })

                
               
            }
        ,__('Actions')
        );
    
        frm.add_custom_button(
            __('Delete Object'),function(){
                frappe.prompt(__('Enter Object Name To Delete'),({value})=>
                    frappe.confirm('Are you sure you want to delete Object '+value+"?",
                    // YES
                    ()=>{
                        frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.delete_object', args:{
                                'name':frm.doc.name1,
                                'object':value
                            },
                            callback:function(r){
                                frm.reload_doc();
                            }
                            })
                    },
                    // NO
                    ()=>{}
                    // 
                    )
                )
            }
            ,__('Actions')
        );

        frm.add_custom_button(
            __('Create Folder'),function(){
                frappe.prompt(__('Enter Folder Name'),({value})=>
                    frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.create_folder', args:{
                                'storage_type':frm.doc.storage_type,
                                'name':frm.doc.name1,
                                'resource':frm.doc.resource,
                                'object':value
                            },
                            callback:function(r){
                                frm.reload_doc();
                            }
                            })
                    
                )
            }
            ,__('Actions')
        );
        }


    },
	on_load(frm) {
        //frm.disable_save();
        frappe.call({method:'datamanagement.data_management.services.services.fetch_resource_names', args:{
           'storage_type':frm.doc.storage_type
        },
        callback:function(r){
            console.log(r.message)
            frm.set_df_property('resource', 'options', r.message);
            frm.refresh_field('resource');
        }
       });

       frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_objects', args:{
            'storage_type':frm.doc.storage_type,
            'name':frm.doc.name1
       },
       callback:function(r){
           console.log(r.message)
           frm.refresh_field('objects');
       }
       })

	},

    after_save(frm) {
        //frm.disable_save();
        frappe.call({method:'datamanagement.data_management.services.services.fetch_resource_names', args:{
           'storage_type':frm.doc.storage_type
        },
        callback:function(r){
            console.log(r.message)
            frm.set_df_property('resource', 'options', r.message);
            frm.refresh_field('resource');
        }
       });

       frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_objects', args:{
            'storage_type':frm.doc.storage_type,
            'name':frm.doc.name1
       },
       callback:function(r){
           console.log(r.message)
           frm.refresh_field('objects');
       }
       })

	},


    
});
