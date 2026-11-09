// The cart links are built server side without the user id, because the page
// is rendered before the browser knows who is signed in. This fills it in.

var userId = localStorage.getItem("user_id");

var orderButton = document.getElementById("order-button");
if (orderButton) {
    orderButton.href += "/" + userId;
}

// the script used to look for a delete button that is not on this page, threw
// on it, and left the rest of the file unrun
var links = document.querySelectorAll(".need_id_path");
for (var i = 0; i < links.length; i++) {
    links[i].href += "/" + userId;
}
