var userId = localStorage.getItem("user_id");

var links = document.querySelectorAll('.need_id_path');
for (var i = 0; i < links.length; i++) {
    links[i].href += "/" + userId;
}
