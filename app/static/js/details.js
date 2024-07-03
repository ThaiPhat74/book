function spinner(status="block") {
    let s = document.getElementsByClassName("spinning")
    for (let i = 0; i < s.length; i++)
        s[i].style.display = status
}

function isEmpty(value){
    return value === null || typeof(value) === 'undefined' || value === ''
}

function addComment(bookId) {
    let cmt = document.getElementById("comment-content")
    if(!isEmpty(cmt.value))
    {
    spinner()
        fetch(`/api/books/${bookId}/comments`, {
            method: "post",
            body: JSON.stringify({
                "content": cmt.value
            }),
            headers: {
                "Content-Type": "application/json"
            }
        }).then((res) => res.json()).then((data) => {
            spinner("none")
           if (data.status === 204) {
                let c = data.comment
                let h = `
                    <li class="list-group-item">
                      <div class="row">
                          <div class="col-md-12 col-sm-12">
                              <p>${c.content}</p>
                              <small>Bình luận <span class="text-info">${moment(c.created_date).locale("vi").fromNow()}
                              </span> bởi <span class="text-info">${c.user.name}</span></small>
                          </div>
                      </div>
                  </li>
                `
                let d = document.getElementById("comments")
                d.innerHTML = h + d.innerHTML;
                cmt.value = ""
           } else
                alert("Lỗi hệ thống!")
        })
    }
    else
        alert("Comment trống")
}
function loadComments(bookId) {
    spinner()
    fetch(`/api/books/${bookId}/comments`).then(res => res.json()).then(data => {
        spinner("none")
        let h = "";
        let c = data.comment
        data.forEach(c => {
            h += `
                <li class="list-group-item">
                  <div class="row">
                      <div class="col-md-12 col-sm-12">
                          <p>${c.content}</p>
                          <small>Bình luận <span class="text-info">${moment(c.created_date).locale("vi").fromNow()}
                          </span> bởi <span class="text-info">${c.user.name}</span></small>
                      </div>
                  </div>
              </li>
            `
        })
                              let d = document.getElementById("comments")
               d.innerHTML = h;
    })
}