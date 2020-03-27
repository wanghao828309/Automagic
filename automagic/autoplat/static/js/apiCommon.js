function add_param(){
    	var html='<tr class="params_p" cnt="4">\
								<td>\
									<input class="params_name input-text" type="text" name="p_name_4" title="参数名称" alt="参数名称" value="" maxlength="100">\
								</td>\
								<td>\
									<input class="params_value input-text" type="text" name="p_value_4" title="参数数值" alt="参数数值" value="" maxlength="5000">\
									<button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
								</td>\
							</tr>'
    	$("#params_table>tbody:last").append(html);
    }

function add_header(){
    	var html='<tr class="params_p" cnt="4">\
								<td>\
									<input class="params_name input-text" type="text" name="p_name_4" title="header名称" alt="header名称" value="" maxlength="100">\
								</td>\
								<td>\
									<input class="params_value input-text" type="text" name="p_value_4" title="header数值" alt="header数值" value="" maxlength="5000">\
									<button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
								</td>\
							</tr>'
    	$("#headers_table>tbody:last").append(html);
    }

function del_param(delBtn){
   		$(delBtn).parent().parent().remove();
}

function IsURL(str_url){
    var strRegex =/(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/;
    var re=new RegExp(strRegex);
    if (re.test(str_url)){
        return (true);
    }else{
        return (false);
    }
}

function getUrlParam(name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);
            if (r != null) return unescape(r[2]); return null;
}


function validateAPI(){
   		if($("#selapiproductid").val()== ""){
   			$("#selapiproductid").focus();
   			$("#selapiproductid").css("background-color","#FFFFCC");
   			toastr.error('项目必填');
   			return false;
   		}

   		if($("#selapimoduleid").val()== ""){
   			$("#selapimoduleid").focus();
   			$("#selapimoduleid").css("background-color","#FFFFCC");
   			toastr.error('模块必填');
   			return false;
   		}

   		if($("#apiInfoname").val() == ""){
   			$("#apiInfoname").focus();
   			$("#apiInfoname").css("background-color","#FFFFCC");
   			toastr.error('api名称必填');
   			return false;
   		}

        var httpReg=new RegExp("^"+"http://");
        var httpsReg=new RegExp("^"+"https://");

   		if($("#http_url_input").val() == "" || ! IsURL($("#http_url_input").val()) | (!httpReg.test($("#http_url_input").val()) & !httpsReg.test($("#http_url_input").val())) ) {
   			$("#http_url_input").focus();
   			$("#http_url_input").css("background-color","#FFFFCC");
   			toastr.error('url未填写或url格式不符合，参考http://www.baidu.com');
   			return false;
   		}

   		if($("#contentType").find('input[type=checkbox]:checked').length == 0 ){
   			$("#contentType").focus();
   			$("#contentType").css("background-color","#FFFFCC");
   			toastr.error('请求数据格式必填，请选择一个');
   			return false;
   		}
   		return true;
   }

   $(function(){

	$.ajax({
		type: "GET",
		data: {},
		url: "/api/webinterface/env/listall",
		cache: false,
		dataType: 'json',
		async: false,
		success: function (result, TextStatus) {
			result=result.results;
			//元素管理元素添加项目选择
			var envItem=$("#apiEnv");
			envItem.empty();
			envItem.append('<option value="">选择运行环境</option>')
			if (result.length > 0) {
				for (i = 0; i < result.length; i++) {
					envItem.append('<option value="' + result[i].env_name + '">' + result[i].env_name + '</option>');
				}
			}
		 }
	 });
	 
	 

	 $("#http_test").on("click",function(){
		validateAPI();
		if($("#apiEnv").val()== ""){
			$("#apiEnv").focus();
			$("#apiEnv").css("background-color","#FFFFCC");
			toastr.error('请先选择一个运行的环境');
			return false;
		}

		let env_name=$("#apiEnv").val();
		var request={};
		var headers=[];
		var request_data=[];
		var type=$("#contentType").find('input[type=checkbox]:checked').val();  
		if(type == "raw"){
			 cType="application/json;charset=utf-8;"
		 }
		if(type =="x-www-form-urlencoded" | type =="form-data" ) {
			 cType="application/"+type+";charset=utf-8;"
		 }
		headers.push({"key":"Content-Type","value":cType});
 
		$('#headers_table').find('tbody tr').each(function(i){
				key=$(this).children().children(".params_name").val();
				value=$(this).children().children(".params_value").val();
				if(key!= "" & value != ""){
					headers.push({"key":key,"value":value});
			   }
		});
 
		
		if(type =="x-www-form-urlencoded" | type =="form-data" ) {
			 $('#params_table').find('tbody tr').each(function(i){
 
				 key=$(this).children().children(".params_name").val();
					value=$(this).children().children(".params_value").val();
					if(key!= "" & value != ""){
					request_data.push({"key":key,"value":value});
				   }
				});
			 type="data";//置为data
			 
			}
		 
		if (type == "raw"){
			 type="json";//置为json
			 request_data=$("#param_json_val").val().replace(/[\r\n]/g,"");
		 }
 
		if(type == "binary"){
			 return false;//file类型暂时不支持
		 }
 
		   request.url=$("#http_url_input").val();
		   request.method=$("#api_method").val();
		   request.headers=headers;
		   request.type=type;
		   request.request_data=request_data;
		   request.env_name=env_name;
		  
		   request=JSON.stringify(request);
		 console.log(request);
 
		 $.ajax({
			 type: "POST",
			 data: request,
			 url: "/api/webinterface/api/debug",
			 cache: false,
			 dataType: 'json',
			 contentType: "application/json; charset=utf-8",
			 async: false,
			 success: function (result, TextStatus) {
//				 result=result;
                 if(result.hasOwnProperty("msg")){
                    toastr.error(result.msg);
                 }else if(result.hasOwnProperty("result") && result.result.success){
					 toastr.success("运行成功");
					 $("#resheaders").val(js_beautify(JSON.stringify(result.result.header),1,"    "));
					 $("#output").val(js_beautify(JSON.stringify(result.result.response),1,"    "));
				 }else{
					 toastr.error("运行失败");
					 $("#output").val(js_beautify(JSON.stringify(result.result.response),1,"    "));
				 }
 
			 },
			 error : function(msg) {
					 toastr.error(msg);
			 }
	 });
 
	
 
 
 

	 })

	  $('#contentType').find('input[type=checkbox]').bind('click', function(){  
		        var id = $(this).attr("id");
		        if(this.checked){
		            //除当前的checkbox其他的都不选中
		            $("#contentType").find('input[type=checkbox]').not(this).attr("checked", false);
		          	var typeVal=$(this).val();
			
					if(typeVal == "form-data" | typeVal == "x-www-form-urlencoded"  ){
						$("#params_table").show();
						$("#add_url_parameter").show();
						$("#params_json").hide();
						$("#params_file").hide();
					}
		
					if(typeVal == "raw"  ){
						$("#params_table").hide();
						$("#add_url_parameter").hide();
						$("#params_json").show();
						$("#params_file").hide();
					}
		
					if(typeVal == "binary"  ){
						$("#params_table").hide();
						$("#add_url_parameter").hide();
						$("#params_json").hide();
						$("#params_file").show();
					}
		          
		       
		        }else{
		        }
		    });
		
			$("#param_json_val").on("blur",function(){
				let val=$("#param_json_val").val();
				$("#param_json_val").val(js_beautify(val,1,"    "))
			})
		
		
		
		
			$('body').on('mouseenter' , 'tr' , function() {
				var delBtn=$(this).children().children(".tiny");
				delBtn.show();
			})
		
			 $('body').on('mouseleave' , 'tr' , function() {
				var delBtn=$(this).children().children(".tiny");
				delBtn.hide();
			})
   })

$(function loadAPI(){
    //   $.ajax({
    //         type: "GET",
    //         data: {'productid': ""},
    //         url: "/setting/get/project/",
    //         cache: false,
    //         dataType: 'json',
    //         async: false,
    //         success: function (result, TextStatus) {
    //             //元素管理元素添加项目选择
    //             var projectItem=$("#selapiproductid")
    //             projectItem.empty();
    //             projectItem.append('<option value="">所属项目</option>')
    //             if (result.length > 0) {
    //                 for (i = 0; i < result.length; i++) {
    //                     projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
    //                 }
    //             }

    //     }
    // })

     $("#selapiproductid").bind("change", function () {
        var s1SelectedVal = $('#selapiproductid').val();
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',
            async: false,
            success: function (result, TextStatus) {
                //元素管理元素添加项目选择
                var projectItem=$("#selapimoduleid")
                projectItem.empty();
                projectItem.append('<option value="">所属模块</option>')
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        projectItem.append('<option value="' + result[i].value + '">' + result[i].value + '</option>');
                    }
                }
        }
        })

    })


  //接口管理 编辑和添加页面 加载 选项框
  $.ajax({
    type: "GET",
    data: {},
    url: "/api/webinterface/api/" + getUrlParam("id"),
    cache: false,
    dataType: 'json',
    async: false,
    success: function (apiResult, TextStatus) {

      //$("#selapiproductid").find("option[text='"+apiResult.project+"']").attr("selected",true);
      $("#api-selproductid").find("option:contains('" + apiResult.product + "')").attr("selected", true);


      const s1SelectedVal = $('#api-selproductid').val()
      const projectItem = $('#selapiproductid')
      $.ajax({
        type: "GET",
        data: { 'productid': s1SelectedVal },
        url: "/setting/get/project/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
        cache: false,
        dataType: 'json',
        async: false,
        success: function (result, TextStatus) {
          let option_str = ''
          projectItem.empty();
          if (result.length > 0) {
           for (i = 0; i < result.length; i++) {
                option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
            }
          }else{
            option_str += '<option value="">'+"所属项目"+'</option>'
          }
          projectItem.append(option_str)

          $("#selapiproductid option").filter(function () { return $(this).text() == apiResult.project; }).prop("selected", true);
          $("#selapiproductid").trigger("change");
          $("#selapimoduleid").find("option:contains('" + apiResult.module + "')").attr("selected", true);
          $("#api_method").find("option:contains('" + apiResult.method + "')").attr("selected", true);

          $("#apiInfoname").val(apiResult.name);
          $("#http_url_input").val(apiResult.url);
          headers = apiResult.data.test.request.headers;


          $("#contentType").find('input[type=checkbox]').each(function (index, element) {
            var contenTypes = headers["Content-Type"];
            if (contenTypes.indexOf("json") != -1) {
              contenTypes = "raw";
            }
            if (contenTypes.indexOf(element.value) != -1) {
              //$(this).attr("checked", true);
              $(this).trigger("click");
            }
          })

          if (headers["Content-Type"].indexOf("json") != -1) {
            body = apiResult.data.test.request.json;
            body = JSON.stringify(body)
            if(body==='""'){
              body = ""
            }
            $("#param_json_val").val(js_beautify(body, 1, "    "));
          }//json

          if (headers["Content-Type"].indexOf("form") != -1) {
            body = apiResult.data.test.request.data;
            for (var param in body) {
              var html = '<tr class="params_p" cnt="4">\
								<td>\
									<input class="params_name input-text" type="text" name="p_name_4" title="参数名称" alt="参数名称" value="'+ String(param) + '" maxlength="100">\
								</td>\
								<td>\
									<input class="params_value input-text" type="text" name="p_value_4" title="参数数值" alt="参数数值" value="'+ String(body[param]) + '" maxlength="5000">\
									<button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
								</td>\
							</tr>';
              $("#params_table>tbody:last").append(html);

            }
          }//form

          //file 暂时不支持

          delete headers["Content-Type"];

          for (var head in headers) {
            console.log(typeof (head));
            var html = '<tr class="params_p" cnt="4">\
								<td>\
									<input class="params_name input-text" type="text" name="p_name_4" title="header名称" alt="header名称" value="'+ String(head) + '" maxlength="100">\
								</td>\
								<td>\
									<input class="params_value input-text" type="text" name="p_value_4" title="header数值" alt="header数值" value="'+ String(headers[head]) + '" maxlength="5000">\
									<button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
								</td>\
							</tr>';
            $("#headers_table>tbody:last").append(html);
          }

        }
      });


      // $("#selapimoduleid").find("option:contains('" + result.module + "')").attr("selected", true);
      // $("#api_method").find("option:contains('" + result.method + "')").attr("selected", true);

      // $("#apiInfoname").val(result.name);
      // $("#http_url_input").val(result.url);
      // headers = result.data.test.request.headers;


      // $("#contentType").find('input[type=checkbox]').each(function (index, element) {
      //   var contenTypes = headers["Content-Type"];
      //   if (contenTypes.indexOf("json") != -1) {
      //     contenTypes = "raw";
      //   }
      //   if (contenTypes.indexOf(element.value) != -1) {
      //     //$(this).attr("checked", true);
      //     $(this).trigger("click");
      //   }
      // })

      // if (headers["Content-Type"].indexOf("json") != -1) {
      //   body = result.data.test.request.json;
      //   $("#param_json_val").val(js_beautify(body, 1, "    "));
      // }//json

      // if (headers["Content-Type"].indexOf("form") != -1) {
      //   body = result.data.test.request.data;
      //   for (var param in body) {
      //     var html = '<tr class="params_p" cnt="4">\
			// 					<td>\
			// 						<input class="params_name input-text" type="text" name="p_name_4" title="参数名称" alt="参数名称" value="'+ String(param) + '" maxlength="100">\
			// 					</td>\
			// 					<td>\
			// 						<input class="params_value input-text" type="text" name="p_value_4" title="参数数值" alt="参数数值" value="'+ String(body[param]) + '" maxlength="5000">\
			// 						<button class="button danger tiny" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
			// 					</td>\
			// 				</tr>';
      //     $("#params_table>tbody:last").append(html);

      //   }
      // }//form

      // //file 暂时不支持

      // delete headers["Content-Type"];

      // for (var head in headers) {
      //   console.log(typeof (head));
      //   var html = '<tr class="params_p" cnt="4">\
			// 					<td>\
			// 						<input class="params_name input-text" type="text" name="p_name_4" title="header名称" alt="header名称" value="'+ String(head) + '" maxlength="100">\
			// 					</td>\
			// 					<td>\
			// 						<input class="params_value input-text" type="text" name="p_value_4" title="header数值" alt="header数值" value="'+ String(headers[head]) + '" maxlength="5000">\
			// 						<button class="button danger tiny" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
			// 					</td>\
			// 				</tr>';
      //   $("#headers_table>tbody:last").append(html);
      // }




    }, function(msg) {
      toastr.error("获取api信息失败:" + result.msg);
    }
  })

})



