const loginForm = document.getElementById('login-form')
const baseEndpoint = "http://localhost:8000/api"
const contentContainer = document.getElementById('content-container')

//search
const searchForm = document.getElementById('search-form')


if (loginForm) {
    // handle this login form
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm) {
    searchForm.addEventListener('submit', handleSearch)
}

function handleLogin(event) {
    console.log(event)
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr =  JSON.stringify(loginObjectData)
    const options = {
        "method":"POST",
        headers:{
            "Content-Type":"application/json",
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options).then(response=>{
        console.log(response) //Promise
        return response.json()
    })// request.POST
    .then(authData => {
        handleAuthData(authData, getProductList)
    })
    .catch(err=>{
        console.log('err',err)
    })
}

function handleSearch(event) {
    console.log(event)
    event.preventDefault()
    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/search/?${searchParams}`
    const headers ={
        "Content-Type": "application/json",
    }
    const authToken = localStorage.getItem('access') 
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`
    }

    const options = {
        method: "GET",
        headers: headers,

    }
    fetch(endpoint, options).then(response=>{
        //Promise
        return response.json()
    })// request.POST
    .then(data => {
        const validData = isTokenNotValid(data)
        if (validData && contentContainer){
            contentContainer.innerHTML = ""
            if (data && data.hits) {
                let htmlStr = ""
                for (let result of data.hits){
                    htmlStr += "<li>" + result.title + "</li>"
                }
                contentContainer.innerHTML = htmlStr
                if (data.hits.length === 0 ){
                    contentContainer.innerHTML = "<p> No Result Found </p>"
                }
            } else {
                contentContainer.innerHTML = "<p> No Result Found </p>"
            }
        }
    })
    .catch(err=>{
        console.log('err',err)
    })
}

function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh',authData.refresh)

    if (callback) {
        callback()
    }
}

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"
    }
}

function getFetchOptions(method, body){
    return {
        method: method === null ? "GET" : method,
        headers: {
            "Content-Type":"application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body : body ? body : null
    }
}

function isTokenNotValid(jsonData) {
    if(jsonData.code && jsonData.code === "token_not_valid") {
        // run a refresh token fetch
        alert("Please login again")
        return false
    }
    return true
}

function validateJWTToken(){
    //fetch
    const endpoint = `${baseEndpoint}/token/verify/`
    const options = {
        method: "POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            token: localStorage.getItem('access')
        })
    }
    fetch(endpoint, options)
    .then(response=>response.json())
    .then(x=> {
        //refresh token
    })
}


function getProductList(){
    const endpoint = `${baseEndpoint}/products/`
    const options = getFetchOptions()
    fetch(endpoint, options)
    .then(response=>{
        console.log(response)
        return response.json()
    })
    .then(data=> {
        const validData = isTokenNotValid(data)
        if (validData) {
            writeToContainer(data)
        }
    })
}



//getProductList()
validateJWTToken()

// algolia search

const searchClient = algoliasearch('D1PLQ1RXD5', '8126841eb1897d05da1a6278e151db13');

const search = instantsearch({
  indexName: 'home_Product',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

  instantsearch.widgets.clearRefinements({
    container: '#clear-refinements',
  }),
  

  instantsearch.widgets.refinementList({
    container: '#user-list',
    attribute: 'user'
  }),

  instantsearch.widgets.refinementList({
    container: '#public-list',
    attribute: 'public'
  }),

  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
        item: `
        <div>
        <h1>{{#helpers.highlight}}{"attribute":"title"}{{/helpers.highlight}}</h1>
        <br>
        <h4>{{#helpers.highlight}}{"attribute":"content"}{{/helpers.highlight}}</h4>
        <p>{{ user }}</p> 
        <p>\${{ price }} </p> 
        </div>
        `
    }
  })
]);

search.start();
