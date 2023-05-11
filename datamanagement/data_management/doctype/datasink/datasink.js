// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt


frappe.ui.form.on("DataSink", {
	refresh(frm) {

        if (frm.doc.connection_type == 'DIRECT_DB'){
            frm.set_df_property('ssh_tunnel_host','hidden',true)
            frm.set_df_property('ssh_tunnel_port','hidden',true)
            frm.set_df_property('ssh_tunnel_login','hidden',true)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',true)
            frm.set_df_property('remote_destination_port','hidden',true)

            frm.set_df_property('ssh_tunnel_host','reqd',false)
            frm.set_df_property('ssh_tunnel_port','reqd',false)
            frm.set_df_property('ssh_tunnel_login','reqd',false)
            frm.set_df_property('ssh_tunnel_password','reqd',false)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',false)
            frm.set_df_property('local_port','reqd',false)
            frm.set_df_property('remote_destination_port','reqd',false)

        }

        else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORD'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',false)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)


            frm.set_df_property('ssh_tunnel_host','reqd',true)
            frm.set_df_property('ssh_tunnel_port','reqd',true)
            frm.set_df_property('ssh_tunnel_login','reqd',true)
            frm.set_df_property('ssh_tunnel_password','reqd',true)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',false)
            frm.set_df_property('local_port','reqd',true)
            frm.set_df_property('remote_destination_port','reqd',true)

        }
        
        else if (frm.doc.connection_type == 'SSH_TUNNEL_PEM'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',false)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)

            frm.set_df_property('ssh_tunnel_host','reqd',true)
            frm.set_df_property('ssh_tunnel_port','reqd',true)
            frm.set_df_property('ssh_tunnel_login','reqd',true)
            frm.set_df_property('ssh_tunnel_password','reqd',false)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',true)
            frm.set_df_property('local_port','reqd',true)
            frm.set_df_property('remote_destination_port','reqd',true)


        }

        else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORDLESS'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)

            frm.set_df_property('ssh_tunnel_host','reqd',true)
            frm.set_df_property('ssh_tunnel_port','reqd',true)
            frm.set_df_property('ssh_tunnel_login','reqd',true)
            frm.set_df_property('ssh_tunnel_password','reqd',false)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',false)
            frm.set_df_property('local_port','reqd',true)
            frm.set_df_property('remote_destination_port','reqd',true)
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

            frm.set_df_property('ssh_tunnel_host','reqd',false)
            frm.set_df_property('ssh_tunnel_port','reqd',false)
            frm.set_df_property('ssh_tunnel_login','reqd',false)
            frm.set_df_property('ssh_tunnel_password','reqd',false)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',false)
            frm.set_df_property('local_port','reqd',false)
            frm.set_df_property('remote_destination_port','reqd',false)

        }

        else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORD'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',false)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)


            frm.set_df_property('ssh_tunnel_host','reqd',true)
            frm.set_df_property('ssh_tunnel_port','reqd',true)
            frm.set_df_property('ssh_tunnel_login','reqd',true)
            frm.set_df_property('ssh_tunnel_password','reqd',true)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',false)
            frm.set_df_property('local_port','reqd',true)
            frm.set_df_property('remote_destination_port','reqd',true)

        }
        
        else if (frm.doc.connection_type == 'SSH_TUNNEL_PEM'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',false)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)

            frm.set_df_property('ssh_tunnel_host','reqd',true)
            frm.set_df_property('ssh_tunnel_port','reqd',true)
            frm.set_df_property('ssh_tunnel_login','reqd',true)
            frm.set_df_property('ssh_tunnel_password','reqd',false)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',true)
            frm.set_df_property('local_port','reqd',true)
            frm.set_df_property('remote_destination_port','reqd',true)


        }

        else if (frm.doc.connection_type == 'SSH_TUNNEL_PASSWORDLESS'){
            frm.set_df_property('ssh_tunnel_host','hidden',false)
            frm.set_df_property('ssh_tunnel_port','hidden',false)
            frm.set_df_property('ssh_tunnel_login','hidden',false)
            frm.set_df_property('ssh_tunnel_password','hidden',true)
            frm.set_df_property('ssh_tunnel_pem_path','hidden',true)
            frm.set_df_property('local_port','hidden',false)
            frm.set_df_property('remote_destination_port','hidden',false)

            frm.set_df_property('ssh_tunnel_host','reqd',true)
            frm.set_df_property('ssh_tunnel_port','reqd',true)
            frm.set_df_property('ssh_tunnel_login','reqd',true)
            frm.set_df_property('ssh_tunnel_password','reqd',false)
            frm.set_df_property('ssh_tunnel_pem_path','reqd',false)
            frm.set_df_property('local_port','reqd',true)
            frm.set_df_property('remote_destination_port','reqd',true)
        }
    },
});
