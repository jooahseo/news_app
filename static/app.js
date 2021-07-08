// ************ carousel ************
let items = document.querySelectorAll('.carousel .carousel-item')

items.forEach((el) => {
    const minPerSlide = 4
    let next = el.nextElementSibling
    for (var i=1; i<minPerSlide; i++) {
        if (!next) {
            // wrap carousel by using first child
        	next = items[0]
      	}
        let cloneChild = next.cloneNode(true)
        el.appendChild(cloneChild.children[0])
        next = next.nextElementSibling
    }
})

// *********** request to server ***********

const cards = document.querySelectorAll('.news_card')

for(let i=0; i<cards.length; i++){
    cards[i].addEventListener("click", function(e){
        e.preventDefault();
        if(e.target.tagName === "BUTTON"){
            if(e.target.disabled){ //button disabled (it's already saved)
                e.target.disabled = false;
                removeNewsMain(e)
            }else{
                e.target.disabled= true;
                saveNewsMain(e)
            }

            // console.log('image url', e.target.nextElementSibling.src)
            // console.log('url', e.target.nextElementSibling.nextElementSibling.children[3].href)
            // console.log('title',e.target.nextElementSibling.nextElementSibling.children[0].innerHTML)
            // console.log('description',e.target.nextElementSibling.nextElementSibling.children[2].innerHTML)
            // console.log('date time',e.target.nextElementSibling.nextElementSibling.children[1].innerHTML)
        }
    })
}

const searchNews = document.querySelectorAll('.search_news')

for(let i=0; i< searchNews.length; i++){
    searchNews[i].addEventListener("click", function(e){
        e.preventDefault()
        if(e.target.tagName === "BUTTON"){
            console.log('image url', e.target.nextElementSibling.children[0].children[0].src)
            console.log('title', e.target.nextElementSibling.children[1].children[0].children[0].innerHTML)
            console.log('description', e.target.nextElementSibling.children[1].children[0].children[1].innerHTML)
            console.log('url', e.target.nextElementSibling.children[1].children[0].children[3].href)
            console.log('date time',e.target.nextElementSibling.children[1].children[0].children[2].innerHTML)
        }
    })
}

async function saveNewsMain(e){
    e.preventDefault()
    const cardBody = e.target.nextElementSibling.nextElementSibling;

    const url = cardBody.children[3].href;
    const title = cardBody.children[0].innerHTML;
    const description = cardBody.children[2].innerHTML;
    const date = cardBody.children[1].innerHTML;
    const image = e.target.nextElementSibling.src;

    res = await axios.post('/save-news', {url, title, description, date, image})
    console.log(res)
    if(res.data.result){
        e.target.className += "deactivated"
    }
}

async function removeNewsMain(e){
    
}