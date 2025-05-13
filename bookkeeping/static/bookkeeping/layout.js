document.addEventListener("DOMContentLoaded", function () {
    //creaate a varable for the buttons
    let btn = document.querySelector('#btn')
    let sidebar = document.querySelector('.sidebar')

btn.addEventListener("click",btnButton)

function btnButton(){
     sidebar.classList.toggle('active')
}
})
