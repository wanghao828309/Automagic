/*
 *
 *   RENAISSANCE - Responsive Admin Theme
 *   version 1.3.0
 *
*/

function init_acs(language, theme, editor) {
    editor.setTheme("ace/theme/" + theme);
    editor.session.setMode("ace/mode/" + language);

    editor.setFontSize(17);

    editor.setReadOnly(false);

    editor.setOption("wrap", "free");

    ace.require("ace/ext/language_tools");
    editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        autoScrollEditorIntoView: true
    });
}

var datetime = null,
        date = null;

var update = function () {
    date = moment(new Date())
    datetime.html(date.format('h:mm A'));
};

$(window).on('load', function(){
    //Preloader
    setTimeout(function(){
        $('.preloader').fadeOut(100);
    }, 500);
});


// check if browser support HTML5 local storage
function localStorageSupport() {
    return (('localStorage' in window) && window['localStorage'] !== null)
}


  //Personal working platform Sidebar

$("li.perwork-btn").click(function(){

     $(this).toggleClass("active").siblings().removeClass("active");

    var currentEle=$(this);
    
    var siblingsElel=currentEle.siblings("li.members-btn");

    $.each(siblingsElel,function(index,ele){
       $("#"+$(ele).data("href")).removeClass('members-sidebar-open');
       if($("#"+$(ele).data("href")).hasClass('dropdown-menu')){
          $("#"+$(ele).data("href")).attr("aria-expanded","false");
          $(ele).removeClass("open").removeClass("active");
       }
    });

    cta($(this)[0], $("#"+currentEle.data("href"))[0], {relativeToWindow: true}, function () {
      if($("#"+currentEle.data("href")).hasClass('dropdown-menu')){
        $("#"+currentEle.data("href")).attr("aria-expanded","true");
        currentEle.toggleClass("open");
      }else{
          $("#"+currentEle.data("href")).toggleClass('members-sidebar-open');
      }
    });

    $(currentEle.data("close")).click(function(){
      $("#"+currentEle.data("href")).removeClass('members-sidebar-open');
      currentEle.removeClass('active');
    });
  return false;

});

$(document).ready(function () {

   

      $(function () {
        $("#apitable").DataTable({

            "searching": false,
            "ordering": false,
            "info": false,
            "paging": true,

            "scrollX": false,
            "scrollY": false,
            "lengthChange": false,
            "aLengthMenu": [10, 25, 50, 75, 100],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "stripeClasses": ['strip1', 'strip2'],
            //"autoWidth": true,
            "processing": true,
            "destroy": true,
            //"dom": 'lrtip',
            "fnServerData": retrieveData,

            "language": {
                "processing": "请求数据中...",
                "lengthMenu": "Display _MENU_ records",
                "info": "Showing page _PAGE_ of _PAGES_",
                "emptyTable": "No data available in table",
                "zeroRecords": "No records to display",
                "paginate": {
                    "first": "第一页",
                    "last": "最后一页",
                    "next": ">>",
                    "previous": "<<"
                },
                "loadingRecords": "Please wait - loading..."
            },
            "serverSide": true,
            "ajax": {
                url: "/api/webinterface/api/list",
                type: 'GET',
                data: "{}",
                //用于处理服务器端返回的数据。 dataSrc是DataTable特有的
                dataSrc: "results"

            },
            "columns": [
            {
                "data": "id",
                 "title":"接口ID"
            },
            {
                "data": "project_name",
                "title":"所属项目"
            },
            {
                "data": "mudule_name",
                "title":"所属模块"
            },
            {
                "data": "name",
                "title":"接口名称"
            },
            {
                "data": "url",
                "title":"接口地址"
            },
            {
                "data": "method",
                "title":"请求方式"
            },
            {
                 "data": "create_time",
                 "title":"创建时间"
            },
            {
                "data": "update_time",
                "title":"更新时间"
            },
            {
                "data": "update_author",
                "title":"更新人"
            },{
                "data": null,
                "title":"操作"
            }
            ],
            columnDefs: [
                {
                    targets: 9,
                    render: function (a, b, c, d) {

                            var html ='<a title="试运行" href="#" class="ke-ablock"  data-toggle="modal" data-target="#envModal" onclick=\'runAPI('+eval(c.id)+',\"'+c.update_author+'\")\'><i class="glyphicon glyphicon-play-circle" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                    '<a title="查看" href="/apiInfo/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-eye-open"  style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                   '<a title="修改" href="/api/edit/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-edit" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                   '<a title="复制" href="/api/copy/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-copy" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                   '<a title="删除" href="/api/del/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-trash" onclick=\'delAPI('+c.id+')\' style="margin-left: 8px;margin-top: 5px;"></i></a>';
                        //console.log(html);
                        return html;
                    }
                }

            ],
        });

    })



    $(function () {
        $("#apicasetable").DataTable({

            "searching": false,
            "ordering": false,
            "info": false,
            "paging": true,

            "scrollX": false,
            "scrollY": false,
            "lengthChange": false,
            "aLengthMenu": [10, 25, 50, 75, 100],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "stripeClasses": ['strip1', 'strip2'],
            //"autoWidth": true,
            "processing": true,
            "destroy": true,
            //"dom": 'lrtip',
            "fnServerData": retrievecaseData,

            "language": {
                "processing": "请求数据中...",
                "lengthMenu": "Display _MENU_ records",
                "info": "Showing page _PAGE_ of _PAGES_",
                "emptyTable": "No data available in table",
                "zeroRecords": "No records to display",
                "paginate": {
                    "first": "第一页",
                    "last": "最后一页",
                    "next": ">>",
                    "previous": "<<"
                },
                "loadingRecords": "Please wait - loading..."
            },
            "serverSide": true,
            "ajax": {
                url: "/api/webinterface/case/list",
                type: 'GET',
                data: "{}",
                //用于处理服务器端返回的数据。 dataSrc是DataTable特有的
                dataSrc: "results"

            },
            "columns": [
            {
                    "data": null,
                     "title":'<label class="contentlabel"><input id="pickALL" class="pickALLToRun" onclick="allPick()" type="checkbox">全选</label>'
            },
            {
                "data": "id",
                 "title":"CASE ID"
            },
            {
                "data": "project_name",
                "title":"所属项目"
            },
            {
                "data": "mudule_name",
                "title":"所属模块"
            },
            {
                "data": "name",
                "title":"CASE名称"
            },
            {
                 "data": "create_time",
                 "title":"创建时间"
            },
            {
                "data": "update_time",
                "title":"更新时间"
            },
            {
                "data": "update_author",
                "title":"更新人"
            },{
                "data": null,
                "title":"操作"
            }
            ],
            columnDefs: [
                {
                    targets: 8,
                    render: function (a, b, c, d) {

                            var html ='<a title="运行" href="#" class="ke-ablock"  data-toggle="modal" data-target="#envModal" onclick=\'runAPICASE('+eval(c.id)+',\"'+c.update_author+'\")\'><i class="glyphicon glyphicon-play-circle" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                       '<a title="修改" href="/apicase/edit/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-edit" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                       '<a title="删除" href="/apicase/del/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-trash" onclick=\'delAPI('+c.id+')\' style="margin-left: 8px;margin-top: 5px;"></i></a>';
                        //console.log(html);
                        return html;
                    }
                },{ 
                    targets: 0,
                    render: function (a, b, c, d) {
                            var html ='<label class="contentlabel"><input class="pickToRun" type="checkbox" value="'+eval(c.id)+'"></label>';
                        //console.log(html);
                        return html;
                    }
                }

            ],
        });

    })

    $(function () {
        $("#apisuitetable").DataTable({

            "searching": false,
            "ordering": false,
            "info": false,
            "paging": true,

            "scrollX": false,
            "scrollY": false,
            "lengthChange": false,
            "aLengthMenu": [10, 25, 50, 75, 100],
            "pageLength": 10,
            "pagingType": "full_numbers",
            "stripeClasses": ['strip1', 'strip2'],
            //"autoWidth": true,
            "processing": true,
            "destroy": true,
            //"dom": 'lrtip',
            "fnServerData": retrievesuiteData,

            "language": {
                "processing": "请求数据中...",
                "lengthMenu": "Display _MENU_ records",
                "info": "Showing page _PAGE_ of _PAGES_",
                "emptyTable": "No data available in table",
                "zeroRecords": "No records to display",
                "paginate": {
                    "first": "第一页",
                    "last": "最后一页",
                    "next": ">>",
                    "previous": "<<"
                },
                "loadingRecords": "Please wait - loading..."
            },
            "serverSide": true,
            "ajax": {
                url: "/api/webinterface/suite/list",
                type: 'GET',
                data: "{}",
                //用于处理服务器端返回的数据。 dataSrc是DataTable特有的
                dataSrc: "results"

            },
            "columns": [
            {
                    "data": null,
                     "title":'<label class="contentlabel"><input id="pickALL" class="pickALLToRun" onclick="allPick()" type="checkbox">全选</label>'
            },
            {
                "data": "id",
                 "title":"ID"
            },
            {
                "data": "project_name",
                "title":"所属项目"
            },
           
            {
                "data": "name",
                "title":"名称"
            },
            {
                 "data": "create_time",
                 "title":"创建时间"
            },
            {
                "data": "update_time",
                "title":"更新时间"
            },
            {
                "data": "update_author",
                "title":"更新人"
            },{
                "data": null,
                "title":"操作"
            }
            ],
            columnDefs: [
                {
                    targets: 7,
                    render: function (a, b, c, d) {

                            var html ='<a title="运行" href="#" class="ke-ablock"  data-toggle="modal" data-target="#envModal" onclick=\'runAPISUITE('+eval(c.id)+',\"'+c.update_author+'\")\'><i class="glyphicon glyphicon-play-circle" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                       '<a title="修改" href="/apisuite/edit/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-edit" style="margin-left: 8px;margin-top: 5px;"></i></a>'+
                                       '<a title="删除" href="/apisuite/del/?id='+eval(c.id)+'" class="ke-ablock" ><i class="glyphicon glyphicon-trash" onclick=\'delAPI('+c.id+')\' style="margin-left: 8px;margin-top: 5px;"></i></a>';
                        //console.log(html);
                        return html;
                    }
                },{ 
                    targets: 0,
                    render: function (a, b, c, d) {
                            var html ='<label class="contentlabel"><input class="pickToRun" type="checkbox" value="'+eval(c.id)+'"></label>';
                        //console.log(html);
                        return html;
                    }
                }

            ],
        });

    })

    //   $.ajax({
    //         type: "GET",
    //         data: {'productid': ""},
    //         url: "/setting/get/project/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
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
    // });






   


    function retrieveData(url,data,callback){
	    var oTable = $("#apitable").dataTable(); //table1为表格的id
		var tableSetings=oTable.fnSettings();
		var paging_length=tableSetings._iDisplayLength;//当前每页显示多少
		var page_start=tableSetings._iDisplayStart;//当前页开始
		var pagevalue=(page_start / paging_length)+1; //得到页数值  比页码小1
//        console.log("page start from:"+page_start);
//        console.log("page length:"+pagevalue);

	    if (typeof(pagevalue) == "undefined")
         {
             pagevalue=1;
         }

         /*
         自定义搜索条件
         */
         data.push({"name":"project","value":$("#selapiproductid").val()})
         data.push({"name":"module","value":$("#selapimoduleid").val()})
         data.push({"name":"method","value":$("#req_method").val()})
         data.push({"name":"name","value":$("#apiname").val()})
         data.push({"name":"url","value":$("#apiurl").val()})

	    var page={
	    "name":"page",
	    "value":pagevalue
	    };
	    var size={
	    "name":"size",
	    "value":10
	    };
	    data.push(page);
	    data.push(size);
		$.ajax({
                url: "/api/webinterface/api/list",
                type: 'GET',
                data: data,
			   success : function(result) {
                    
                    result.recordsFiltered=result.count;
                    result.recordsTotal=result.results.length;
                    
					callback(result);//把返回的数据传给这个方法就可以了,datatable会自动绑定数据的
			    },
			    error : function(msg) {
					console.log(msg)
			    }

	}
	)
    }
    
    function retrievecaseData(url,data,callback){
	    var oTable = $("#apicasetable").dataTable(); //table1为表格的id
		var tableSetings=oTable.fnSettings();
		var paging_length=tableSetings._iDisplayLength;//当前每页显示多少
		var page_start=tableSetings._iDisplayStart;//当前页开始
		var pagevalue=(page_start / paging_length)+1; //得到页数值  比页码小1
//        console.log("page start from:"+page_start);
//        console.log("page length:"+pagevalue);

	    if (typeof(pagevalue) == "undefined")
         {
             pagevalue=1;
         }

         /*
         自定义搜索条件
         */
         data.push({"name":"project","value":$("#selapiproductid").val()})
         data.push({"name":"module","value":$("#selapimoduleid").val()})
         data.push({"name":"method","value":$("#req_method").val()})
         data.push({"name":"name","value":$("#apicasename").val()})
         

	    var page={
	    "name":"page",
	    "value":pagevalue
	    };
	    var size={
	    "name":"size",
	    "value":10
	    };
	    data.push(page);
	    data.push(size);
		$.ajax({
                url: "/api/webinterface/case/list",
                type: 'GET',
                data: data,
			   success : function(result) {
                   
                    result.recordsFiltered=result.count;
                    result.recordsTotal=result.results.length;
					callback(result);//把返回的数据传给这个方法就可以了,datatable会自动绑定数据的
			    },
			    error : function(msg) {
					console.log(msg)
			    }

	}
	)
    }
    
    function retrievesuiteData(url,data,callback){
	    var oTable = $("#apisuitetable").dataTable(); //table1为表格的id
		var tableSetings=oTable.fnSettings();
		var paging_length=tableSetings._iDisplayLength;//当前每页显示多少
		var page_start=tableSetings._iDisplayStart;//当前页开始
		var pagevalue=(page_start / paging_length)+1; //得到页数值  比页码小1
//        console.log("page start from:"+page_start);
//        console.log("page length:"+pagevalue);

	    if (typeof(pagevalue) == "undefined")
         {
             pagevalue=1;
         }

         /*
         自定义搜索条件
         */
         data.push({"name":"project_id","value":$("#selapiproductid").val()})
//         data.push({"name":"module","value":$("#selapimoduleid").val()})
         data.push({"name":"method","value":$("#req_method").val()})
         data.push({"name":"name","value":$("#apisuitename").val()})
         

	    var page={
	    "name":"page",
	    "value":pagevalue
	    };
	    var size={
	    "name":"size",
	    "value":10
	    };
	    data.push(page);
	    data.push(size);
		$.ajax({
                url: "/api/webinterface/suite/list",
                type: 'GET',
                data: data,
			   success : function(result) {
                    result.recordsFiltered=result.count;
                    result.recordsTotal=result.results.length;
					callback(result);//把返回的数据传给这个方法就可以了,datatable会自动绑定数据的
			    },
			    error : function(msg) {
					console.log(msg)
			    }

	}
	)
    }
    
     //menuStyle add by yansl:
     $(".menu_link").on("click",function(){
        $(".menu_link").each(function(){
            $(this).parent().removeClass('first_dd');
        })
        $(this).parent().css('background-color','#fafafa');
    })



	})



