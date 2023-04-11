
frappe.ui.form.on("Field Transformation", {
    form_render: function(frm,cdt,cdn) {
        console.log('ADDING FIELD')
        frm.set_df_property('field', 'options', ['test','test2']);
    }



});