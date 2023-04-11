// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Mapping", {

    // refresh(frm) {
    //     console.log("REFRESH")
    //     if (frm.doc.metadata.length() > 0){
    //         frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_values', args:{
    //             'metadata':frm.doc.metadata,
    //             'name':frm.doc.name
    //         },
    //         callback:function(r){
    //             console.log(r.message)
    //             const obj = r.message
    //             frm.set_value('description',obj.description);
    //             frm.set_value('source',obj.source);
    //             frm.set_value('fields',obj.fields);
    //             frm.set_value('url',obj.url);
    //             frm.set_value('storage_type',obj.storage_type);
    //             frm.set_value('creation_date',obj.creation_date);
    //             frm.set_value('retention_period_units',obj.retention_period_units);
    //             frm.set_value('retention_period_value',obj.retention_period_value);
                
    //         }
    //     });
    //  };

    // frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_fieldsasd', args:{
    //         'metadata':frm.doc.metadata,
    //         'name':frm.doc.name
    //     },
    //     callback:function(r){
    //         console.log(r.message)
    //         // const obj = r.message
    //         // frm.set_value('description',obj.description);
    //         // frm.set_value('source',obj.source);
    //         // frm.set_value('fields',obj.fields);
    //         // frm.set_value('url',obj.url);
    //         // frm.set_value('storage_type',obj.storage_type);
    //         // frm.set_value('creation_date',obj.creation_date);
    //         // frm.set_value('retention_period_units',obj.retention_period_units);
    //         // frm.set_value('retention_period_value',obj.retention_period_value);
    //         // frm.doc.reload()
    //     }
    // });

     
	// },
    // field_transformations(frm, cdt, cdn) {
    //     console.log("adding field")
    //     frm.set_df_property('field', 'options', ['test','test2']);
    // },


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

    frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_fields', args:{
        'metadata':frm.doc.metadata,
        'name':frm.doc.name
    },
    callback:function(r){
        console.log(r.message)
        
    }
}); 

    

	},

});



frappe.ui.form.on("FieldTransformation", {
    form_render: function(frm,cdt,cdn) {
        frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_fields', args:{
            'metadata':frm.doc.metadata,
            'name':frm.doc.name
        },
        callback:function(r){
            //console.log(r.message)
            //console.log('ADDING FIELD '+cdt+" "+cdn);
            //console.log('ADDING FIELD '+frm.fields);
            //frm.set_df_property('md_field', 'options', r.message);   
            let df = frappe.meta.get_docfield('FieldTransformation','md_field', frm.doc.name);
            df.options=r.message;
            refresh_field('md_field');
      
        }
        
    });
}



});