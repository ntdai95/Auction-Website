

myStorage = window.localStorage;
myStorage.setItem('user_name', username);
myStorage.setItem('user_id', userId);
var userId = myStorage.getItem('user_id');
console.log(userId);

var addwatchbutton =document.getElementById("add-watch-button");
var removewatchbutton =document.getElementById("remove-watch-button");
addwatchbutton.href = addwatchbutton.href + myStorage.getItem('user_id');
removewatchbutton.href = removewatchbutton.href + myStorage.getItem('user_id');

var els = document.querySelectorAll('.need_id');
for (var i=0; i < els.length; i++) {
    els[i].href += myStorage.getItem('user_id');
}

window.location.replace(url);

