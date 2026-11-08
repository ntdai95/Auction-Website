// setting up storage

var myStorage = window.localStorage;

// creating identity functions

function getUserId(){
    return myStorage.getItem("user_id");
}
function getUserName(){
    return myStorage.getItem("user_name");
}

// localStorage returns a string, so a non-admin stored as false arrives here
// as "false", which is truthy. Compare against the text instead.
function isAdmin(){
    return myStorage.getItem("is_admin") === "true";
}

// setting up user specific items

var userDisplay = document.getElementById("user-disp");
if (userDisplay){
    // signed out there is nothing in storage, and "null | null" looked like a
    // bug sitting in the navigation bar
    if (getUserName()){
        userDisplay.innerText=getUserName()+" (#"+getUserId()+")";
    } else {
        userDisplay.innerText="";
    }
}

// links requiring user information

var myAuctionsLink =document.getElementById("my-auctions-link");
var myItemsLink =document.getElementById("my-items-link");
var activeAuctions =document.getElementById("active-auctions-link");
var cartLink =document.getElementById("cart-link");
var settingsLink =document.getElementById("settings-link");
var watchlistLink =document.getElementById("watchlist-link");
var logoutLink =document.getElementById("logout-link");

if (myAuctionsLink) myAuctionsLink.href=Flask.url_for('my_auctions', {user_id:getUserId()});
if (myItemsLink) myItemsLink.href=Flask.url_for('my_items', {user_id:getUserId()});
if (activeAuctions) activeAuctions.href=Flask.url_for('view_participating_auctions', {user_id:getUserId()});
if (settingsLink) settingsLink.href=Flask.url_for('settings', {user_id:getUserId()});
if (cartLink) cartLink.href=Flask.url_for('cart', {user_id:getUserId()});
// the navigation bar had a watchlist entry that was never given a link
if (watchlistLink) watchlistLink.href=Flask.url_for('watchlist', {user_id:getUserId()});
// logging out only redirected, so the identity stayed in storage and the next
// page still treated the visitor as signed in
if (logoutLink){
    logoutLink.href=Flask.url_for('logout');
    logoutLink.addEventListener("click", function(){
        myStorage.removeItem("user_name");
        myStorage.removeItem("user_id");
        myStorage.removeItem("is_admin");
    });
}

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
