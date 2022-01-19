// setting up storage

myStorage = window.localStorage;
// myStorage.setItem('user_name', 'eugene');
// myStorage.setItem('user_id', '200');
// myStorage.setItem('is_admin', 'true');


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

console.log(getUserId());
console.log(getUserName());
console.log(isAdmin());

// setting up user specific items

var userdip  = document.getElementById("user-disp");
userdip.innerText=getUserName()+"|"+getUserId();

// links requiring user information

var myAuctionsLink =document.getElementById("my-auctions-link");
var myItemsLink =document.getElementById("my-items-link");
var activeAuctions =document.getElementById("active-auctions-link");
var cartLink =document.getElementById("cart-link");
var settingsLink =document.getElementById("settings-link");
var logoutLink =document.getElementById("logout-link");

myAuctionsLink.href=Flask.url_for('my_auctions', {user_id:getUserId()});
myItemsLink.href=Flask.url_for('my_items', {user_id:getUserId()});
activeAuctions.href=Flask.url_for('view_participating_auctions', {user_id:getUserId()});
settingsLink.href=Flask.url_for('settings', {user_id:getUserId()});
cartLink.href=Flask.url_for('cart', {user_id:getUserId()});
logoutLink.href=Flask.url_for('logout');

var adminLink = document.getElementById('admin-link');

if (isAdmin()){
    adminLink.style.display="block";
} else {
    adminLink.style.display="none";
}


// // Setting user id
// var userId =document.getElementById("user-id");
// userId.value=getUserId();

function pasteUserId(name){
    var el = document.getElementById(name);
    el.value=getUserId();
}


auction_host="auctions"
auction_port="3308"



function makeBid(){
    var bid=document.getElementById("bid").value;
    var user_id=getUserId();
    var auction_id=document.getElementById("auction_id").value;
    var data={"auction_id":auction_id,"user_id":user_id,"bid_price":bid}
    fetch(`http://${auction_host}:${auction_port}/create-new-bid`, {
    // fetch(`/create-new-bid`, {
        mode: 'cors',
        method: 'POST',
        body: data,
    }).then(function(resp) {
        console.log(resp.json());
        return response.json();})
    .then(data => {return data});
}

//   const FD = new FormData( form );

function deleteItem(a){
    fetch('http://localhost:5003/delete', {
    method: 'POST',
    body: {"user_id": "asdas"}
}).then(response => response.json())
  .then((x)=>console.log(x))
}

function markInapp(item_id,id){
    fetch('http://localhost:5003/item/inappropriate');
    console.log(item_id,id);
    var flag = document.getElementById(id);
    flag.innerText="Marked as inappropriate";

}