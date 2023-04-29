document.addEventListener('DOMContentLoaded', function(){

    var passwordInput = document.getElementById("password")
    var eye = document.getElementById("eye")
    eye.addEventListener("click", function(){
        this.classList.toggle("fa-eye-slash")
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password"
        passwordInput.setAttribute("type", type)
    });
});