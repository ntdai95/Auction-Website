// setting up storage

myStorage = window.localStorage;

// creating identity functions

function getUserId(){
    return myStorage.getItem("user_id");
}
function getUserName(){
    return myStorage.getItem("user_name");
}

function isAdmin(){
    return myStorage.getItem("is_admin");
}

// setting up user specific items

var userdip = document.getElementById("user-disp");
if (userdip){
    userdip.innerText=getUserName()+"|"+getUserId();
}

// links requiring user information

var myAuctionsLink =document.getElementById("my-auctions-link");
var myItemsLink =document.getElementById("my-items-link");
var activeAuctions =document.getElementById("active-auctions-link");
var cartLink =document.getElementById("cart-link");
var settingsLink =document.getElementById("settings-link");
var logoutLink =document.getElementById("logout-link");

if (myAuctionsLink) myAuctionsLink.href=Flask.url_for('my_auctions', {user_id:getUserId()});
if (myItemsLink) myItemsLink.href=Flask.url_for('my_items', {user_id:getUserId()});
if (activeAuctions) activeAuctions.href=Flask.url_for('view_participating_auctions', {user_id:getUserId()});
if (settingsLink) settingsLink.href=Flask.url_for('settings', {user_id:getUserId()});
if (cartLink) cartLink.href=Flask.url_for('cart', {user_id:getUserId()});
if (logoutLink) logoutLink.href=Flask.url_for('logout');

var adminLink = document.getElementById('admin-link');

if (adminLink){
    if (isAdmin()){
        adminLink.style.display="block";
    } else {
        adminLink.style.display="none";
    }
}

function pasteUserId(name){
    var el = document.getElementById(name);
    el.value=getUserId();
}
