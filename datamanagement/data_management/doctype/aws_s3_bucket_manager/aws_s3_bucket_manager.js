// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("AWS S3 Bucket Manager", {

    on_load(frm){
        frm.disable_save()
        frm.fields_dict['buckets'].grid.wrapper.find('.grid-remove-rows').hide();
        console.log("GRID WRAPPER="+frm.fields_dict['buckets'].grid.wrapper.keys)
        frappe.call({method:'datamanagement.data_management.doctype.aws_s3_bucket_manager.aws_s3_bucket_manager.fetch_buckets', args:{
           
        },
        callback:function(r){
            console.log(r.message)
        }
       })

    },


   refresh(frm) {
    frm.disable_save();
    frm.fields_dict['buckets'].grid.wrapper.find('.edit-row').hide();
    var keys = Object.keys(frm.fields_dict['buckets'].grid.wrapper);
        for (var key in frm.fields_dict['buckets'].grid.wrapper){
            console.log("GRID WRAPPER="+key)
        }
    frm.add_custom_button(
        __('Reload Buckets'),function(){
        frappe.call({method:'datamanagement.data_management.doctype.aws_s3_bucket_manager.aws_s3_bucket_manager.fetch_buckets', args:{
        
        },
        callback:function(r){
            console.log(r.message)
            frm.doc.reload_doc()
        }
       })
    }
    ,__('Actions')
    );
    frm.add_custom_button(
        __('Create Bucket'),function(){
            frappe.prompt(__('Enter Bucket Name'),({value})=> 
                frappe.call({method:'datamanagement.data_management.doctype.aws_s3_bucket_manager.aws_s3_bucket_manager.create_bucket', args:{
                    'bucket':value
                },
                callback:function(r){
                    frm.doc.reload_doc()
                }
                })
                );
           
           
        }
    ,__('Actions')
    );

    frm.add_custom_button(
        __('Delete Bucket'),function(){
            frappe.prompt(__('Enter Bucket Name To Delete'),({value})=>
                frappe.confirm('Are you sure you want to delete bucket '+value+"?",
                // YES
                ()=>{
                    frappe.call({method:'datamanagement.data_management.doctype.aws_s3_bucket_manager.aws_s3_bucket_manager.delete_bucket', args:{
                            'bucket':value
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
 },

 
});
