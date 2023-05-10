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
            };

            if (frm.doc.connection_type == 'DIRECT_DB'){
                frm.set_df_property('ssh_tunnel_host','hidden',true)
                frm.set_df_property('ssh_tunnel_port','hidden',true)
                frm.set_df_property('ssh_tunnel_login','hidden',true)
                frm.set_df_property('ssh_tunnel_password','hidden',true)
                frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
                frm.set_df_property('local_port','hidden',true)
                frm.set_df_property('remote_destination_port','hidden',true)
    
            }
    
            else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORD'){
                frm.set_df_property('ssh_tunnel_host','hidden',false)
                frm.set_df_property('ssh_tunnel_port','hidden',false)
                frm.set_df_property('ssh_tunnel_login','hidden',false)
                frm.set_df_property('ssh_tunnel_password','hidden',false)
                frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
                frm.set_df_property('local_port','hidden',false)
                frm.set_df_property('remote_destination_port','hidden',false)
    
            }
            
            else if (frm.doc.connection_type == 'SSH_TUNNEL_PEM'){
                frm.set_df_property('ssh_tunnel_host','hidden',false)
                frm.set_df_property('ssh_tunnel_port','hidden',false)
                frm.set_df_property('ssh_tunnel_login','hidden',false)
                frm.set_df_property('ssh_tunnel_password','hidden',true)
                frm.set_df_property('ssh_tunnel_pem_path','hidden',false)
                frm.set_df_property('local_port','hidden',false)
                frm.set_df_property('remote_destination_port','hidden',false)
    
            }
    
            else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORDLESS'){
                frm.set_df_property('ssh_tunnel_host','hidden',false)
                frm.set_df_property('ssh_tunnel_port','hidden',false)
                frm.set_df_property('ssh_tunnel_login','hidden',false)
                frm.set_df_property('ssh_tunnel_password','hidden',true)
                frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
                frm.set_df_property('local_port','hidden',false)
                frm.set_df_property('remote_destination_port','hidden',false)
            }
	},

    connection_type(frm){
        if (frm.doc.connection_type == 'DIRECT_DB'){
            frm.set_df_property('ssh_tunnel_host','hidden',true)
            frm.set_df_property('ssh_tunnel_port','hidden',true)
            frm.set_df_property('ssh_tunnel_login','hidden',true)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',true)
            frm.set_df_property('remote_destination_port','hidden',true)

        }

        else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORD'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',false)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)

        }
        
        else if (frm.doc.connection_type == 'SSH_TUNNEL_PEM'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',false)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)

        }

        else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORDLESS'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)
        }
    },
});
