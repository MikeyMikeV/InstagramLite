console.log('Sanity check');

const postID = JSON.parse(document.getElementById('postID').textContent);

let commentInput = document.getElementById('commentInput')
let commentSend = document.getElementById('commentSend')
let commentList = document.getElementById('comment_list')
let postLike = document.getElementById('postLike')
let postLikeCounter = document.getElementById('post_like_counter')
let commentLikeButtons = document.getElementsByName('comment_like')
let commentReplyButtons = document.getElementsByName('comment_reply')

commentInput.onkeyup = function(e){
    if (e.keyCode === 13){
        commentSend.click()
    }
}

commentSend.onclick = function(){
    if (commentInput.value.length === 0) return;
    postSocket.send(JSON.stringify(
        {
            'type':'comment',
            'text':commentInput.value,
        }
    ));
    commentInput.value='';
};

postLike.onclick = function(){
    postSocket.send(JSON.stringify(
        {
            'type': 'post_like'
        }
    ))
    if (postLike.className=='post_like0'){
        postLike.src = '/static/images/SVG/red-heart-icon.svg'
        postLike.className="post_like1"
        postLikeCounter.innerHTML = parseInt(postLikeCounter.innerHTML) + 1
    }
    else{
        postLike.src = '/static/images/SVG/heart-thin-icon.svg'
        postLike.className="post_like0"
        postLikeCounter.innerHTML = parseInt(postLikeCounter.innerHTML) - 1
    }
};

for (let index = 0; index < commentLikeButtons.length; index++) {
    const element = commentLikeButtons[index];
    element.style.cursor = 'pointer';
    element.onclick = function () {
        postSocket.send(JSON.stringify(
            {
                'type':'comment_like',
                'comment_id':element.id.split('_')[2],
            }
        ));
        let elementImg = element.getElementsByTagName('img')[0]
        let elementCounter = element.getElementsByTagName('p')[0]
        if (element.className=='comment_like_0'){
            elementImg.src = '/static/images/SVG/red-heart-icon.svg'
            element.className="comment_like_1"
            elementCounter.innerHTML = parseInt(elementCounter.innerHTML) + 1
        }
        else{
            elementImg.src = '/static/images/SVG/heart-thin-icon.svg'
            element.className="comment_like_0"
            elementCounter.innerHTML = parseInt(elementCounter.innerHTML) - 1
        }
    }
}

for (let index = 0; index < commentReplyButtons.length; index++) {
    const element = commentReplyButtons[index];
    element.style.cursor = 'pointer';
    element.onclick = function () {
        postSocket.send(JSON.stringify(
            {
                'type':'reply_to',
                'profile_id':element.id.split('_')[2],
            }
        ));
        console.log(element.id.split('_')[2])
    }
}

let postSocket = null

function connect() {
    postSocket = new WebSocket('ws://'+window.location.host+'/ws/post/'+postID+'/')
    
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

    postSocket.onmessage = function (e) {
        const data = JSON.parse(e.data)
        // console.log(data)
        switch (data['type']) {
            case 'comment':
                const comment = document.createElement('div')
                comment.className = 'comment_card'
                comment.id = "comment_"+data['comment_id']
                    const top = document.createElement('div')
                    top.className = 'top'
                        const com_pp = document.createElement('div')
                        com_pp.className = 'com_pp'
                            const img1 = document.createElement('img')
                            img1.src = '/media/'+data['profile_pic']
                            com_pp.appendChild(img1)
                        top.appendChild(com_pp)
                        const com_name = document.createElement('div')
                        com_name.className = 'com_name'
                            const p1 = document.createElement('p')
                            p1.innerHTML = data['profile']
                            com_name.appendChild(p1)
                        top.appendChild(com_name)
                        const com_edit = document.createElement('div')
                        top.appendChild(com_edit)
                    comment.appendChild(top)

                    const middle = document.createElement('div')
                    middle.className = 'middle'
                        const text = document.createElement('div')
                        text.className = 'text'
                        text.innerHTML = data['text']
                        middle.appendChild(text)
                    comment.appendChild(middle)

                    const bottom = document.createElement('div')
                    bottom.className = 'bottom'
                        const com_timestamp = document.createElement('div')
                        com_timestamp.className = 'com_timestamp'
                        // com_timestamp.value = data['time_stamp']
                        bottom.appendChild(com_timestamp)
                        const com_bar = document.createElement('div')
                        com_bar.className = 'com_bar'
                            const com_reply = document.createElement('div')
                            com_reply.className = 'com_reply'
                            //TODO - добавить функции клика для ответов
                            com_bar.appendChild(com_reply)
                            const com_like = document.createElement('div')
                            com_like.className = 'com_like'
                            //TODO - добавить функции клика для лайков
                            com_bar.appendChild(com_like)
                        bottom.appendChild(com_bar)
                    comment.appendChild(bottom)
                commentList.prepend(comment)
                console.log(commentList.childNodes)
                break;
            case 'reply_to':
                commentInput.id = data['profile_id']
                commentInput.value = '@'+data['profile_tag']
                commentInput.focus()
            default:
                console.error("Unknown message type!");
                break;
        }
    }

    postSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        postSocket.close();
    }
}

connect();