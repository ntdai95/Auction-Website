var username = document.getElementById("username").innerText;
var userId = document.getElementById("user-id").innerText;
var admin = document.getElementById("is-admin").innerText;

if (admin=="True"){
    admin=true;
} else {
    admin=false;
}

myStorage = window.localStorage;
myStorage.setItem('user_name', username);
myStorage.setItem('user_id', userId);
myStorage.setItem('is_admin', admin);

if (admin){
	var url = Flask.url_for('admin', {user_id:userId});	
}
else{
	var url = Flask.url_for('view_participating_auctions', {user_id:userId});
}
window.location.replace(url);

