// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Mapping", {
	metadata(frm) {
        console.log("REFRESH")

        frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_values', args:{
            'metadata':frm.doc.metadata,
            'name':frm.doc.name
        },
        callback:function(r){
            console.log(r.message)
            const obj = r.message
            frm.set_value('description',obj.description);
            frm.set_value('source',obj.source);
            frm.set_value('fields',obj.fields);
            frm.set_value('url',obj.url);
            frm.set_value('storage_type',obj.storage_type);
            frm.set_value('creation_date',obj.creation_date);
            frm.set_value('retention_period_units',obj.retention_period_units);
            frm.set_value('retention_period_value',obj.retention_period_value);
        }
    });

	},
    onload(frm) {
        console.log("REFRESH")
        if (frm.doc.metadata.length() > 0){
            frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_values', args:{
                'metadata':frm.doc.metadata,
                'name':frm.doc.name
            },
            callback:function(r){
                console.log(r.message)
                const obj = r.message
                frm.set_value('description',obj.description);
                frm.set_value('source',obj.source);
                frm.set_value('fields',obj.fields);
                frm.set_value('url',obj.url);
                frm.set_value('storage_type',obj.storage_type);
                frm.set_value('creation_date',obj.creation_date);
                frm.set_value('retention_period_units',obj.retention_period_units);
                frm.set_value('retention_period_value',obj.retention_period_value);
            }
        });
     }
	},
});
