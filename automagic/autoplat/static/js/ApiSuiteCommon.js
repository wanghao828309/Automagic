$(function(){
  //   $.ajax({
  //       type: "GET",
  //       data: {'productid': ""},
  //       url: "/setting/get/project/", 
  //       cache: false,
  //       dataType: 'json',
  //       async: false,
  //       success: function (result, TextStatus) {
  //           //元素管理元素添加项目选择
  //           var projectItem=$("#selapiproductid")
  //           projectItem.empty();
  //           projectItem.append('<option value="">所属项目</option>')
  //           if (result.length > 0) {
  //               for (i = 0; i < result.length; i++) {
  //                   projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');                    
  //               }
  //           }

  //           projectItem=$("#apicaseproductid")
  //           projectItem.empty();
  //           projectItem.append('<option value="">所属项目</option>')
  //           if (result.length > 0) {
  //               for (i = 0; i < result.length; i++) {
  //                   projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');                    
  //               }
  //           }

          

  //   }

  // })



  $("#apicaseproductid").bind("change", function () {
    var s1SelectedVal = $('#apicaseproductid').val();
    $.ajax({
        type: "GET",
        data: {'projectid': s1SelectedVal},
        url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
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
      }
     )
    }
   )//end change
 }
)


function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

function serachAPI(){
           
    //请求后台
let data={};
data.name=$("#apisearchstr").val();
data.project=$("#apicaseproductid").val();
data.module=$("#apicasemoduleid").val();
data.page=1;
data.size=100;//默认加载100个，这个足够了
$.ajax({
    type: "GET",
    data: data,
    url: "/api/webinterface/case/list", 
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

function validate(){

    if($("#selapiproductid").val()== ""){
           $("#selapiproductid").focus();
           $("#selapiproductid").css("background-color","#FFFFCC");
           toastr.error('项目必填');
           return false;
       }

       
    if($("#case_name").val()== ""){
           $("#case_name").focus();
           $("#case_name").css("background-color","#FFFFCC");
           toastr.error('suite名称必填');
           return false;
    }
      
}

function add_transfer_item(apiName,apiId){
   
   let html='<label class="transfer-panel-item" data-text="'+apiName+'" data-value="'+apiId+'">\
                  <span class="checkbox-input pull-left">\
                      <input type="checkbox" class="checkbox-inline" value="'+apiId+'">\
                  </span>\
                  <span class="checkbox-label pull-left">\
                      <span>'+apiName+'</span>\
                  </span>\
           </label>';
   $("#transfer-right-api").append(html);        
}

function loadApiSuite(){
    let apiSuiteInfo=undefined;
    let suiteId=getUrlParam("id");
    $.ajax({
            type: "GET",
            data: "",
            url: "/api/webinterface/suite/info?id="+suiteId, 
            cache: false,
            dataType: 'json',
            async: false,
            success: function (suiteResult, TextStatus) {
                apiSuiteInfo=suiteResult;
                $("#api-selproductid").find("option:contains('" + suiteResult.product + "')").attr("selected", true);


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
          
                    let project_name = apiSuiteInfo.project_name;
                    $("#selapiproductid").find("option:contains('" + project_name + "')").attr("selected", true);
                    $("#selapiproductid").trigger("change");
              
                    $("#case_name").val(apiSuiteInfo.name);
                    // let caseparams=apiSuiteInfo.data;
                   
                    
                    let cases=apiSuiteInfo.case_info;
                    for (let i in cases){
                        let caseInfo=cases[i];
                        caseName=caseInfo.name;
                        caseId=caseInfo.id;       
                        add_transfer_item(caseName,caseId);
                    }

                    }
                  });




                
                // let project=apiSuiteInfo.project_name;
    
                // $("#selapiproductid").find("option:contains('"+project+"')").attr("selected",true);
                
            
                // $("#case_name").val(apiSuiteInfo.name);
                // // let caseparams=apiSuiteInfo.data;
               
                
                // let cases=apiSuiteInfo.case_info;
                // for (let i in cases){
                //     let caseInfo=cases[i];
                //     caseName=caseInfo.name;
                //     caseId=caseInfo.id;       
                //     add_transfer_item(caseName,caseId);
                // }
        },error:function(suiteResult){
            toastr.error("获取suite详情失败"+suiteResult.msg)
        }
    });

    // let project=apiSuiteInfo.project_name;
    
    // $("#selapiproductid").find("option:contains('"+project+"')").attr("selected",true);
    

    // $("#case_name").val(apiSuiteInfo.name);
    // // let caseparams=apiSuiteInfo.data;
   
    
    // let cases=apiSuiteInfo.case_info;
    // for (let i in cases){
    //     let caseInfo=cases[i];
    //     caseName=caseInfo.name;
    //     caseId=caseInfo.id;       
    //     add_transfer_item(caseName,caseId);
    // }
}

function saveSuiteToDb(Ctype){
            let url="";
            let data={};
            if(Ctype==="new"){
                url="/api/webinterface/suite/add";
            }else{
                data.id=getUrlParam("id");
                url="/api/webinterface/suite/update";
            }
            
            let case_ids=[];
            data.suite_name=$("#case_name").val();
            data.project_id=$("#selapiproductid").find("option:selected").val();
            $("#transfer-right-api").find('.transfer-panel-item').each(function(){                
                case_ids.push($(this).attr("data-value"));
            }); 
            data.case_ids=case_ids;
            req=JSON.stringify(data);
		    console.log(req);
          
            $.ajax({
            type: "POST",
            data: req,
            url: url,
            cache: false,
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            async: false,
            success: function (result, TextStatus) {
                  if(result.code==='30002'){
                    toastr.error(result.msg); 
                  }else{
                    toastr.success(result.msg);          
                  }

                },
        	error : function(msg) {
					toastr.error(msg);
			    }
            });

}