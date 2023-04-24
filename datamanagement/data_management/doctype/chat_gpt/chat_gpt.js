// Copyright (c) 2023, Andy Garcia and contributors
// For license information, please see license.txt

frappe.ui.form.on("Chat GPT", {
   
	refresh(frm) {
        frm.disable_save();

        if (frm.doc.gpt_context != null && frm.doc.gpt_context != ''){
            frm.add_custom_button(
                __('Re-train GPT'),function(){
                    frappe.confirm(__('Train Data?'),()=> {
                        frm.doc.display="<div style=\"display: flex; justify-content: flex-center;\"><p class=\"alert-info\" style=\"width: 100%;\">"+
                        "Training Data..."+
                        "</p></div>"+
                        "<div class=\"d-flex justify-content-center\">"+
                        "<div class=\"spinner-border text-primary\" role=\"status\">"+
                        "</div>"+
                        "</div>";
                        frm.set_df_property('display','options',frm.doc.display);
                        frappe.call({method:'datamanagement.data_management.doctype.chat_gpt.chat_gpt.train_chatbot', args:{
                            'context':frm.doc.gpt_context
                        },
                        callback:function(r){
                            frm.doc.display="</div></div>";
                            frm.doc.json=[];
                            frm.set_df_property('display','options',frm.doc.display);
                            frappe.msgprint("Training Done!");
                            show_greeting();
                        }
                        })},
                        ()=>{}
                        );
                
                
                }
            ,__('Actions')
            );

            frm.add_custom_button(
                __('Clear Chat'),function(){
                    show_greeting();
                }
            ,__('Actions')
            );
        }
       function show_greeting(){
            frappe.call({method:'datamanagement.data_management.doctype.chat_gpt.chat_gpt.fetch_greeting', args:{
                'context':frm.doc.gpt_context
            },
            callback:function(r){
                var result="<div></div>"
                if (r.message != null && r.message != ''){
                    result+="<div style=\"display: flex; justify-content: flex-start;\"><p class=\"alert-primary\" style=\"width: 98%;\">"+
                    r.message+
                    "</p></div>"
                }
                frm.doc.display=result;
                frm.doc.json=[];
                frm.set_df_property('display','options',frm.doc.display);
                console.log("Cleared Chat");
            }
            });

       };

       if(frm.doc.gpt_context != null && frm.doc.gpt_context != '') show_greeting();
       else frm.set_df_property('send','hidden',true);
	},

    gpt_context(frm){
        console.log("GPT CONTEXT="+frm.doc.gpt_context);
        if (frm.doc.gpt_context != null && frm.doc.gpt_context != ''){
            frm.add_custom_button(
                __('Re-train GPT'),function(){
                    frappe.confirm(__('Train Data?'),()=> {
                        frm.doc.display="<div style=\"display: flex; justify-content: flex-center;\"><p class=\"alert-info\" style=\"width: 100%;\">"+
                        "Training Data..."+
                        "</p></div>"+
                        "<div class=\"d-flex justify-content-center\">"+
                        "<div class=\"spinner-border text-primary\" role=\"status\">"+
                        "</div>"+
                        "</div>";
                        frm.set_df_property('display','options',frm.doc.display);
                        frappe.call({method:'datamanagement.data_management.doctype.chat_gpt.chat_gpt.train_chatbot', args:{
                            'context':frm.doc.gpt_context
                        },
                        callback:function(r){
                            frm.doc.display="</div></div>";
                            frm.doc.json=[];
                            frm.set_df_property('display','options',frm.doc.display);
                            frappe.msgprint("Training Done!");
                            show_greeting();
                        }
                        })},
                        ()=>{}
                        );
                
                
                }
            ,__('Actions')
            );

            frm.add_custom_button(
                __('Clear Chat'),function(){
                    show_greeting();
                }
            ,__('Actions')
            );
            show_greeting();
        }
       

        function show_greeting(){
            frappe.call({method:'datamanagement.data_management.doctype.chat_gpt.chat_gpt.fetch_greeting', args:{
                'context':frm.doc.gpt_context
            },
            callback:function(r){
                var result="<div></div>"
                if (r.message != null && r.message != ''){
                    result+="<div style=\"display: flex; justify-content: flex-start;\"><p class=\"alert-primary\" style=\"width: 98%;\">"+
                    r.message+
                    "</p></div>"
                }
                frm.doc.display=result;
                frm.doc.json=[];
                frm.set_df_property('display','options',frm.doc.display);
                frm.set_df_property('send','hidden',false);
            }
            });

       };

    },

    send(frm){
        console.log("Send Pressed")
        if (frm.doc.input !=null && frm.doc.input !=''){
            if (frm.doc.json==null)frm.doc.json=[];
            if (frm.doc.display == null ) frm.doc.display='';
            var input=frm.doc.input;
            frm.doc.display+="<div style=\"display: flex; justify-content: flex-end;\"><p class=\"alert-info\" style=\"width: 98%;\">"+
                    input+
                    "</p></div>"+
                    "<div class=\"d-flex justify-content-center\">"+
                    "<div class=\"spinner-border text-primary\" role=\"status\">"+
                    "</div>"+
                    "</div>"

            frm.set_df_property('display','options',frm.doc.display);
            frm.doc.input=null
            frm.refresh_field("input")


            // frappe.call({method:'datamanagement.data_management.doctype.chat_gpt.chat_gpt.send', args:{
            //     'msg':frm.doc.input,
            //     'jsonStr':frm.doc.json
            // },

            frappe.call({method:'datamanagement.data_management.doctype.chat_gpt.chat_gpt.ask_question', args:{
                'msg':input,
                'jsonStr':frm.doc.json,
                'context':frm.doc.gpt_context
            },
            callback:function(r){
                frm.doc.json=r.message
                frm.doc.display=format_json(r.message)
                frm.set_df_property('display','options',frm.doc.display);
               
                //frm.refresh_field("display")
                console.log(frm.doc.display)
            }
            })
        }

        function format_json(json){
            var result=""
            for (var i=0; i < json.length; i ++) {

                if(json[i][0] != null){
                    result+="<div style=\"display: flex; justify-content: flex-end;\"><p class=\"alert-info\" style=\"width: 98%;\">"+
                    json[i][0]+
                    "</p></div>"
                }

                if(json[i][1] != null){
                    var output=json[i][1].replaceAll('\n','<br>');
                    
                    console.log(output);
                    result+="<div style=\"display: flex; justify-content: flex-start;\"><p class=\"alert-primary\" style=\"width: 98%;\">"+
                    output+
                    "</p></div>"
                }

            }

            return result

        }
    },


});
