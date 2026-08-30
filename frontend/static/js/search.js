myStorage = window.localStorage;
var userId = myStorage.getItem('user_id');

var els = document.querySelectorAll('.need_id');
for (var i=0; i < els.length; i++) {
    els[i].href += userId;
}
