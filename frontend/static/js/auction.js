var adminDiv = document.getElementById("admin-console");
if (localStorage.getItem("is_admin")){
    adminDiv.style.display="block";
}