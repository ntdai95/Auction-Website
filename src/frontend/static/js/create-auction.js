var date = new Date(); //create date object var 
min_date = date.toISOString().slice(0,10);
var currentTime = date.toISOString().substring(11,16);
// min_date = Date.now();
var auctionStartDate = document.getElementById("start");
var auctionStartTime = document.getElementById("start-time");

auctionStartDate.min=date.toISOString().slice(0,10);
auctionStartDate.value=date.toISOString().slice(0,10);
auctionStartTime.value=currentTime;




var auctionEndDate = document.getElementById("end");
var auctionEndTime = document.getElementById("end-time");
date.setDate(date.getDate()+1);
auctionEndDate.min=date.toISOString().slice(0,10);
auctionEndDate.value=date.toISOString().slice(0,10);
auctionEndTime.value=currentTime;

var user = document.getElementById("input-user-id");
user.value=getUserId();