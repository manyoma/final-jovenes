function login() {
    let userName = document.getElementById("userName").value
    let password = document.getElementById("password").value

    let name = localStorage.getItem("username")
    let contra = localStorage.getItem("password")
    if (userName == name && password == contra) {
        alert("usuario existente")
        window.location.href="perfil.html"
    } else {
        alert("usuario no existe")
    }
    

  
}
