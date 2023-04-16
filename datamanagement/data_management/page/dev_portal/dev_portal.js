frappe.pages['dev-portal'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Dev Portal',
		single_column: true
	});

	var airflow_url='';
	var thisPage='';
	frappe.call({method:'datamanagement.data_management.services.services.get_airflow_url', args:{
		
		},
		callback:function(r){
			airflow_url=r.message;
			console.log("AIRFLOW URL="+airflow_url);
			
			
			thisPage='<div class="h-100 d-flex align-items-center justify-content-center">\
			<!--[if IE]><object classid="clsid:25336920-03F9-11CF-8FD0-00AA00686F13" data="'+airflow_url+'">\
			<p>backup content</p>\
			</object>\
			<![endif]-->\
			<!--[if !IE]> <-->\
			<object type="text/html" data="'+airflow_url+'" style="width:100%; height:768px">\
			<p>backup content</p>\
			</object>\
			<!--> <![endif]-->\
			</div>';
			renderPage(thisPage);

		}
		});

	function renderPage(thisPage){
		this.main_section = page.wrapper.find(".layout-main-section");
		console.log("PAGE="+thisPage);
		this.main_section.append(thisPage);
	}
}

