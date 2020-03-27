function initProductSelect() {
  $.ajax({
    type: "GET",
    url: "/setting/get/product/",
    cache: false,
    dataType: 'json',
    async: false,
    success: function (result, TextStatus) {
      let option_str = '<option value="0">所属产品</option>'
      let api_selproductid = $('#api-selproductid')

      // let api_selproductid = $('#api-selproductid')

      if (result.length > 0) {
        for (i = 0; i < result.length; i++) {
          option_str += ('<option value="' + result[i].key + '">' + result[i].value + '</option>');
        }
      }
      api_selproductid.empty()
      api_selproductid.append(option_str)
    }
  });
}

function initProjectSelect() {
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
      initModuleSelect()
    }
  });
}

function initModuleSelect(){
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
                  projectItem.append('<option value="' + result[i].key + '">' + result[i].value + '</option>');
              }
          }
      }
  })
}

initProductSelect()



$('#api-selproductid').bind('change',initProjectSelect)
