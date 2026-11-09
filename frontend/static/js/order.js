// The complete button is rendered without the user id, so it is filled in here.

var completeButton = document.getElementById("complete-button");
if (completeButton) {
    completeButton.href += "/" + localStorage.getItem("user_id");
}
