class Card {
    constructor(primary_id, secondary_id, content, src, href, date, username, like, dislike) {
        this.primary_id = primary_id;
        this.secondary_id = `${primary_id}-${secondary_id}`;
        this.parent = document.getElementById(`comments-${primary_id}`);
        this.content = content;
        this.src = src;
        this.href = href;
        this.date = date;
        this.username = username;
        this.like = like;
        this.dislike = dislike;
    }
    header() {
        var container = document.createElement("div");
        container.id = `card-header-${this.secondary_id}`;
        container.className = "card card-header container text-center w-100 color-white";
        container.style.paddingBottom = "25px";
        var d_flex_justified = document.createElement("div");
        d_flex_justified.className = "d-flex justify-content-between";
        var d_flex_left = document.createElement("div");
        d_flex_left.className = "d-flex text-left";
        var d_px1 = document.createElement("div");
        d_px1.className = "d-inline justify-content-between px-2";
        var img = document.createElement("img");
        img.className = "img rounded img-thumbnail";
        img.src = this.src;
        var d_px2 = document.createElement("div");
        d_px2.className = "px-2"
        var a = document.createElement("a");
        a.href = this.href;
        a.innerHTML = this.username;
        var br = document.createElement("br");
        var small = document.createElement("small");
        small.innerHTML = this.date;
        var d_inline = document.createElement("div");
        d_inline.className = "d-inline";
        var btn_update = document.createElement("button");
        btn_update.id = `btn-update-${this.secondary_id}`;
        btn_update.className = "btn btn-outline-secondary mx-1";
        btn_update.innerHTML = "Update";
        var btn_delete = document.createElement("button");
        btn_delete.id = `btn-delete-${this.secondary_id}`;
        btn_delete.className = "btn btn-outline-secondary mx-1";
        btn_delete.innerHTML = "Delete";
        d_px2.append(a);
        d_px2.append(br);
        d_px2.append(small);
        d_px1.append(img);
        d_flex_left.append(d_px1);
        d_flex_left.append(d_px2);
        d_inline.append(btn_update);
        d_inline.append(btn_delete);
        d_flex_justified.append(d_flex_left);
        d_flex_justified.append(d_inline);
        container.append(d_flex_justified);
        this.parent.append(container);
    }
    body() {
        var container = document.createElement("div");
        container.id = `card-body-${this.secondary_id}`;
        container.className = "card-body container text-left border-left border-right";
        var content = document.createElement("p");
        content.id = `content-${this.secondary_id}`
        content.innerHTML = this.content;
        var hidden = document.createElement("div");
        hidden.id = `hidden-${this.secondary_id}`;
        hidden.style.display = "none";
        var input_group = document.createElement("div");
        input_group.className = "input-group mb-3 container rounded mx-auto w-100";
        var textarea = document.createElement("textarea");
        textarea.id = `textarea-${this.secondary_id}-update`;
        textarea.className = "form-control";
        var input_group_append = document.createElement("div");
        input_group_append.className = "input-group-append";
        var btn_save = document.createElement("button");
        btn_save.id = `submit-save-${this.secondary_id}`;
        btn_save.className = "btn btn-outline-secondary";
        btn_save.innerHTML = "Save";
        input_group_append.append(btn_save)
        input_group.append(textarea);
        input_group.append(input_group_append);
        hidden.append(input_group);
        container.append(content);
        container.append(hidden);
        this.parent.append(container);
    }
    footer() {
        var container = document.createElement("div");
        container.id = `card-footer-${this.secondary_id}`;
        container.className = "card card-footer container text-center w-100 mb-2 bg-white";
        container.style.paddingBottom = "25px";
        var text_center = document.createElement("div");
        text_center.className = "text-center w-100";
        for (var i of ["like", "dislike", "reply", "comments"]) {
            var btn = document.createElement("button");
            btn.id = `btn-${i}-${this.secondary_id}`;
            btn.className = "btn btn-link";
            var img = document.createElement("img");
            var filename = images[i];
            img.src = filename;
            img.alt = "";
            var span = document.createElement("span");
            span.id = `span-${i}-${this.secondary_id}`;
            btn.append(img);
            btn.append(span);
            text_center.append(btn);
        }
        var div_reply = document.createElement("div");
        div_reply.id = `reply-${this.secondary_id}`;
        div_reply.className = "collapse hide";
        var input_group = document.createElement("div");
        input_group.className = "input-group mb-3 container rounded mx-auto w-100";
        container.style.paddingTop = "5px";
        var textarea = document.createElement("textarea");
        textarea.id = `textarea-${this.secondary_id}`;
        textarea.className = "form-control";
        var input_group_append = document.createElement("div");
        input_group_append.className = "input-group-append";
        var btn_send = document.createElement("button");
        btn_send.id = `submit-send-${this.secondary_id}`;
        btn_send.className = "btn btn-outline-secondary";
        btn_send.innerHTML = "Send";
        var hidden_value = document.createElement("input");
        hidden_value.id = `hidden-value-${this.secondary_id}`;
        hidden_value.type = "hidden";
        hidden_value.value = ""
        var collapse_hide = document.createElement("div");
        collapse_hide.id = `comments-${this.secondary_id}`;
        collapse_hide.className = "collapse hide";
        input_group_append.append(btn_send)
        input_group.append(textarea);
        input_group.append(input_group_append);
        div_reply.append(input_group);
        text_center.append(div_reply);
        text_center.append(hidden_value);
        text_center.append(collapse_hide);
        container.append(text_center);
        this.parent.append(container);
        for (var i of ["reply", "comments"]) {
            var btn = document.getElementById(`btn-${i}-${this.secondary_id}`);
            btn.setAttribute("data-toggle", "collapse");
            btn.setAttribute("data-target", `#${i}-${this.secondary_id}`);
        }
        add_comment(this.secondary_id);
        update_comment(this.secondary_id, this.primary_id);
        delete_comment(this.secondary_id);
        like_dislike_comment(this.secondary_id, "like", 1);
        like_dislike_comment(this.secondary_id, "dislike", -1);
    }
}

function add_comment(primary_id) {
    document.getElementById(`submit-send-${primary_id}`).onclick = function (e) {
        var form = new FormData();
        form.append("content", document.getElementById(`textarea-${primary_id}`).value);
        form.append("primary_id", primary_id);
        form.append("add", true)
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.status === 200 && (xhr.readyState == XMLHttpRequest.DONE)) {
                var comment = JSON.parse(xhr.responseText);
                document.getElementById(`span-comments-${primary_id}`).innerHTML = `(${comment["total"]})`;
                var card = new Card(
                    primary_id=comment["primary_id"],
                    secondary_id=comment["secondary_id"],
                    content=comment["content"],
                    src=comment["src"],
                    href=comment["href"],
                    date=comment["date"],
                    username=comment["username"],
                    like=comment["likes"],
                    dislike=comment["dislikes"]
                );
                card.header();
                card.body();
                card.footer();
                document.getElementById(`textarea-${comment["primary_id"]}`).value = "";
                document.getElementById(`hidden-value-${comment["primary_id"]}-${comment["secondary_id"]}`).value = comment["hidden_value"];
                document.getElementById(`btn-reply-${comment["primary_id"]}`).click();
            }
        }
        xhr.open("POST", `/article/${title}`, true);
        xhr.send(form);
    }
}


function like_dislike_comment(primary_id, select, value) {
    document.getElementById(`btn-${select}-${primary_id}`).onclick = function (e) {
        var form = new FormData();
        form.append("value", value);
        form.append("primary_id", primary_id);
        form.append("like_dislike", select);
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.status === 200 && (xhr.readyState == XMLHttpRequest.DONE)) {
                var like = JSON.parse(xhr.responseText).like;
                var dislike = JSON.parse(xhr.responseText).dislike;
                for (var i of [[like, "like"], [dislike, "dislike"]]) {
                    if (i[0] == 0) {
                        document.getElementById(`span-${i[1]}-${primary_id}`).innerHTML = "";
                    } else {
                        document.getElementById(`span-${i[1]}-${primary_id}`).innerHTML = "(" + i[0] + ")";
                    }
                }
            }
        }
        xhr.open("POST", `/article/${title}`, true);
        xhr.send(form);
    }
}

function update_comment(primary_id, secondary_id) {
    var active = false;
    var content = document.getElementById(`content-${primary_id}`);
    var hidden = document.getElementById(`hidden-${primary_id}`);
    var hidden_value = document.getElementById(`hidden-value-${primary_id}`);
    var textarea = document.getElementById(`textarea-${primary_id}-update`);
    var btn_update = document.getElementById(`btn-update-${primary_id}`);
    try {
        var btn = document.getElementById(`btn-update-${primary_id}`);
        btn.onclick = function (e) {
            if (active == false) {
                hidden.style.display = "block";
                content.style.display = "none";
                textarea.value = hidden_value.value;
                btn_update.innerHTML = "Cancel";
                active = true;
            } else {
                hidden.style.display = "none";
                content.style.display = "block";
                btn_update.innerHTML = "Update";
                active = false;
            }
        }
        document.getElementById(`submit-save-${primary_id}`).onclick = function (e) {
            var form = new FormData();
            form.append("content", textarea.value);
            form.append("primary_id", primary_id);
            form.append("update", true)
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.status === 200 && (xhr.readyState == XMLHttpRequest.DONE)) {
                    content.innerHTML = JSON.parse(xhr.responseText).content;
                    hidden_value.value = JSON.parse(xhr.responseText).hidden_value;
                    hidden.style.display = "none";
                    content.style.display = "block";
                    btn_update.innerHTML = "Update";
                    active = false;
                }
            }
            xhr.open("POST", `/article/${title}`, true);
            xhr.send(form);
        }
    } catch (error) {
        return;
    }
}

function delete_comment(primary_id) {
    try {
        var btn = document.getElementById(`btn-delete-${primary_id}`);
        btn.onclick = function (e) {
            var form = new FormData();
            form.append("primary_id", primary_id);
            form.append("delete", true)
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.status === 200 && (xhr.readyState == XMLHttpRequest.DONE)) {
                    var primary_id = JSON.parse(xhr.responseText).primary_id;
                    var parent_id = JSON.parse(xhr.responseText).parent_id;
                    var total = JSON.parse(xhr.responseText).total;
                    document.getElementById(`card-header-${primary_id}`).remove();
                    document.getElementById(`card-body-${primary_id}`).remove();
                    document.getElementById(`card-footer-${primary_id}`).remove();
                    if (total == 0) {
                        document.getElementById(`span-comments-${parent_id}`).innerHTML = "";
                    } else {
                        document.getElementById(`span-comments-${parent_id}`).innerHTML = `(${total})`;
                    }

                }
            }
            xhr.open("POST", `/article/${title}`, true);
            xhr.send(form);
        }
    } catch (error) {
        return;
    }
}

function init_card() {
    var div = document.createElement("div");
    div.id = `comments-${title}`;
    document.body.append(div);
    var card = new Card(
        primary_id=title,
        secondary_id="secondary",
        content="",
        src="",
        href="",
        date="",
        username="",
        like="",
        dislike=""

    );
    card.footer();
}

function create_card(primary_id, comment) {
    var card = new Card(
        primary_id=primary_id,
        secondary_id=comment.id,
        content=comment["content"],
        src=comment["src"],
        href=comment["href"],
        date=comment["date"],
        username=comment["username"],
        like=comment["likes"],
        dislike=comment["dislikes"]
    );
    card.header();
    card.body();
    card.footer();
    document.getElementById(`hidden-value-${primary_id}-${comment['id']}`).value = comment["hidden_value"];
    if (comment["likes"] > 0) {
        document.getElementById(`span-like-${primary_id}-${comment['id']}`).innerHTML = `(${comment["likes"]})`;
    }
    if (comment["dislikes"] > 0) {
        document.getElementById(`span-dislike-${primary_id}-${comment['id']}`).innerHTML = `(${comment["dislikes"]})`;
    }
    if (comment["username"] != comment["current_user"]) {
        document.getElementById(`btn-update-${primary_id}-${comment['id']}`).style.display = "none";
        document.getElementById(`btn-delete-${primary_id}-${comment['id']}`).style.display = "none";
    }
}

function recursively_init_comments(obj, primary_id) {
    if (obj.length > 0) {
        document.getElementById(`span-comments-${primary_id}`).innerHTML = `(${obj.length})`;
    }
    for (var child of obj) {
        create_card(primary_id=primary_id, comment=child);
        if (child["children"].length > 0) {
            recursively_init_comments(child["children"], `${primary_id}-${child.id}`);
        }
    }
}

function article_stats() {
    if (article_like_count > 0) {
        document.getElementById(`span-like-${title}-secondary`).innerHTML = `(${article_like_count})`;
    }
    if (article_dislike_count > 0) {
        document.getElementById(`span-dislike-${title}-secondary`).innerHTML = `(${article_dislike_count})`;
    }
}

function init_comments() {
    var form = new FormData();
    form.append("comments", true)
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.status === 200 && (xhr.readyState == XMLHttpRequest.DONE)) {
            var comments = JSON.parse(xhr.responseText);
            if (comments.length > 0) {
                recursively_init_comments(comments, `${title}-secondary`)
            }
            article_stats(comments);
        }
    }
    xhr.open("POST", `/article/${title}`, true);
    xhr.send(form);
}

function search_article() {
    document.getElementById("search-article").onkeypress = function (e) {
        if (e.key == "Enter") {
            var title = document.getElementById("search-article").value;
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == XMLHttpRequest.DONE) {
                    if (xhr.status != 404) {
                        window.location.replace(`/article/${title}`);
                    } else {
                        alert(`No article found!`);
                    }
                }
            }
            xhr.open("GET", `/article/${title}`);
            xhr.send();
        }
    }
}
