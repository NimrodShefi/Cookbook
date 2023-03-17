function change_password_form_visibility() {
    form = document.getElementById("change_password");
    btn = document.getElementById("change_password_btn");
    if (form.style.display === "none") {
        form.style.display = "block";
        btn.innerHTML = "Hide Form";
    } else {
        form.style.display = "none";
        btn.innerHTML = "Change Password";
    }
}