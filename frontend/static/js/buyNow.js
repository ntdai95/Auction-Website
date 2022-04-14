function pasteUserId(name){
    var el = document.getElementById(name);
    el.value=getUserId();
}

// pasteUserId("user-id");

var link = document.getElementById("buyNow-button");
link.href += "/"+localStorage.getItem("user_id");