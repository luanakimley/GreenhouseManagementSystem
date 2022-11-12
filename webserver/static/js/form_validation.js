function validateUsername() {
    let uname = document.forms["register"]["username"].value
    if (uname.length > 30) {
        document.getElementById("floatingInputUsername").classList.add("is-invalid");
        document.getElementById("floatingInputUsernameLabel").innerHTML = 'Invalid input - username must be 30 characters or less'
        return false
    }
    else if (uname.length === 0) {
        document.getElementById("floatingInputUsername").classList.add("is-invalid");
        document.getElementById("floatingInputUsernameLabel").innerHTML = 'Invalid input - username must not be empty'
        return false
    }
    else {
        document.getElementById("floatingInputUsername").classList.remove("is-invalid");
        document.getElementById("floatingInputUsernameLabel").innerHTML = 'Username'
        return true
    }
}

function validateEmail() {
    const regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    let email = document.forms["register"]["email"].value
    if (!email.match(regex)) {
        document.getElementById("floatingInputEmail").classList.add("is-invalid");
        document.getElementById("floatingInputEmailLabel").innerHTML = 'Invalid input - email must be valid'
        return false
    } else {
        document.getElementById("floatingInputEmail").classList.remove("is-invalid");
        document.getElementById("floatingInputEmailLabel").innerHTML = 'Email'
        return true
    }
}

function validatePassword() {
    let password = document.forms["register"]["password"].value
    if (password.length < 8) {
        document.getElementById("floatingInputPassword").classList.add("is-invalid");
        document.getElementById("floatingInputPasswordLabel").innerHTML = 'Invalid input - password must be 8 characters or more'
        return false
    }
    else {
        document.getElementById("floatingInputPassword").classList.remove("is-invalid");
        document.getElementById("floatingInputPasswordLabel").innerHTML = 'Password'
        return true
    }
}

function validateConfirmPassword() {
    if (document.forms["register"]["password"].value !== document.forms["register"]["confirm-password"].value) {
        document.getElementById("floatingInputConfirmPassword").classList.add("is-invalid");
        document.getElementById("floatingInputConfirmPasswordLabel").innerHTML = 'Invalid input - password must match'
        return false
    }
    else {
        document.getElementById("floatingInputConfirmPassword").classList.remove("is-invalid");
        document.getElementById("floatingInputConfirmPasswordLabel").innerHTML = 'Confirm password'
        return true
    }
}

function validateRegisterForm() {
    return validateEmail() && validateUsername() && validatePassword() && validateConfirmPassword()
}