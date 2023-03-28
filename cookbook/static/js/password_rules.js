document.addEventListener('DOMContentLoaded', function(){
    const password_input = document.getElementById("password");

    password_input.addEventListener('input', check_password)
    
    function check_password() {
        var password_value = password_input.value;
    
        var rule_length = document.getElementById("rule1");
        var rule_uppercase = document.getElementById("rule2");
        var rule_lowercase = document.getElementById("rule3");
        var rule_number = document.getElementById("rule4");
        var rule_special_char = document.getElementById("rule5");
    
        if (password_value.length >= 8) {
            rule_length.style.color = 'green';
        } else {
            rule_length.style.color = 'red';
        }
    
        if (/[A-Z]/.test(password_value)) {
            rule_uppercase.style.color = 'green';
        } else {
            rule_uppercase.style.color = 'red';
        }
    
        if (/[a-z]/.test(password_value)) {
            rule_lowercase.style.color = 'green';
        } else {
            rule_lowercase.style.color = 'red';
        }
    
        if (/[1-9]/.test(password_value)) {
            rule_number.style.color = 'green';
        } else {
            rule_number.style.color = 'red';
        }
    
        if (/[!@#$%^&*()]/.test(password_value)) {
            rule_special_char.style.color = 'green';
        } else {
            rule_special_char.style.color = 'red';
        }
        
    }
})
