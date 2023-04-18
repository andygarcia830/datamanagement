// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Data Mapping", {

   refresh:function(frm,cdt,cdn) {
    frm.set_query("field_transformations",  function(frm,cdt,cdn) {
        var d = locals[cdt][cdn];
        //console.log("D="+d);
         
        return {
            filters:[
                ['Transformation', 'transformation', '=',d.transformation]
            ]
        }
    });
        
      

        
       // console.log("QUERY="+frm.fields_dict['field_transformations'].grid.get_field('transformation').get_query);

        },


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
    // field_transformations_add(frm,cdt,cdn) {
    //     frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_fields', args:{
    //         'metadata':frm.doc.metadata,
    //         'name':frm.doc.name
    //     },
    //     callback:function(r){
    //         console.log(r.message)
    //         //console.log('ADDING FIELD '+cdt+" "+cdn);
    //         //console.log('ADDING FIELD '+frm.fields);
    //         //frm.set_df_property('md_field', 'options', r.message);   
            
    //         var df = frappe.meta.get_docfield('FieldTransformation','md_field', frm.doc.name);
    //         frm.refresh();
    //         df.options=r.message;

    //         // let item = locals[cdt][cdn]; 
    //         // item.md_field='TEST'

    //         frm.refresh_field('field_transformations');

      
    //     }
        
    // });
    // },

   form_render:function(cfrm,cdt,cdn) {
        var df = frappe.meta.get_docfield('FieldTransformation','md_field', cfrm.doc.name);
        let item = locals[cdt][cdn]; 
        console.log("LOCALS="+Object.getOwnPropertyNames(item));
        console.log("Doctype="+Object.keys(cfrm.fields_dict.field_transformations));
        frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_fields', args:{
            'metadata':cfrm.doc.metadata,
            'name':cfrm.doc.name
        },
        callback:function(r){
            console.log(r.message)
            console.log('ADDING FIELD '+cfrm+" "+cdt+" "+cdn);
            //console.log('ADDING FIELD '+frm.fields);
            //frm.set_df_property('md_field', 'options', r.message);   
            //var df = frappe.meta.get_docfield('FieldTransformation','md_field', cfrm.doc.name);
            df.options=r.message;
            // df.value='TEST'
            console.log("df.value="+Object.getOwnPropertyNames(df));
            console.log("df.value="+df.options);
    

            // let item = locals[cdt][cdn]; 
            // console.log("ITEM="+Object.keys(item));
            // console.log("ITEM="+item.field);
            //cfrm.reload_doc();

       

      
        }
        
    });

    frappe.call({method:'datamanagement.data_management.doctype.data_mapping.data_mapping.fetch_origin_fields', args:{
        'sources':cfrm.doc.source,
    },
    callback:function(r){
        console.log("SOURCE1 = "+cfrm.doc.source_field_1)
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_1', cfrm.doc.name);
        df.options=r.message;
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_2', cfrm.doc.name);
        df.options=r.message;
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_3', cfrm.doc.name);
        df.options=r.message;
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_4', cfrm.doc.name);
        df.options=r.message;
       
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_5', cfrm.doc.name);
        df.options=r.message;
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_6', cfrm.doc.name);
        df.options=r.message;
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_7', cfrm.doc.name);
        df.options=r.message;
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_8', cfrm.doc.name);
        df.options=r.message;
        
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_9', cfrm.doc.name);
        df.options=r.message;
        var df = frappe.meta.get_docfield('FieldTransformation','source_field_10', cfrm.doc.name);
        df.options=r.message;

    }
    
    });
    
    },


    transformation(frm,cdt,cdn){
       
        frappe.model.set_value(cdt,cdn,"last_update_date",frappe.datetime.nowdate());
        //console.log("CHANGED FIELD TRANSFORMATION " +frm.last_update_date+" "+frappe.datetime.nowdate())
        frm.refresh_field('last_update_date');
        
    },
    md_field(frm,cdt,cdn){
       
        frappe.model.set_value(cdt,cdn,"last_update_date",frappe.datetime.nowdate());
        //console.log("CHANGED FIELD TRANSFORMATION " +frm.last_update_date+" "+frappe.datetime.nowdate())
        frm.refresh_field('last_update_date');
        
    }



});