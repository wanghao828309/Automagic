$(function loadProject(){
    // $.ajax({
    //     type: "GET",
    //     data: {'productid': ""},
    //     url: "/setting/get/project/",
    //     cache: false,
    //     dataType: 'json',
    //     async: false,
    //     success: function (result, TextStatus) {
    //         //元素管理元素添加项目选择
    //         var projectItem=$("#selapiproductid")
    //         projectItem.empty();
    //         projectItem.append('<option value="">所属项目</option>')
    //         if (result.length > 0) {
    //             for (i = 0; i < result.length; i++) {
    //                 projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
    //             }
    //         }

    //         var projectItem=$("#apicaseproductid")
    //         projectItem.empty();
    //         projectItem.append('<option value="">所属项目</option>')
    //         if (result.length > 0) {
    //             for (i = 0; i < result.length; i++) {
    //                 projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
    //             }
    //         }
    // }   



    //     });
    

    
        $("#selapiproductid").bind("change", function () {
            var s1SelectedVal = $('#selapiproductid').val();
            $.ajax({
                type: "GET",
                data: {'projectid': s1SelectedVal},
                url: "/setting/get/module/", 
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
        })})
    
        $("#apicaseproductid").bind("change", function () {
            var s1SelectedVal = $('#apicaseproductid').val();
            $.ajax({
                type: "GET",
                data: {'projectid': s1SelectedVal},
                url: "/setting/get/module/", 
                cache: false,
                dataType: 'json',
                async: false,
                success: function (result, TextStatus) {
                    //元素管理元素添加项目选择
                    var projectItem=$("#apicasemoduleid")
                    projectItem.empty();
                    projectItem.append('<option value="">所属模块</option>')
                    if (result.length > 0) {
                        for (i = 0; i < result.length; i++) {
                            projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                        }
                    }
            }
        })})
    }
)

function add_transfer_item(apiName,apiId,uuid){

    let html='<label class="transfer-panel-item" data-text="'+apiName+'" data-value="'+apiId+'">\
                   <span class="checkbox-input pull-left">\
                       <input type="checkbox" class="checkbox-inline" value="'+apiId+'">\
                   </span>\
                   <span class="checkbox-label pull-left">\
                       <span>'+apiName+'</span>\
                   </span>\
                   <span class="checkbox-label pull-left">\
                <span><a title="编辑" href="#" class="ke-ablock"  id="'+uuid+'" data-toggle="modal" data-target="#apicaseModal" onclick=\'loadApiCaseData(\"'+uuid+'\")\'><i class="glyphicon glyphicon-play-circle" style="margin-left: 8px;margin-top: 5px;"></i>edit</a></span>\
            </span>\
            </label>';
    $("#transfer-right-api").append(html);
}     
function getUrlParam(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
}
     
function generateUUID() {
                var d = new Date().getTime();
                var uuid = 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                  var r = (d + Math.random()*16)%16 | 0;
                  d = Math.floor(d/16);
                  return (c=='x' ? r : (r&0x3|0x8)).toString(16);
                });
                return uuid;
};

      function serachAPI(){

            //请求后台
        let data={};
        data.name=$("#apisearchstr").val();
        data.url=$("#apisearchstr").val();
        data.project=$("#apicaseproductid").val();
        data.module=$("#apicasemoduleid").val();
        data.page=1;
        data.size=100;//默认加载100个，这个足够了
        $.ajax({
            type: "GET",
            data: data,
            url: "/api/webinterface/api/list",
            cache: false,
            dataType: 'json',
            async: false,
            success: function (result, TextStatus) {
                //元素管理元素添加项目选择
                let caseItem=$("#transfer-left-api");
                caseItem.empty();
                result=result.results;
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        caseItem.append('<label class="transfer-panel-item" data-text="'+result[i].name+'" data-value="'+result[i].id+'" draggable="false">\
                                               <span class="checkbox-input pull-left">\
                                                      <input type="checkbox" class="checkbox-inline" value="1">\
                                               </span>\
                                                <span class="checkbox-label pull-left">\
                                                    <span>'+result[i].name+'</span>\
                                                    </span>\
                                            </label>');
                    }
                }


            }
        });


        }


        function add_param_value(key,value){
    	    var html='<tr class="params_p" cnt="1">\
                        <td>\
                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="'+key+'" maxlength="100">\
                        </td>\
                        <td>\
                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="'+value+'" maxlength="5000">\
                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                        </td>\
                    </tr>'
    	    $("#params_table>tbody:last").append(html);
        }
        
        function add_param(){
    	    var html='<tr class="params_p" cnt="1">\
                        <td>\
                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="" maxlength="100">\
                        </td>\
                        <td>\
                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="" maxlength="5000">\
                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                        </td>\
                    </tr>'
    	    $("#params_table>tbody:last").append(html);
        }

        function add_subparam(){
            var html='<tr class="params_p" cnt="1">\
                        <td>\
                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="" maxlength="100">\
                        </td>\
                        <td>\
                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="" maxlength="5000">\
                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                        </td>\
                    </tr>'
    	    $("#sub_params_table>tbody:last").append(html);
        }

        function add_sub_value(){
            var html='<tr class="params_p" cnt="1">\
                                                        <td>\
                                                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="" maxlength="100">\
                                                        </td>\
                                                        <td>\
                                                            <label>=</label>\
                                                        </td>\
                                                        <td>\
                                                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="" maxlength="5000">\
                                                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                                                        </td>\
                                                    </tr>'
    	    $("#sub_value_table>tbody:last").append(html);
        }

        function add_sub_check(){
    	    var html='   <tr class="params_p" cnt="1">\
                                                        <td>\
                                                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="" maxlength="100">\
                                                        </td>\
                                                        <td>\
                                                            <select class="itype" >\
                                                                    <option value="string" selected="">string</option>\
                                                                    <option value="int" >int</option>\
                                                                    <option value="float">float</option>\
                                                                    <option value="double">double</option>\
                                                                    <option value="boolean">boolean</option>\
                                                                </select>\
                                                            </td>\
                                                        <td>\
                                                                <select class="checktor" >\
                                                                        <option value="equals">equals</option>\
                                                                        <option value="contains">contains</option>\
                                                                        <option value="startswith">startswith</option>\
                                                                        <option value="endswith">endswith</option>\
                                                                        <option value="regex_match">regex_match</option>\
                                                                        <option value="type_match">type_match</option>\
                                                                        <option value="contained_by">contained_by</option>\
                                                                        <option value="less_than">less_than</option>\
                                                                        <option value="less_than_or_equals">less_than_or_equals</option>\
                                                                        <option value="greater_than">greater_than</option>\
                                                                        <option value="greater_than_or_equals">greater_than_or_equals</option>\
                                                                        <option value="not_equals">not_equals</option>\
                                                                        <option value="string_equals">string_equals</option>\
                                                                        <option value="length_equals">length_equals</option>\
                                                                        <option value="length_greater_than">length_greater_than</option>\
                                                                        <option value="length_greater_than_or_equals">length_greater_than_or_equals</option>\
                                                                        <option value="length_less_than">length_less_than</option>\
                                                                        <option value="equals">length_less_than_or_equals</option>\
                                                                    </select>\
                                                            </td>\
                                                        <td>\
                                                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="" maxlength="5000">\
                                                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                                                        </td>\
                                                    </tr>'
    	    $("#sub_check_table>tbody:last").append(html);
        }


    function del_param(delBtn){
   		$(delBtn).parent().parent().remove();
   }

    /*
     *加载case参数等
     *提升易用性
     */
    function loadApiCaseData(hiddenId){


        $("#apicaseModal").html('<input id="modal_link_id" type="text" style="display:none" hiddenId="'+String(hiddenId)+'">\
        <div class="modal-dialog">\
                <div class="modal-content" style="min-height:500px;height: auto;">\
                    <div class="modal-header">\
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                        <h4 class="modal-title" id="myModalLabel">接口参数</h4>\
                    </div>\
                    <ul id="myTab" class="nav nav-tabs">\
                            <li class="active">\
                                <a href="#home" data-toggle="tab">\
                                     接口参数\
                                </a>\
                            </li>\
                            <li><a href="#ios" data-toggle="tab">case变量赋值</a></li>\
                            <li><a href="#jmeter" data-toggle="tab">接口断言</a></li>\
                        </ul>\
                        <div id="myTabContent" class="tab-content">\
                            <div class="tab-pane fade in active" id="home">\
                                    <table id="sub_params_table" class="table table-bordered transfer-table">\
                                            <thead>\
                                                <tr>\
                                                    <th width="43%">接口参数名称</th>\
                                                    <!-- <th width="10%">Body参数类型</th> -->\
                                                    <th>接口参数值</th>\
                                                </tr>\
                                            </thead>\
                                            <tbody>\
                                            </tbody>\
                                        </table>\
                            </div>\
                            <div class="tab-pane fade" id="ios">\
                                    <table id="sub_value_table" class="table table-bordered transfer-table">\
                                            <thead>\
                                                <tr>\
                                                    <th width="43%">case参数名称</th>\
                                                     <th>等于</th>\
                                                    <th>参数取值</th>\
                                                </tr>\
                                            </thead>\
                                            <tbody>\
                                            </tbody>\
                                        </table>\
                                        <div id="controlltable">\
                                                <button class="btn  btn-primary " id="add_url_parameter" type="button" onclick="add_sub_value()" style="margin-left: 80;">添加</button>\
                                                <!--<button class="button success small" id="add_raw_url_parameter" type="button">RAW批量添加</button>-->\
                                        </div>\
                            </div>\
                            <div class="tab-pane fade" id="jmeter">\
                                    <table id="sub_check_table" class="table table-bordered transfer-table">\
                                            <thead>\
                                                <tr>\
                                                    <th width="30%">参数</th>\
                                                    <th width="15%">参数类型</th>\
                                                    <th width="20%">断言类型</th>\
                                                    <!-- <th width="10%">Body参数类型</th> -->\
                                                    <th>预期值</th>\
                                                </tr>\
                                            </thead>\
                                            <tbody>\
                                            </tbody>\
                                        </table>\
                                        <div id="controlltable">\
                                                <button class="btn  btn-primary " id="add_url_parameter" type="button" onclick="add_sub_check()" style="margin-left: 80;">添加</button>\
                                        </div>\
                            </div>\
                        </div>\
                        <div class="modal-footer diy-footer">\
                                <button type="button" id="modal_cancel" class="btn btn-default" data-dismiss="modal">取消</button>\
                                <button type="button" class="btn btn-primary" onclick="saveApicase()">保存</button>\
                        </div>\
                </div><!-- /.modal-content -->');


        if($("#"+hiddenId).data().hasOwnProperty("data")){
            let data=JSON.stringify($("#"+hiddenId).data());
            data= $.parseJSON (data);
            let params=data.data.params;
            let extract=data.data.extract;
            let asserts=data.data.asserts;
            for(var p in params){
                var html='<tr class="params_p" cnt="1">\
                        <td>\
                            <input class="p_name transfer-table-td-input" type="text" disabled="disabled" name="p_name_1" title="参数名称" alt="参数名称" value="'+String(params[p].key)+'" maxlength="100">\
                        </td>\
                        <td>\
                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="'+String(params[p].value)+'" maxlength="5000">\
                        </td>\
                    </tr>'
    	        $("#sub_params_table>tbody:last").append(html);
            }
            if(typeof(params)=='undefined'){
                //json类型
                pjson=data.data.pjson;
                if(pjson){
                  $("#sub_params_table").remove();
                  $("#home").empty()
                  $("#home").append('<div id="params_json" class="independSection">\
                        <textarea id="param_json_val" class="independSection"></textarea>\
                                  </div>');
                  pjson = JSON.stringify(pjson)
                      $("#param_json_val").val(js_beautify(pjson,1,"    "));
                }
            }

            for (var e in extract.test){
                var html='<tr class="params_p" cnt="1">\
                                                        <td>\
                                                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="'+String(extract.test[e].key)+'" maxlength="100">\
                                                        </td>\
                                                        <td>\
                                                            <label>=</label>\
                                                        </td>\
                                                        <td>\
                                                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="'+String(extract.test[e].value)+'" maxlength="5000">\
                                                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                                                        </td>\
                                                    </tr>'
    	        $("#sub_value_table>tbody:last").append(html);
            }
            for(var asser in asserts.test){
                let assertkey=asserts.test[asser].key;
                let assertType=asserts.test[asser].comparator;
                let itype=asserts.test[asser].type;
                let assertValue=asserts.test[asser].value;
                var html='   <tr class="params_p" cnt="1">\
                                                        <td>\
                                                            <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" alt="参数名称" value="'+String(assertkey)+'" maxlength="100">\
                                                        </td>\
                                                        <td>';
                var selectHtml='<select class="checktor" >\
                                                                        <option value="equals">equals</option>\
                                                                        <option value="contains">contains</option>\
                                                                        <option value="startswith">startswith</option>\
                                                                        <option value="endswith">endswith</option>\
                                                                        <option value="regex_match">regex_match</option>\
                                                                        <option value="type_match">type_match</option>\
                                                                        <option value="contained_by">contained_by</option>\
                                                                        <option value="less_than">less_than</option>\
                                                                        <option value="less_than_or_equals">less_than_or_equals</option>\
                                                                        <option value="greater_than">greater_than</option>\
                                                                        <option value="greater_than_or_equals">greater_than_or_equals</option>\
                                                                        <option value="not_equals">not_equals</option>\
                                                                        <option value="string_equals">string_equals</option>\
                                                                        <option value="length_equals">length_equals</option>\
                                                                        <option value="length_greater_than">length_greater_than</option>\
                                                                        <option value="length_greater_than_or_equals">length_greater_than_or_equals</option>\
                                                                        <option value="length_less_than">length_less_than</option>\
                                                                        <option value="equals">length_less_than_or_equals</option>\
                                                                    </select>';
                selectHtml=selectHtml.replace(assertType+'"',assertType+'" selected="true"');

                var selectHtmlType='<select class="itype" >\
										<option value="string" selected="">string</option>\
										<option value="int" >int</option>\
										<option value="float">float</option>\
										<option value="double">double</option>\
										<option value="boolean">boolean</option>\
                                    </select>';
                selectHtmlType=selectHtmlType.replace(itype+'"',itype+'" selected="true"');
                var tailHtml='</td>\
                                                        <td>\
                                                            <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="'+String(assertValue)+'" maxlength="5000">\
                                                            <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                                                        </td>\
                                                    </tr>';
                html=html+selectHtmlType+"</td><td>"+selectHtml+tailHtml;
    	        $("#sub_check_table>tbody:last").append(html);

            }
        }

        let apiId=$("#"+hiddenId).parent().parent().parent().attr("data-value");

      if(!$("#param_json_val").val()){
        $.ajax({
        type: "GET",
        data: {},
        url: "/api/webinterface/api/"+apiId,
        cache: false,
        dataType: 'json',
        async: false,
        success: function (result, TextStatus) {
            let pjson=result.data.test.request.json;
            let headers = result.data.test.request.headers
              if(typeof(pjson)!="undefined"){
                //数据类型为json
                $("#sub_params_table").remove();
                $("#home").html('<div id="params_json" class="independSection">\
                      <textarea id="param_json_val" class="independSection"></textarea>\
                                </div>');
                if(typeof pjson === 'string' && pjson===''){
                  pjson = {}
                }
                pjson = JSON.stringify(pjson)
                $("#param_json_val").val(js_beautify(pjson,1,"    "));
                $("#param_json_val").data('headers',headers)
              }

          }
        });
      }
      if($("#sub_params_table").find("tbody tr").length == 0){
          $.ajax({
          type: "GET",
          data: {},
          url: "/api/webinterface/api/"+apiId,
          cache: false,
          dataType: 'json',
          async: false,
          success: function (result, TextStatus) {
              let params=result.data.test.request.data;
              let headers = result.data.test.request.headers
              if(typeof(params)!="undefined"){
                  //数据类型为data

                  for(let key in params){
                      let value=params[key];
                      let html='<tr class="params_p" cnt="1">\
                      <td>\
                          <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" disabled="disabled" alt="参数名称" value="'+String(key)+'" maxlength="100">\
                      </td>\
                      <td>\
                          <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="'+String(value)+'" maxlength="5000">\
                          <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
                      </td>\
                      </tr>'
                    $("#sub_params_table>tbody:last").append(html);
                  }
                  $('#sub_params_table>tbody:last').data('headers',headers)
              }
            }
          });
      }


















        // if($("#sub_params_table").find("tbody tr").length == 0 | $("#param_json_val").val()==""){
        //     $.ajax({
        //     type: "GET",
        //     data: {},
        //     url: "/api/webinterface/api/"+apiId,
        //     cache: false,
        //     dataType: 'json',
        //     async: false,
        //     success: function (result, TextStatus) {
        //         let params=result.data.test.request.data;
        //         let pjson=result.data.test.request.json;
        //         if(typeof(params)!="undefined"){
        //             //数据类型为data

        //             for(let key in params){
        //                 let value=params[key];
        //                 let html='<tr class="params_p" cnt="1">\
        //                 <td>\
        //                     <input class="p_name transfer-table-td-input" type="text" name="p_name_1" title="参数名称" disabled="disabled" alt="参数名称" value="'+String(key)+'" maxlength="100">\
        //                 </td>\
        //                 <td>\
        //                     <input class="p_value transfer-table-td-input" type="text" name="p_value_1" title="参数数值" alt="参数数值" value="'+String(value)+'" maxlength="5000">\
        //                     <button class="button danger tiny else-btn" onclick="javascript:del_param(this);" type="button" style="display:none;">删除参数</button>\
        //                 </td>\
        //                 </tr>'
    	  //               $("#sub_params_table>tbody:last").append(html);
        //             }
        //         }
        //         if(typeof(pjson)!="undefined"){
        //             //数据类型为json
        //             $("#sub_params_table").remove();
        //             $("#home").html('<div id="params_json" class="independSection">\
				// 	                <textarea id="param_json_val" class="independSection"></textarea>\
        //                             </div>');
        //             pjson = JSON.stringify(pjson)
        //             $("#param_json_val").val(js_beautify(pjson,1,"    "));
        //         }

        //       }
        //     });
        // }
        
    }

    function saveApicase(){


        let data={};
        let params=[];
        let extract={};
        let asserts={};
        let test=[];
        $('#sub_params_table').find('tbody tr').each(function(i){
   			key=$(this).children().children(".p_name").val();
   			value=$(this).children().children(".p_value").val();
            if(key!= "" & value != ""){
                params.push({"key":key,"value":value});
      		}
        });

        $('#sub_value_table').find('tbody tr').each(function(i){
   			key=$(this).children().children(".p_name").val();
   			value=$(this).children().children(".p_value").val();
   			if(key!= "" & value != ""){
                test.push({"key":key,"value":value});
      		}
        });

        extract.test=test;
        test=[];
        $('#sub_check_table').find('tbody tr').each(function(i){
            assertkey=$(this).children().children(".p_name").val();
            assertType=$(this).children().children(".checktor").val();
            assertValue=$(this).children().children(".p_value").val();
            itype=$(this).children().children(".itype").val();
   			if(assertkey!= "" & assertValue != ""){
      			test.push({"key":assertkey,"comparator":assertType,"type": itype,"value":assertValue});
      		}
           });
        asserts.test=test;

        let svLink=$("#modal_link_id").attr("hiddenId");
        let current_data = $("#"+svLink).data('data')
        let pjson=$("#param_json_val").val();
        // if(!(params== "" | typeof(params) == "undefined")){
        if($("#sub_params_table").length>0){ 
            data.params=params;
            if(!current_data){
              data.type_headers = $("#sub_params_table").data('headers')
            }
        }


        if($("#param_json_val").length>0){
            data.pjson=JSON.parse(pjson);
            if(!current_data){
              data.type_headers = $("#param_json_val").data('headers')
            }
        }else{
          if(!current_data){
            data.type_headers = $("#sub_params_table>tbody:last").data('headers')
          }       
        }


        data.extract=extract;
        data.asserts=asserts;

        data = {
          ...current_data,
          ...data
        }
        // console.log(data);
        $("#"+svLink).data('data',data);
        $("#apicaseModal").modal('hide');

    }

    function validate(){

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

        if($("#case_name").val()== ""){
   			$("#case_name").focus();
   			$("#case_name").css("background-color","#FFFFCC");
   			toastr.error('case名称必填');
   			return false;
        }

    }

    function saveApicaseToDb(Ctype){
            let url="";
            let name={};
            let parameters={};
            let test=[];
            let api=[];
            if(Ctype =="new"){
                name.index="";
                url="/api/webinterface/case/add";
            }else{
                name.index=getUrlParam("id");
                url="/api/webinterface/case/update";
            }
            
            name.author="";
            name.name=$("#case_name").val();
            name.project=$("#selapiproductid").find("option:selected").text();;
            name.module=$("#selapimoduleid").val();

            $('#params_table').find('tbody tr').each(function(i){
                key=$(this).children().children(".p_name").val();
                let valueList=$(this).children().children(".p_value").val().split(",");

   			    if(key!= "" & valueList.length>0){
      			    test.push({"key":key,"value":valueList});
      		    }
   		    });
            parameters.test=test;

            $("#transfer-right-api").find('.transfer-panel-item').each(function(){
                let tmpApi={};
                let request={};
                let request_data={};
                tmpApi.index=$(this).attr("data-value");
                let data=$(this).find(".ke-ablock").data("data");
                if(typeof(data)!="undefined"){
                    if("params" in data){
                    // if(typeof(data.params)!="undefined" ){
                        let test=data.params;
                        request_data.test=test;
                        request.request_data=request_data;
                        request.type="data";
                    }
                    if("pjson" in data){
                    // if(typeof(data.pjson)!="undefined" ){
                      // let str = JSON.stringify(data.pjson)
                      let str = data.pjson
                      if(typeof str !== 'string'){
                        str = JSON.stringify(str)
                      }
                      request.request_data=String(str).replace(/[ ]/g, "").replace(/[\r\n]/g, "");
                      // request.request_data = data.pjson
                        request.type="json";
                    }

                    if(data.type_headers['Content-Type'].includes('json')){
                      // request.header = "json"
                      request.headers = data.type_headers
                    }else{
                      // request.header = "data"
                      request.headers = data.type_headers
                    }

                    if(!request.request_data){
                      request.request_data = ""
                    }
                    if(data.type_headers['Content-Type'].includes('json')){
                      request.type="json";
                    }else{
                      request.type="data";
                    }
                    // request.headers="";//headers为空，暂时，不支持
                    tmpApi.request=request;
                    tmpApi.extract=data.extract;
                    tmpApi.validate=data.asserts;
                    api.push(tmpApi);
                }else{
                    tmpApi.request="";
                    tmpApi.extract="";
                    tmpApi.validate="";
                    api.push(tmpApi);
                }


            });

            let req={};
            req.name=name;
            req.parameters=parameters;
            req.api=api;

            req=JSON.stringify(req);

            $.ajax({
            type: "POST",
            data: req,
            url: url,
            cache: false,
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            async: false,
            success: function (result, TextStatus) {
            	if(result.success){
            	    toastr.success(result.msg);
            	}else{
            	    toastr.error(result.msg);
            	}

                },
        	error : function(msg) {
					toastr.error(msg);
			    }
            });
    }

function getCaseInfo() {
  let apiCaseInfo = undefined;
  let caseId = getUrlParam("id");
  $.ajax({
    type: "GET",
    data: "",
    url: "/api/webinterface/case/" + caseId,
    cache: false,
    dataType: 'json',
    async: false,
    success: function (caseResult, TextStatus) {
      apiCaseInfo = caseResult;
      $("#api-selproductid").find("option:contains('" + caseResult.product + "')").attr("selected", true);


      const s1SelectedVal = $('#api-selproductid').val()
      const projectItem = $('#selapiproductid')
      const apicaseProduItem =$('#apicaseproductid')
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
          apicaseProduItem.empty();
          if (result.length > 0) {
           for (i = 0; i < result.length; i++) {
                option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
            }
          }else{
            option_str += '<option value="">'+"所属项目"+'</option>'
          }
          projectItem.append(option_str)
          apicaseProduItem.append(option_str)
          apicaseProduItem.trigger('change')

          let project = apiCaseInfo.project;
          let module = apiCaseInfo.module;
          $("#selapiproductid").find("option:contains('" + project + "')").attr("selected", true);
          $("#selapiproductid").trigger("change");
          $("#selapimoduleid").find("option:contains('" + module + "')").attr("selected", true);
    
          $("#case_name").val(apiCaseInfo.name);
          let caseparams = apiCaseInfo.data;
          for (let i in caseparams) {
            for (let key in caseparams[i]) {
              value = caseparams[i][key].join(",");
              add_param_value(key, value);
            }
          }
    
          let apis = apiCaseInfo.apis;
          for (let i in apis) {
            let api = apis[i];
            apiName = api.name;
            apiId = api.id;
            let uuid = generateUUID();
            add_transfer_item(apiName, apiId, uuid);
            let uuidData = {};
            let params = [];
            let extract = {};
            let asserts = {};
            let test = [];
            let pjson = {};//json的先不处理
            uuidData.type_headers = api.data.test.request.headers;
            if ("data" in api.data.test.request) {
              paramsTmp = api.data.test.request.data;
              for (let param in paramsTmp) {
                params.push({ "key": param, "value": paramsTmp[param] });
              }
              uuidData.params = params;
            }
    
            if ("json" in api.data.test.request) {
              uuidData.pjson = api.data.test.request.json;
              if(typeof uuidData.pjson === 'string'){
                if(uuidData.pjson === ''){
                  uuidData.pjson = "{}"
                }
                uuidData.pjson = JSON.parse(uuidData.pjson)
              }
            }
    
            extractTmp = api.data.test.extract;
            for (let e in extractTmp) {
              for (let key in extractTmp[e]) {
                test.push({ "key": key, "value": extractTmp[e][key] });
              }
    
            }
    
            extract.test = test;
            test = [];
            assertsTmp = api.data.test.validate;
            for (let e in assertsTmp) {
              test.push({ "key": assertsTmp[e].check, "comparator": assertsTmp[e].comparator, "type": assertsTmp[e].type, "value": assertsTmp[e].expected });
            }
    
            asserts.test = test;
            uuidData.extract = extract;
            uuidData.asserts = asserts;
            $("#" + uuid).data('data', uuidData);
          }
        }
      });






      // let project = apiCaseInfo.project;
      // let module = apiCaseInfo.module;
      // $("#selapiproductid").find("option:contains('" + project + "')").attr("selected", true);
      // $("#selapiproductid").trigger("change");
      // $("#selapimoduleid").find("option:contains('" + module + "')").attr("selected", true);

      // $("#case_name").val(apiCaseInfo.name);
      // let caseparams = apiCaseInfo.data;
      // for (let i in caseparams) {
      //   for (let key in caseparams[i]) {
      //     value = caseparams[i][key].join(",");
      //     add_param_value(key, value);
      //   }
      // }

      // let apis = apiCaseInfo.apis;
      // for (let i in apis) {
      //   let api = apis[i];
      //   apiName = api.name;
      //   apiId = api.id;
      //   let uuid = generateUUID();
      //   add_transfer_item(apiName, apiId, uuid);
      //   let uuidData = {};
      //   let params = [];
      //   let extract = {};
      //   let asserts = {};
      //   let test = [];
      //   let pjson = {};//json的先不处理
      //   if ("data" in api.data.test.request) {
      //     paramsTmp = api.data.test.request.data;
      //     for (let param in paramsTmp) {
      //       params.push({ "key": param, "value": paramsTmp[param] });
      //     }
      //     uuidData.params = params;
      //   }

      //   if ("json" in api.data.test.request) {
      //     uuidData.pjson = api.data.test.request.json;
      //   }

      //   extractTmp = api.data.test.extract;
      //   for (let e in extractTmp) {
      //     for (let key in extractTmp[e]) {
      //       test.push({ "key": key, "value": extractTmp[e][key] });
      //     }

      //   }

      //   extract.test = test;
      //   test = [];
      //   assertsTmp = api.data.test.validate;
      //   for (let e in assertsTmp) {
      //     test.push({ "key": assertsTmp[e].check, "comparator": assertsTmp[e].comparator, "type": assertsTmp[e].type, "value": assertsTmp[e].expected });
      //   }

      //   asserts.test = test;
      //   uuidData.extract = extract;
      //   uuidData.asserts = asserts;
      //   $("#" + uuid).data('data', uuidData);
      // }

    }, error: function (caseResult) {
      toastr.error("获取case详情失败" + caseResult.msg)
    }
  });

}