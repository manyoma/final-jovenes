function registerUser(){
let name=document.getElementById("name").value
let lastname=document.getElementById("last name").value
let phone=document.getElementById("phone").value
let username=document.getElementById("userName").value
let password=document.getElementById("password").value
let repeat=document.getElementById("repeat").value

if(password==repeat){
    alert("las contraseñas coiciden")
    localStorage.setItem("name",name)
    localStorage.setItem("lastname",lastname)
    localStorage.setItem("phone",phone)
    localStorage.setItem("username",username)
    localStorage.setItem("password",password)
    localStorage.setItem("repeat",repeat)
}else{
    alert("las contraseñas no coiciden")
}


}