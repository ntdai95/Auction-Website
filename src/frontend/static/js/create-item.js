function pasteUserId(name){
    var el = document.getElementById(name);
    el.value=getUserId();
}

pasteUserId("user-id");