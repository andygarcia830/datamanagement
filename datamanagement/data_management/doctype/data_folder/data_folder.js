// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Folder", {
    refresh(frm){
        frm.add_custom_button(
            __('Reload Objects'),function(){
                frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_objects', args:{
                    'storage_type':frm.doc.storage_type,
                    'name':frm.doc.name1
               },
               callback:function(r){
                   console.log(r.message)
               }
               })
        }
        ,__('Actions')
        );
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
                           console.log(r.message)
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
                                'storage_type':frm.doc.storage_type,
                                'name':frm.doc.name1,
                                'folder':frm.doc.folder,
                                'object':value
                            },
                            callback:function(r){
                                frm.doc.reload_doc()
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
                                'folder':frm.doc.folder,
                                'object':value
                            },
                            callback:function(r){
                                frm.doc.reload_doc()
                            }
                            })
                    
                )
            }
            ,__('Actions')
        );
    
        frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_folder_names', args:{
            'storage_type':frm.doc.storage_type
         },
         callback:function(r){
             console.log(r.message)
             frm.set_df_property('folder', 'options', r.message);
             frm.refresh_field('folder');
         }
        });

    },
	on_load(frm) {
        //frm.disable_save();
        frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_folder_names', args:{
           'storage_type':frm.doc.storage_type
        },
        callback:function(r){
            console.log(r.message)
            frm.set_df_property('folder', 'options', r.message);
            frm.refresh_field('folder');
        }
       });

       frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_objects', args:{
            'storage_type':frm.doc.storage_type,
            'name':frm.doc.name1
       },
       callback:function(r){
           console.log(r.message)
       }
       })

	},

    after_save(frm) {
        //frm.disable_save();
        frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_folder_names', args:{
           'storage_type':frm.doc.storage_type
        },
        callback:function(r){
            console.log(r.message)
            frm.set_df_property('folder', 'options', r.message);
            frm.refresh_field('folder');
        }
       });

       frappe.call({method:'datamanagement.data_management.doctype.data_folder.data_folder.fetch_objects', args:{
            'storage_type':frm.doc.storage_type,
            'name':frm.doc.name1
       },
       callback:function(r){
           console.log(r.message)
       }
       })

	},


    
});
