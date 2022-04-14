function login(){
    var username= document.getElementById("username").value;
    var password= document.getElementById("password").value;
    let paramsString = "http://users:3302/user/login"
    let searchParams = new URLSearchParams(paramsString);
    searchParams.append("username", username);
    searchParams.append("password", password);
}


function makeBid(){
  var data={"auction_id":4,"user_id":88,"bid_price":100.23}
  fetch(`http://${auction_conf["host"]}:${auction_conf["port"]}/create-new-bid`, {
      mode: 'cors',
      method: 'POST',
      body: data,
  }).then(function(resp) {
      console.log(resp.json());
      return response.json();});