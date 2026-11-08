// localStorage always returns a string, so a non-admin stored as false comes
// back as "false", which is truthy. Compare against the text instead.
var adminDiv = document.getElementById("admin-console");
if (adminDiv && localStorage.getItem("is_admin") === "true"){
    adminDiv.style.display="block";
}
