// const addUser = document.querySelector('#add-user')

// addUser.addEventListener('onclick', function(){
//     window.location.href='create_user.html'
// })

const listContainer = document.querySelector(".list-container")
const body = document.querySelector('body')

function data(e) {
    console.log(e)
}

// listContainer.addEventListener('click', data)


listContainer.addEventListener('click', function(e){
    if (e.target.nodeName === 'LI'){
        sessionStorage.setItem("name", JSON.stringify(e.target.innerText))
        let name = sessionStorage.getItem("name")
        console.log(e.target.innerText)
        console.log(name)
    }
})

// body.addEventListener('click', function(){
//     console.log('testing')
// })