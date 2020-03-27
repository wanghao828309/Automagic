/**
 * Created by ray on 16-9-9.
 */


let elementEditSelectChangeFlag
let caseEditFlag
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)return r[2];return 0;
}

function setOptions(result,elment){
  elment.empty();
  elment.append('<option value="">所属项目</option>')
  if (result.length > 0) {
      for (i = 0; i < result.length; i++) {
          elment.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
      }
  }

  if (elment.val() != localStorage.getItem('project')) {
      // alert('test');
      elment.find("option[value=" + localStorage.getItem('project') + "]").attr("selected", true);
  }
  if (elment.val() != "") {
      elment.change();
  }
};
    //产品和项目二级菜单关联 通过product关联project下拉菜单
    $("#selproductid").bind("change", function () {
      var s1SelectedVal = $('#selproductid').val();
      $("#right_content").contents().find('#check_productid').val(s1SelectedVal);
      $.ajax({
          type: "GET",
          data: {'productid': s1SelectedVal},
          url: "/setting/get/project/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
          cache: false,
          dataType: 'json',
          async: false,
          success: function (result, TextStatus) {
              //用例管理 
              var caseaddSelmoduleid = $("#right_content").contents().find("#selmoduleid.caseaddframe")
              var caseeditSelmoduleid = $("#right_content").contents().find("#selmoduleid.caseeditframe")
              var caseframeProjectItem = $("#right_content").contents().find("#selprojectid.caseframe")
              //元素管理元素添加项目选择
              var projectItem=$("#right_content").contents().find("#selprojectid")
              //任务管理 添加任务 项目
              const selprojectid_task = $('#right_content').contents().find('#selprojectid_task')
              //任务管理 编辑任务 项目
              const selprojectid_task_edit = $('#right_content').contents().find('#selprojectid_task_edit')
              //任务管理 添加任务树
              const treeDemo = $('#right_content').contents().find('#treeDemo')
              
              //获取表单action
              let form = $("#right_content").contents().find('#case_edit')
              let form_action = form.attr('action')
              if(form.length === 0 ){
                form_action = $("#right_content").contents().find('#case_copy').attr('action')
              }
              if(form_action==='/func/case/update/'){
                if(caseEditFlag){
                  let option_str = '<option value="0">所属项目</option>'
                  if (result.length > 0) {
                      for (i = 0; i < result.length; i++) {
                        option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                      }
                  }
                  projectItem.empty();
                  projectItem.append(option_str)
                  caseaddSelmoduleid.empty()
                  caseaddSelmoduleid.append('<option value="0">所属项目</option>')
                  caseeditSelmoduleid.empty()
                  caseeditSelmoduleid.append('<option value="0">所属项目</option>')
                }else{
                  let option_str = '<option value="0">所属项目</option>'
                  if (result.length > 0) {
                      for (i = 0; i < result.length; i++) {
                        option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                  }
                  caseframeProjectItem.empty()
                  caseframeProjectItem.append(option_str)
                  caseEditFlag = true
                }
              } else if (form_action && form_action.indexOf('/func/case/copy/')!== -1) {
                if (caseEditFlag) {
                  let option_str = '<option value="0">所属项目</option>'
                  if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                      option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                  }
                  projectItem.empty();
                  projectItem.append(option_str)
                  caseaddSelmoduleid.empty()
                  caseaddSelmoduleid.append('<option value="0">所属项目</option>')
                  caseeditSelmoduleid.empty()
                  caseeditSelmoduleid.append('<option value="0">所属项目</option>')
                } else {
                  let option_str = '<option value="0">所属项目</option>'
                  if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                      option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                  }
                  caseframeProjectItem.empty()
                  caseframeProjectItem.append(option_str)
                  caseEditFlag = true
                }
              } else {
                projectItem.empty();
                let option_str = '<option value="">所属项目</option>'
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                      option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                projectItem.append(option_str)
                if (projectItem.val() != localStorage.getItem('project')) {
                    // alert('test');
                    projectItem.find("option[value=" + localStorage.getItem('project') + "]").attr("selected", true);
                }
                if (projectItem.val() != "") {
                    projectItem.change();
                }
                var eleprojectItem=$("#right_content").contents().find("#sel_projectid")
                setOptions(result,eleprojectItem)
  
                //任务管理 添加任务 填充项目
                if(selprojectid_task.length>0){
                  selprojectid_task.empty()
                  selprojectid_task.append(option_str)
                }
                //任务管理 编辑任务 填充项目
                if(selprojectid_task_edit.length>0){
                  if(elementEditSelectChangeFlag){
                    selprojectid_task_edit.empty()
                    selprojectid_task_edit.append(option_str)
                  }else{
                    elementEditSelectChangeFlag = true
                    $(window.parent.document).find("#selproductid").val('0')
                  }
                }
                //任务管理 当产品变化时 将树置空
                treeDemo.html('')
              }
          }
      });

      $("#right_content").contents().find('#mytable').on('click','.ke-ablock[title=编辑]',function(event){
        elementEditSelectChangeFlag = false
        caseEditFlag = false
      })

      if (s1SelectedVal == localStorage.getItem('product')) {
          return;
      }
      $("#right_content").contents().find('#search_btn').click()
      localStorage.setItem('product', s1SelectedVal);
      localStorage.setItem('moduleid', '');
      // $('#search_btn').trigger('click');
  });
$('#right_content').load(function () {







    $('#selproductid').change()
    $('#sel_projectid').change()
    /*chenwx selprojectid选项框如果值不为空就发起请求加载对应的模块*/
    if($("#right_content").contents().find('#selprojectid').val()){
        var s1SelectedVal = $("#right_content").contents().find("#selprojectid").val();
        localStorage.setItem('project', s1SelectedVal);
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                var moduleItem=$("#right_content").contents().find("#selmoduleid")
                //获取表单action
                let form = $("#right_content").contents().find('#case_edit')
                let form_action = form.attr('action')
                if(form.length === 0 ){
                  form_action = $("#right_content").contents().find('#case_copy').attr('action')
                }

                if(form_action==='/func/case/update/'){
                  if(caseEditFlag){
                    console.log('第一次进入caseframe不加载模块')
                  }else{
                    caseEditFlag = true
                  }
                } else if (form_action && form_action.indexOf('/func/case/copy/')!== -1) {
                  if (caseEditFlag) {
                    console.log('第一次进入caseframe不加载模块')
                  } else {
                    caseEditFlag = true
                  }
                }else{
                  moduleItem.empty();
                  moduleItem.append('<option value="">所属模块</option>');
                  if (result.length > 0) {
                      for (i = 0; i < result.length; i++) {
                          moduleItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                      }
                  }
                  if (moduleItem.val() != localStorage.getItem('moduleid')) {
                      moduleItem.find("option[value=" + localStorage.getItem('moduleid') + "]").attr("selected", true);
                  }
                }
            }
        });
        var projectid_url = getUrlParam('projectid');
        if (projectid_url == 0 && $('#selprojectid').val() !== null){
            $('#search_btn').trigger('click');
        }
    }
    /*chenwx sel_projectid选项框如果值不为空就发起请求加载对应的模块*/
    if($("#right_content").contents().find('#sel_projectid').val()){
      var s1SelectedVal = $("#right_content").contents().find('#sel_projectid').val();
      console.log(s1SelectedVal)
      $.ajax({
          type: "GET",
          data: {'projectid': s1SelectedVal},
          url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
          cache: false,
          dataType: 'json',

          success: function (result, TextStatus) {
            $("#right_content").contents().find('#selvalue').empty();
            $("#right_content").contents().find('#selvalue').append('<option value="">所属模块</option>');
              if (result.length > 0) {
                  for (i = 0; i < result.length; i++) {
                    $("#right_content").contents().find('#selvalue').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                  }
              }
          }
      });
  }

    /*
    add by yansl@wondershare.cn
    项目的初始化跟联动
    */


    /*    通过project关联module下拉菜单   */
    $("#right_content").contents().find("#selprojectid").bind("change", function () {
        var s1SelectedVal = $("#right_content").contents().find("#selprojectid").val();
        localStorage.setItem('project', s1SelectedVal);
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                var moduleItem=$("#right_content").contents().find("#selmoduleid")
                moduleItem.empty();
                moduleItem.append('<option value="">所属模块</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        moduleItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                if (moduleItem.val() != localStorage.getItem('moduleid')) {
                    moduleItem.find("option[value=" + localStorage.getItem('moduleid') + "]").attr("selected", true);
                }

            }
        });
        var projectid_url = getUrlParam('projectid');
        if (projectid_url == 0 && $('#selprojectid').val() !== null){
            $('#search_btn').trigger('click');
        }
    });

     $("#right_content").contents().find("#sel_projectid").bind("change", function () {
        var s1SelectedVal = $("#right_content").contents().find("#sel_projectid").val();
        localStorage.setItem('project', s1SelectedVal);
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                var moduleItem=$("#right_content").contents().find("#selvalue")
                moduleItem.empty();
                moduleItem.append('<option value="">所属模块</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        moduleItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                if (moduleItem.val() != localStorage.getItem('moduleid')) {
                    moduleItem.find("option[value=" + localStorage.getItem('moduleid') + "]").attr("selected", true);
                }

            }
        });
        var projectid_url = getUrlParam('projectid');
        if (projectid_url == 0 && $('#selprojectid').val() !== null){
            $('#search_btn').trigger('click');
        }
    });

    /*   通过module关联element 菜单 */
    $("#right_content").contents().find("#selmoduleid").bind("change", function () {
        var moduleVal = $("#right_content").contents().find("#selmoduleid").val();
        var moduleid = localStorage.getItem('moduleid');
        if (moduleVal!== moduleid){
            $('#search_btn').trigger('click');
            localStorage.setItem('moduleid', moduleVal);
        }
    });

    /*    添加元素页面 project关联module下拉多选菜单   */
    $("#sel_projectid").bind("change", function () {
        var s1SelectedVal = $('#sel_projectid').val();
        // $('#mdlist').val('');
        // $('#selvalue').val('');
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',

            success: function (result, TextStatus) {
                // $('.multi_select').empty();
                // $('#selmoduleid').append('<option value="">所属模块</option>');
                // if (result.length > 0) {
                //    $(function (){
                //      $('.multi_select').MSDL({
                //        'width': '160',
                //        'data': result,
                //      });
                //    });
                // }
                $('#selvalue').empty();
                $('#selvalue').append('<option value="">所属模块</option>');
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                        $('#selvalue').append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
            }
        });
    });

    /*    编辑元素project关联module下拉菜单   */
    $("#right_content").contents().find("#eleprojectid").bind("change", function () {
        var s1SelectedVal = $("#right_content").contents().find("#eleprojectid").val();
        // alert($('#eleprojectid').val())
        $.ajax({
            type: "GET",
            data: {'projectid': s1SelectedVal},
            url: "/setting/get/module/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
            cache: false,
            dataType: 'json',
            async: false,

            success: function (result, TextStatus) {
                let elemoduleid = $("#right_content").contents().find('#elemoduleid')
                let options_str = ''
                elemoduleid.empty();
                options_str += '<option value="">所属模块</option>'
                if (result.length > 0) {
                    for (i = 0; i < result.length; i++) {
                      options_str +=('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                    }
                }
                elemoduleid.append(options_str)
            }
        });
    });

    /*    添加测试用例    */
    $('#case_add').submit(function () {
        $('[name="autocomplete"]').each(function () {
            if ($(this).val() == '') {
                $(this).next().val('None')
            }
        });
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            //             data:{casedesc:casedesc, isenabled:isenabled, issmoke:issmoke, projectid:projectid, moduleid:moduleid,dependent:dependent,descr:descr,keyword:keyword,elementid:elementid,inputtext:inputtext},
            url: "/func/case/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
                window.location.href = "/func/case/list/"
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('保存失败');
                setTimeout("$('#log_info').css('display','none');", 1500);
            }
        });
        return false;
    });

    /*    添加元素     */
    $('#ele_add').submit(function () {
        var descr = $("#id_descr").val();      //获得form中用户输入的descr 注意这里的descr 与你html中的id一致
        var projectid = $("#sel_projectid").val(); //同上
        var moduleid = $("#selvalue").val(); //同上
        var locmode = $("#id_locmode").val();
        var location = $("#id_location").val();
        var m = []
        m = moduleid.split(';')
        // alert(m.length);
        for (i = 0; i < m.length; i++) {
            $.ajax({
                type: "POST",
                data: {descr: descr, projectid: projectid, moduleid: m[i], locmode: locmode, location: location},
                url: "/func/element/add/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致
                cache: false,
                dataType: "html",

                success: function (result, statues, xml) {
                    debugger;
                    $('#log_info').addClass('bg-primary');
                    $('#log_info').css('display', 'block');
                    $('#log_info').html(result);
                    setTimeout("$('#log_info').css('display', 'None');$('#id_location').val('');", 1500);  //成功时弹出view传回来的结
                    setTimeout("location.reload()", 1500);
                    window.location.href = "/func/element/list/"
                },
                error: function () {
                    debugger;
                    $('#log_info').addClass('bg-primary');
                    $('#log_info').css('display', 'block');
                    $('#log_info').html('添加失败。');
                    setTimeout("location.reload()", 1500);
                }
            });
        }

        return false;
    });

    /*     添加关键字     */
    $('#add_keyword').submit(function () {
        var keyword = $('#keyword').val();
        var kwdescr = $('#kwdescr').val();
        var productid = $('#selproductid').val();
        $.ajax({
            type: "POST",
            data: {keyword: keyword, kwdescr: kwdescr, productid: productid},
            url: "/func/keyword/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                // debugger;
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
                window.location.href = "/func/keyword/list/"
                // alert(result);
            },
            error: function () {
                // debugger;
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('添加失败，关键字可能已经存在。');
                setTimeout("location.reload()", 1500);
            }
        });
        return false;
    });

    /*    添加产品     */
    $('#product_add').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/product/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#addProductModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     编辑产品     */
    $('#product_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/product/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editProductModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     添加项目     */
    $('#project_add').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/project/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#addProjectModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     编辑项目     */
    $('#project_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),

            url: "/setting/project/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editProjectModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*   添加模块   */
    $('#module_add').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/module/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#addModuleModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*  编辑模块   */
    $('#module_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/setting/module/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editModuleModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1200);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    /*     提交编辑元素    */
    $('#element_edit').submit(function () {
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/func/element/update/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#editElementModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });

    $(".radioitem").bind("change", function () {
        var selectvalue = $("input[name='tasktype']:checked").val();
        if (selectvalue == 1) {
            $("#testrailrunid").show();
            $("#testrailsuites").hide();
            $("#testsectionid").hide();
            $("#treeDemo").show();
            $("#customParameters").show();
            $("#jenkins_server_url").hide();
            $("#user_id").hide();
            $("#api_token").hide();
            $("#build_name").hide();
            $("#Jtask_id").hide();
            $("#selectedCases").show();
            $("#coverid").hide();
        }
        else if (selectvalue == 2) {
            $("#testrailrunid").hide();
            $("#testrailsuites").show();
            $("#testsectionid").show();
            $("#treeDemo").show();
            $("#customParameters").show();
            $("#jenkins_server_url").hide();
            $("#user_id").hide();
            $("#api_token").hide();
            $("#build_name").hide();
            $("#Jtask_id").hide();
            $("#selectedCases").show();
            $("#coverid").show();
        }
        else {
            $("#testrailrunid").show();
            $("#testrailsuites").hide();
            $("#testsectionid").hide();
            $("#treeDemo").hide();
            $("#customParameters").hide();
            $("#jenkins_server_url").show();
            $("#user_id").show();
            $("#api_token").show();
            $("#build_name").show();
            $("#Jtask_id").show();
            $("#selectedCases").hide();
            $("#coverid").hide();
        }
    });

    /*     提交新增任务    */
    $('#task_add').submit(function () {

        var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = treeObj.getCheckedNodes(true);
        console.log(nodes)
        var index = 1;
        var text = '';
        var jsonlist = {}
        nodes.forEach(function (node) {
            if (node.level === 1) {
                var childIds = []
                node.children.forEach(function (child) {
                    if (child.checked === true) {
                        childIds.push(child.id)
                    }
                })
                jsonlist[index++] = childIds.join(',')
            }
        })
        text = JSON.stringify(jsonlist);
        // for (x in nodes){
        //     if (nodes[x].id < 9999999){
        //         text = text + nodes[x].id + ",";
        //     }
        // }
        $('#caseids').val(text);
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            url: "/func/task/add/",
            cache: false,
            dataType: "html",
            success: function (result, statues, xml) {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("window.location.href='/func/task/list/'", 500);
            },
            error: function () {
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html('创建失败');
                alert('创建失败')
            }
        });
        return false;
    });




});

/*    点击产品编辑按钮    */
function setproductValue(id) {
    $.ajax({
        type: "GET",
        data: {'productid': id},
        url: "/setting/setedit/product/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editProductModal [name="productid"]').val(result[i].id);
                    $('#editProductModal [name="productname"]').val(result[i].name);
                    $('#editProductModal [name="descr"]').val(result[i].descr);
                    $('#editProductModal [name="sortby"]').val(result[i].sortby);

                    if (result[i].isenabled) {
                        $('#editProductModal input:checkbox').attr("checked", "checked");
                    }
                    else {
                        $('#editProductModal input:checkbox').attr("checked", false);
                    }
                }
            }
        }
    });
}

/*   点击项目编辑按钮    */
function setprojectValue(id) {
    $.ajax({
        type: "GET",
        data: {'projectid': id},
        url: "/setting/setedit/project/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editProjectModal [name="projectid"]').val(result[i].id);
                    $('#editProjectModal [name="projectname"]').val(result[i].name);
                    $('#editProjectModal [name="descr"]').val(result[i].descr);
                    $('#editProjectModal [name="version"]').val(result[i].version);
                    $('#editProjectModal [name="sortby"]').val(result[i].sortby);

                    if (result[i].isenabled) {
                        $('#editProjectModal input:checkbox').attr("checked", "checked");
                    }
                    else {
                        $('#editProjectModal input:checkbox').attr("checked", false);
                    }
                }
            }
        }
    });
}

/*点击模块编辑按钮*/
function setmoduleValue(id) {
    $.ajax({
        type: "GET",
        data: {'moduleid': id},
        url: "/setting/setedit/module/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editModuleModal [name="moduleid"]').val(result[i].id);
                    $('#editModuleModal [name="modulename"]').val(result[i].name);
                    $('#editModuleModal [name="sortby"]').val(result[i].sortby);

                    if (result[i].isenabled) {
                        $('#editModuleModal input:checkbox').attr("checked", "checked");
                    }
                    else {
                        $('#editModuleModal input:checkbox').attr("checked", false);
                    }
                    // debugger;
                }
            }
        }
    });
}

/*    点击用户编辑按钮    */
function setuserValue(id) {
    $.ajax({
        type: "GET",
        data: {'userid': id},
        url: "/setting/setedit/user/",
        cache: false,
        dataType: 'json',

        success: function (result, TextStatus) {
            if (result.length > 0) {
                for (i = 0; i < result.length; i++) {
                    $('#editUserModal [name="userid"]').val(result[i].id);
                    $('#editUserModal [name="username"]').val(result[i].username);
                    // $('#editUserModal [name="password"]').val(result[i].password);
                    // $('#editUserModal [name="confirmPassword"]').val(result[i].password);
                    $('#editUserModal [name="password"]').val('');
                    $('#editUserModal [name="confirmPassword"]').val('');
                    $('#editUserModal [name="email"]').val(result[i].email);
                    $('#editUserModal [name="realname"]').val(result[i].realname);
                    $('#editUserModal [name="mobile"]').val(result[i].mobile);
                    $('#editUserModal [name="testrailuser"]').val(result[i].testrailuser);
                    $('#editUserModal [name="testrailpass"]').val(result[i].testrailpass);
                    if (result[i].is_active) {
                        $('#editUserModal input[name="is_active"]').attr("checked", "checked");
                    }
                    else {
                        $('#editUserModal input[name="is_active"]').attr("checked", false);
                    }
                    if (result[i].is_admin) {
                        $('#editUserModal input[name="is_admin"]').attr("checked", "checked");
                    }
                    else {
                        $('#editUserModal input[name="is_admin"]').attr("checked", false);
                    }

                }
            }
        }
    });
}




/*    点击元素编辑按钮    */
function setelementValue(id) {
    var projectid="";
    var moduleid="";
    $.ajax({
        type: "GET",
        data: {'elementid': id},
        url: "/func/setedit/element/",
        cache: false,
        dataType: 'json',
        async: false,

        success: function (result, TextStatus) {
            projectid=result[0].projectid;
            moduleid=result[0].moduleid;
            if (result.length > 0) {
                for (var i = 0; i < result.length; i++) {

                    $("#editElementModal [name='elementid']").val(result[i].id);
                    $("#editElementModal [name='eledescr']").val(result[i].descr);
                    $("#editElementModal [name='ele_add_projectid']").val(result[i].projectid);
                    $('#eleprojectid').change();
                    $("#editElementModal [name='moduleid]").val(result[i].moduleid);
                    $("#editElementModal [name='locmode']").val(result[i].locmode);
                    $("#editElementModal [name='elelocation']").val(result[i].location);
                }

            }
            // alert(result[i].projectid);

        }
    });

    var projectItem= $("#editElementModal [name='ele_add_projectid']");
    var moduleItem=$("#editElementModal [name='moduleid']");
    //iframe 获取父页面元素的值
    var productId=$(window.parent.document).find("#selproductid").val();
    //var productId=$("#selproductid").val();



    
    $.ajax({
      type: "GET",
      data: {'productid': productId},
      url: "/setting/get/project/",
      cache: false,
      dataType: 'json',
      async: false,
      success: function (result, TextStatus) {

          projectItem.empty();
          projectItem.append('<option value="">'+"请选择项目"+'</option>')
          if (result.length > 0) {
           for (i = 0; i < result.length; i++) {
                  projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
              }
           }
          if(projectid != "")
              {
               projectItem.find("option[value=" +projectid+ "]").attr("selected", true);
          }else{
              projectItem.find("option[value=" +"请选择项目"+ "]").attr("selected", true);
           }

          if (projectItem.val() != "") {
              projectItem.change();
          }
      }
  });
    //chenwx 判断所属项目是否为空，为空则不进行下面的ajax请求 
    if(!$('#selprojectid').val() && productId==='0'){
      moduleItem.empty();
      moduleItem.append('<option value="">'+"请选择模块"+'</option>')

      // projectItem.empty();
      // projectItem.append('<option value="">'+"请选择项目"+'</option>')
      return false
    }


     $.ajax({
                    type: "GET",
                    data: {'projectid': projectid},
                    url: "/setting/get/module/",
                    cache: false,
                    dataType: 'json',
                    async: false,
                    success: function (result, TextStatus) {

                        moduleItem.empty();
                        moduleItem.append('<option value="">'+"请选择模块"+'</option>')
                        if (result.length > 0) {
                         for (i = 0; i < result.length; i++) {
                                moduleItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
                            }
                         }
                        if(moduleid != "")
                        {
                             moduleItem.find("option[value=" +moduleid+ "]").attr("selected", true);
                        }else{
                             moduleItem.find("option[value=" +"请选择模块"+ "]").attr("selected", true);
                         }


                        if (moduleItem.val() != "") {
                            moduleItem.change();
                        }
//                         alert(moduleItem.innerHTML);
                    }
     });

}

/*    点击元素编辑按钮    */
function setkeywordValue(id){

    $.ajax({
        type:"GET",
        data:{'keywordid':id},
        url: "/func/setedit/keyword/",
        cache: false,
        dataType:'json',

        success: function(result,TextStatus) {
            if (result.length >0){
                for(var i=0; i<result.length; i++) {
                    // $('#editKeywordModal [name="productid"]').val(result[i].productid);
                    $('#editKeywordModal [name="productname"]').find("option[value="+result[i].productid+"]").attr("selected",true);
                    $('#editKeywordModal [name="keywordid"]').val(result[i].id);
                    $('#editKeywordModal [name="kwdescr"]').val(result[i].descr);
                    $('#editKeywordModal [name="keyword"]').val(result[i].name);
                }

         }
         // alert(result[i].projectid);
        },
        error:function (result) {
            alert(result)
        }
     });

}

/*     编辑元素     */
   $('#keyword_edit').submit(function () {
       $.ajax({
           type:"POST",
           data: $(this).serialize(),
           url:"/func/keyword/update/",
           cache: false,
           dataType:"html",
           success:function (result, statues,xml) {
               $('#editProductModal').hide()
               $('#log_info').addClass('bg-primary');
               $('#log_info').css('display','block');
               $('#log_info').html(result);
               setTimeout("location.reload()",1200);
           },
           error:function () {
               $('#log_info').addClass('bg-primary');
               $('#log_info').css('display','block');
               $('#log_info').html('创建失败');
               alert('创建失败')
           }
       });
       return false;
   });

/*     添加用户     */
$(function () {
    $('#user_add')
        .bootstrapValidator({
//        live: 'disabled',
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'icon icon-ok',
                invalid: 'icon icon-remove',
                validating: 'icon icon-refresh'
            },
            fields: {
                username: {
                    message: '无效的用户名',
                    validators: {
                        notEmpty: {
                            message: '登录用户名不能为空'
                        },
                        stringLength: {
                            min: 4,
                            max: 30,
                            message: '用户名的长度为4-30字符'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.\@]+$/,
                            message: '用户名只能由字母、数字和下划线组成'
                        },
                        different: {
                            field: 'password',
                            message: '用户名和密码不能一样'
                        }
                    }
                },
                email: {
                    validators: {
                        emailAddress: {
                            message: '无效的邮箱地址'
                        },
                        notEmpty: {
                            message: '邮箱地址不能为空'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '登录密码不能为空'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能和用户名一样'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'password',
                            message: '密码和确认密码输入不一致'
                        }
                    }
                }
            }
        })

        .on('success.form.bv', function (e) {

            e.preventDefault();

            var $form = $(e.target);

            var bv = $form.data('bootstrapValidator');

            $.post($form.attr('action'), $form.serialize(), function (result) {
                $('#addUserModal').hide()
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
            })
        });

});

/*     编辑用户     */
$(function () {
    $('#user_edit')
        .bootstrapValidator({
//        live: 'disabled',
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'icon icon-ok',
                invalid: 'icon icon-remove',
                validating: 'icon icon-refresh'
            },
            fields: {
                email: {
                    validators: {
                        emailAddress: {
                            message: '无效的邮箱地址'
                        },
                        notEmpty: {
                            message: '邮箱地址不能为空'
                        }
                    }
                },
                password: {
                    validators: {
                        identical: {
                            field: 'confirmPassword',
                            message: '密码和确认密码输入不一致'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        identical: {
                            field: 'password',
                            message: '密码和确认密码输入不一致'
                        }
                    }
                }
            }
        })
        //         .bootstrapValidator({
        // //        live: 'disabled',
        //         message: 'This value is not valid',
        //         feedbackIcons: {
        //             valid: 'icon icon-ok',
        //             invalid: 'icon icon-remove',
        //             validating: 'icon icon-refresh'
        //         },
        //         fields: {
        //             email: {
        //                 validators: {
        //                     emailAddress: {
        //                         message: '无效的邮箱地址'
        //                     },
        //                     notEmpty: {
        //                         message: '邮箱地址不能为空'
        //                     }
        //                 }
        //             },
        //             password: {
        //                 validators: {
        //                     different: {
        //                         field: 'username',
        //                         message: '密码不能和用户名一样'
        //                     }
        //                 }
        //             },
        //             confirmPassword: {
        //                 validators: {
        //                     identical: {
        //                         field: 'password',
        //                         message: '密码和确认密码输入不一致'
        //                     }
        //                 }
        //             },
        //         }
        //     })

        .on('success.form.bv', function (e) {

            e.preventDefault();

            var $form = $(e.target);

            var bv = $form.data('bootstrapValidator');

            $.post($form.attr('action'), $form.serialize(), function (result) {
                $('#addEditModal').hide();
                $('#log_info').addClass('bg-primary');
                $('#log_info').css('display', 'block');
                $('#log_info').html(result);
                setTimeout("location.reload()", 1500);
            })
        });

});

function runcase(id){
    // alert($('#run' + id).children("i").attr("class"))
    i_class = $('#run' + id).children("i").attr("class") 
    if(i_class.indexOf("record")>-1){
         // 加入判断,有"变灰"时返回
         return false;
    }
    runcase2(id)
}
/*   执行用例    */
function runcase2(id) {
    // $('#run' + id).attr('disabled', true);
    $('#run' + id + '>i.glyphicon.glyphicon-play-circle').remove();
    $('#run' + id).append('<i class="glyphicon glyphicon-record"></i>');

    $.ajax({
        type: "GET",
        data: {'caseid': id},
        url: "/func/case/run/",
        cache: false,
        dataType: "html",

        success: function (result, TextStatus, xml) {
            // debugger;
            // alert(result);
            // $('#run'+id).attr('disabled',false);
            // $('#run'+id).addClass('green');
            // $('#run'+id).text('Run');
            setTimeout("location.reload()", 500);
        }
    });
}

function runtask(id){
    // alert($('#run' + id).children("i").attr("class"))
    i_class = $('#run' + id).children("i").attr("class") 
    if(i_class.indexOf("record")>-1){
         // 加入判断,有"变灰"时返回
         return false;
    }
    runtask2(id)
}
/*   执行任务    */
function runtask2(id) {
    // alert($('#t-status').children("span").attr("class"))
    // $('#run'+id).attr('disabled',true);
    $('#run' + id).attr('title',"执行中")
    $('#status' + id).children("span").remove();
    $('#status' + id).append('<span ng-if="f.flag==true" class="label label-danger ng-scope">执行中</span>');
    $('#run' + id + '>i.glyphicon.glyphicon-play-circle').remove();
    $('#run' + id).append('<i class="glyphicon glyphicon-record"></i>');

    $.ajax({
        type: "GET",
        data: {'taskid': id},
        url: "/func/task/run/",
        cache: false,
        dataType: "html",

        success: function (result, TextStatus, xml) {
            // debugger;
            // alert(result);
            // $('#run'+id).attr('disabled',false);
            // $('#run'+id).addClass('green');
            // $('#run'+id).text('Run');
            setTimeout("location.reload()", 500);
        }
    });
}

function viewdebuginfo(x) {
    var debuginfo = $('td#' + x + ' pre').text();
    $('#divdebuginfo').text(debuginfo);
}


$("#selprojectid").on("change", function () {
    $('#mdlist').val('');
    $('#selvalue').val('');
});

/*    编辑元素上下移动行    */
function up(obj) {
    var objParentTR = $(obj).parent().parent();
    var prevTR = objParentTR.prev();
    if (prevTR.length > 0) {
        prevTR.insertAfter(objParentTR);
    }
}
function down(obj) {
    var objParentTR = $(obj).parent().parent();
    var nextTR = objParentTR.next();
    if (nextTR.length > 0) {
        nextTR.insertBefore(objParentTR);
    }
}

function goback() {
    window.history.back();
}