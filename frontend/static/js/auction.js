var adminDiv = document.getElementById("admin-console");
if (adminDiv && localStorage.getItem("is_admin")){
    adminDiv.style.display="block";
}
