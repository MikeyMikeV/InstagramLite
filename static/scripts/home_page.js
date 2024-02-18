console.log('Sanity check');

let homepageLikeButtons = document.getElementsByName('homepage_like')

for (let index = 0; index < homepageLikeButtons.length; index++) {
    const element = homepageLikeButtons[index];
    element.style.cursor = 'pointer';
    element.onclick = function () {
        postSocket.send(JSON.stringify(
            {
                'type':'homepage_like',
                'post_id':element.id.split('_')[2],
            }
        ));
        let elementImg = element.getElementsByTagName('img')[0]
        let elementCounter = element.getElementsByTagName('p')[0]
        if (element.className=='homepage_like_0'){
            elementImg.src = '/static/images/SVG/red-heart-icon.svg'
            element.className="homepage_like_1"
            elementCounter.innerHTML = parseInt(elementCounter.innerHTML) + 1
        }
        else{
            elementImg.src = '/static/images/SVG/heart-thin-icon.svg'
            element.className="homepage_like_0"
            elementCounter.innerHTML = parseInt(elementCounter.innerHTML) - 1
        }
    }
}

const profileID = JSON.parse(document.getElementById('profileID').textContent);
console.log(profileID)
let postSocket = null

function connect() {
    postSocket = new WebSocket('ws://'+window.location.host+'/ws/homepage/'+profileID+'/')
    
    postSocket.onopen = function (e) {
        console.log('Successfully connected to the WebSocket.')
    }

    postSocket.onclose = function (e){
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    }
}

if (profileID != '') {
    connect();
}