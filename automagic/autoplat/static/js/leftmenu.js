/**
 * add by yansl@wondershare.cn 2018-12-29
 */

/*    点击切换菜单    */
function menuClick(){
    if($(this).parent().find('dd').is(":hidden")){
       $(this).parent().find('dd').show();
    }else{
       $(this).parent().find('dd').hide();     //如果元素为显现,则将其隐藏
    }
}


