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
        container.className = "card card-footer text-center bg-dark border border-secondary mt-4";
        container.style.paddingBottom = "25px";
        var d_flex_justified = document.createElement("div");
        d_flex_justified.className = "d-flex justify-content-between";
        var d_flex_left = document.createElement("div");
        d_flex_left.className = "d-flex text-left";
        var d_px1 = document.createElement("div");
        d_px1.className = "d-inline justify-content-between px-2";
        var img = document.createElement("img");
        img.className = "img rounded img";
        img.src = this.src;
        var d_px2 = document.createElement("div");
        d_px2.className = "px-2"
        var a = document.createElement("a");
        a.href = this.href;
        a.innerHTML = this.username;
        var br = document.createElement("br");
        var small = document.createElement("small");
        small.innerHTML = this.date;
        small.className = "text-light";
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
        container.className = "card-body text-left text-light";
        container.style.backgroundColor = "black";
        container.style.overflow = "auto";
        container.style.height = "20rem";
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
        textarea.className = "form-control bg-dark border-secondary text-light";
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
        if (this.secondary_id == `${this.primary_id}-secondary`) {
            container.className = "card card-footer text-center bg-dark border-dark";
        } else {
            container.className = "card card-footer text-center bg-dark border-bottom border-left border-right border-secondary";
        }
        container.style.paddingBottom = "25px";
        var text_center = document.createElement("div");
        text_center.id = `text-center-${this.secondary_id}`;
        text_center.className = "text-center w-100";
        for (var i of ["like", "dislike", "reply", "comments"]) {
            var btn = document.createElement("button");
            btn.id = `btn-${i}-${this.secondary_id}`;
            btn.className = "btn btn-link";
            btn.style.width = "5rem";
            var img = document.createElement("img");
            var filename = images[i];
            img.src = filename;
            img.alt = "";
            var span = document.createElement("span");
            span.id = `span-${i}-${this.secondary_id}`;
            span.className = "badge badge-dark text-secondary";
            span.onmouseover = function() {
                this.className += " text-light";
            }
            span.onmouseleave = function() {
                this.className = this.className.replace(" text-light", "");
            }
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
        textarea.className = "form-control bg-dark border-secondary text-light";
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

class Article {
    constructor(id, parent, title, article_img, article_href, date, author_img, author_href, author_name, recent) {
        this.id = id;
        this.title = title;
        this.author_img = author_img;
        this.author_href = author_href;
        this.article_img = article_img;
        this.article_href = article_href;
        this.author_name = author_name;
        this.date = date;
        this.article = document.createElement("article");
        this.parent = parent;
        this.recent = recent;
    }
    init() {
        this.article.setAttribute("class", "container rounded w-100 bg-dark border border-secondary my-4 col-sm");
        var recent = this.recent;
        var className = this.className;
        function query(media, article_) {
            if (media.matches) {
                article_.className += recent ? "-2" : "-2";
            } else {
                article_.className += recent ? "-8" : "";
            }
        }
        var media = window.matchMedia("(max-width: 600px)")
        query(media, this.article)
        media.addListener((e) => { query(e, this.article); });
        this.header();
        this.body();
        this.footer();
        this.parent.append(this.article);
    }
    header() {
        var main = document.createElement("div");
        main.setAttribute("class", "article-group");
        var justified = document.createElement("div");
        justified.setAttribute("class", "justify-content-between");
        var d_inline = document.createElement("div");
        d_inline.setAttribute("class", "d-inline");
        var div_img = document.createElement("div");
        div_img.setAttribute("class", "article-author-info");
        var author_img = document.createElement("img");
        author_img.setAttribute("class", "img rounded");
        author_img.setAttribute("width", 40);
        author_img.setAttribute("height", 40);
        author_img.setAttribute("src", this.author_img);
        div_img.append(author_img);
        var div_url = document.createElement("div");
        div_url.setAttribute("class", "article-author-info px-1");
        var author_url = document.createElement("a");
        author_url.setAttribute("href", this.author_href);
        author_url.innerHTML = this.author_name;
        author_url.style.fontSize = "12px";
        var br = document.createElement("br");
        var small = document.createElement("small");
        small.setAttribute("class", "text-secondary");
        small.innerHTML = this.date;
        div_url.append(author_url);
        div_url.append(br);
        div_url.append(small);
        d_inline.append(div_img);
        d_inline.append(div_url);
        justified.append(d_inline);
        main.append(justified);
        this.article.append(main);
    }
    body() {
        var main = document.createElement("div");
        main.setAttribute("class", "article-group");
        var a = document.createElement("a");
        a.setAttribute("href", this.article_href);
        var img = document.createElement("img");
        img.setAttribute("width", "100%");
        var recent = this.recent;
        function query(media) {
            if (media.matches) {
                img.setAttribute("height", "100vw");
            } else {
                img.setAttribute("height", recent ? "300vw": "100vw");
            }
        }
        var media = window.matchMedia("(max-width: 600px)")
        query(media)
        media.addListener(query)
        img.setAttribute("class", " d-flex rounded");
        img.setAttribute("src", this.article_img);
        a.append(img);
        main.append(a);
        this.article.append(main);
    }
    footer() {
        var main = document.createElement("div");
        main.setAttribute("class", "article-group");
        var a = document.createElement("a");
        a.setAttribute("class", "article-group-link");
        a.setAttribute("href", this.article_href);
        for (var i of [["h4", "#000000", this.title]]) {
            var item = document.createElement(i[0]);
            item.setAttribute("class", "article-more p-1");
            item.style.color = i[1];
            item.style.fontSize = "12px";
            item.innerHTML = i[2];
            a.append(item);
        }
        main.append(a);
        this.article.append(main);
    }
}

class Carousel {
    constructor(id, articles, parent, href, innerHTML) {
        this.id = id;
        this.articles = articles;
        this.parent = parent;
        this.href = href;
        this.innerHTML = innerHTML;
    }
    init() {
        var div = document.createElement("div");
        var d_inline = document.createElement("div");
        d_inline.setAttribute("class", "d-inline justify-content-center col");
        function query(media) {
            if (media.matches) {
                div.setAttribute("class", "container justify-content-center align-self-center w-75");
            } else {
                div.setAttribute("class", "container justify-content-center align-self-center w-50");
            }
        }
        var media = window.matchMedia("(max-width: 600px)")
        query(media)
        media.addListener(query)
        var carousel = document.createElement("div");
        carousel.id = this.id;
        carousel.setAttribute("class", "carousel slide");
        carousel.setAttribute("data-ride", "carousel");
        var indicators = document.createElement("ol");
        indicators.setAttribute("class", "carousel-indicators")
        var inner = document.createElement("div");
        inner.setAttribute("class", "carousel-inner px-4");
        var length = this.articles.length;
        for (var i = 0; i < length; i++) {
            var indicator = document.createElement("li");
            indicator.setAttribute("data-target", `#{this.id}`);
            indicator.setAttribute("data-slide-to", `${i}`);
            var item = document.createElement("div");
            item.id = `item${i}`;
            item.setAttribute("class", "carousel-item col-sm");
            if (i == 0) {
                indicator.setAttribute("class", "active");
                item.className += " active";
            }
            var article = new Article(
                i,
                item,
                this.articles[i].title,
                this.articles[i].article_img,
                this.articles[i].article_href,
                this.articles[i].date,
                this.articles[i].author_img,
                this.articles[i].author_href,
                this.articles[i].author_name,
                true
            );
            article.init();
            indicators.append(indicator);
            inner.append(item);
        }
        carousel.append(indicators);
        carousel.append(inner);
        for (var i of [["prev", "Previous"], ["next", "Next"]]) {
            var button = document.createElement("a");
            button.setAttribute("class", `carousel-control-${i[0]}`);
            button.setAttribute("href", `#${this.id}`);
            button.setAttribute("role", "button");
            button.setAttribute("data-slide", i[0]);
            var icon = document.createElement("span");
            icon.setAttribute("class", `carousel-control-${i[0]}-icon`);
            icon.setAttribute("aria-hidden", "true");
            var sr_only = document.createElement("span");
            sr_only.setAttribute("class", "sr-only");
            sr_only.innerHTML = i[1];
            button.append(icon);
            button.append(sr_only);
            carousel.append(button);
        }
        d_inline.append(carousel);
        var button_div = document.createElement("div");
        button_div.className = "d-flex justify-content-center";
        var a = document.createElement("a");
        a.href = this.href;
        a.id = "carousel-id";
        a.innerHTML = this.innerHTML;
        a.style.color = "#999999";
        a.className = "btn btn-secondary bg-dark mb-4";
        button_div.append(a);
        d_inline.append(button_div);
        div.append(d_inline);
        document.getElementById(this.parent).append(div);
    }
}

function init_carousel(href, innerHTML) {
    var form = new FormData();
    form.append("articles", true);
    fetch(`/`, {
        method: "POST",
        body: form
    })
    .then(function(response) {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("Request failed.");
        }
    })
    .then(function(articles) {
        if (articles.length > 0) {
            var carousel = new Carousel(1, articles, "articles", href, innerHTML);
            carousel.init();
        }
    })
    .catch(function(error) {
        console.error(error);
    });
}

function add_comment(primary_id) {
    document.getElementById(`submit-send-${primary_id}`).onclick = function (e) {
        var form = new FormData();
        form.append("content", document.getElementById(`textarea-${primary_id}`).value);
        form.append("primary_id", primary_id);
        form.append("add", true);
        fetch(`/article/${title}`, {
            method: "POST",
            body: form
        })
        .then(function(response) {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("Request failed.");
            }
        })
        .then(function(comment) {
            document.getElementById(`span-comments-${primary_id}`).innerHTML = `(${comment.total})`;
            var card = new Card(
                primary_id = comment.primary_id,
                secondary_id = comment.secondary_id,
                content = comment.content,
                src = comment.src,
                href = comment.href,
                date = comment.date,
                username = comment.username,
                like = comment.likes,
                dislike = comment.dislikes
            );
            card.header();
            card.body();
            card.footer();
            document.getElementById(`textarea-${comment.primary_id}`).value = "";
            document.getElementById(`hidden-value-${comment.primary_id}-${comment.secondary_id}`).value = comment.hidden_value;
            document.getElementById(`btn-reply-${comment.primary_id}`).click();
        })
        .catch(function(error) {
            console.error(error);
        });
    }
}


function like_dislike_comment(primary_id, select, value) {
    document.getElementById(`btn-${select}-${primary_id}`).onclick = function (e) {
        var form = new FormData();
        form.append("value", value);
        form.append("primary_id", primary_id);
        form.append("like_dislike", select);
        fetch(`/article/${title}`, {
            method: "POST",
            body: form
        })
        .then(function(response) {
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("Request failed.");
            }
        })
        .then(function(data) {
            var like = data.like;
            var dislike = data.dislike;
            for (var i of [[like, "like"], [dislike, "dislike"]]) {
                if (i[0] == 0) {
                    document.getElementById(`span-${i[1]}-${primary_id}`).innerHTML = "";
                } else {
                    document.getElementById(`span-${i[1]}-${primary_id}`).innerHTML = "(" + i[0] + ")";
                }
            }
        })
        .catch(function(error) {
            console.error(error);
        });
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
            form.append("update", true);
            fetch(`/article/${title}`, {
                method: "POST",
                body: form
            })
            .then(function(response) {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw new Error("Request failed.");
                }
            })
            .then(function(data) {
                content.innerHTML = data.content;
                hidden_value.value = data.hidden_value;
                hidden.style.display = "none";
                content.style.display = "block";
                btn_update.innerHTML = "Update";
                active = false;
            })
            .catch(function(error) {
                console.error(error);
            });
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
            form.append("delete", true);
            fetch(`/article/${title}`, {
                method: "POST",
                body: form
            })
            .then(function(response) {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw new Error("Request failed.");
                }
            })
            .then(function(data) {
                var primary_id = data.primary_id;
                var parent_id = data.parent_id;
                var total = data.total;
                document.getElementById(`card-header-${primary_id}`).remove();
                document.getElementById(`card-body-${primary_id}`).remove();
                document.getElementById(`card-footer-${primary_id}`).remove();
                if (total == 0) {
                    document.getElementById(`span-comments-${parent_id}`).innerHTML = "";
                } else {
                    document.getElementById(`span-comments-${parent_id}`).innerHTML = `(${total})`;
                }
            })
            .catch(function(error) {
                console.error(error);
            });
        }
    } catch (error) {
        return;
    }
}

function init_card(parent) {
    var div = document.createElement("div");
    div.id = `comments-${title}`;
    document.getElementById(parent).append(div);
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
    form.append("comments", true);
    fetch(`/article/${title}`, {
        method: "POST",
        body: form
    })
    .then(function(response) {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("Request failed.");
        }
    })
    .then(function(comments) {
        if (comments.length > 0) {
            recursively_init_comments(comments, `${title}-secondary`);
        }
        article_stats(comments);
    })
    .catch(function(error) {
        alert(error);
    });
}

function list_articles(articles) {
    var div = document.createElement("div");
    div.className = "container rounded";
    div.style.height = "40rem";
    var length = articles.length;
    var row = document.createElement("div");
    row.className = "row";
    for (var i = 0; i < length; i++) {
        var col = document.createElement("div");
        col.className = "col-sm-3";
        var article = new Article(
            i,
            col,
            articles[i].title,
            articles[i].article_img,
            articles[i].article_href,
            articles[i].date,
            articles[i].author_img,
            articles[i].author_href,
            articles[i].author_name,
            false
        )
        article.init();
        row.append(col);
        div.append(row);
    }
    document.getElementById("list").append(div);
}

function init_articles(url) {
    var form = new FormData();
    form.append("all_articles", true);
    fetch(url, {
        method: "POST",
        body: form
    })
    .then(function(response) {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("Request failed.");
        }
    })
    .then(function(articles) {
        list_articles(articles);
    })
    .catch(function(error) {
        console.error(error);
    });
}

class Category {
    constructor(id, parent, child) {
        var div = document.createElement("div");
        div.className = "d-flex p-1";
        div.style.background = "RGBA(0, 0, 0, 0)";
        div.style.verticalAlign = "middle";
        var a = document.createElement("a");
        a.id = id;
        a.className = "card-header col bg-dark text-center rounded";
        a.innerHTML = id.replace("/article/", "");
        a.style.verticalAlign = "middle";
        if (child) {
            a.href = "/article/" + id;
            div.append(a);
        } else {
            a.href = `#category-${id}`;
            a.setAttribute("data-toggle", "collapse");
            a.setAttribute("role", "button");
            a.setAttribute("aria-expanded", false);
            a.setAttribute("aria-controls", `category-${id}`);
            var collapse = document.createElement("div");
            collapse.id = `category-${id}`;
            collapse.setAttribute("data-parent", `#${parent}`);
            collapse.className = `collapse`;
            var d_flex = document.createElement("div");
            var inner = document.createElement("div");
            inner.id = `inner-${id}`;
            d_flex.append(inner);
            collapse.append(d_flex);
            div.append(a);
            div.append(collapse);
        }
        document.getElementById(parent).append(div);
    }
}

function recursively_init_categories(cats, id) {
    for (category of cats) {
        if (category.children.length > 0) {
            var child = false;
        } else {
            var child = true;
        }
        new Category(category.category, id, child);
        if (category.children.length > 0) {
            recursively_init_categories(category.children, `inner-${category.category}`);
        }
    }
}

function init_categories() {
    var form = new FormData();
    form.append("articles", true);
    fetch("/articles", {
        method: "POST",
        body: form
    })
    .then(function(response) {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("Request failed.");
        }
    })
    .then(function(articles) {
        recursively_init_categories(articles, "cat-container");
    })
    .catch(function(error) {
        console.error(error);
    });
}

function create_table(data, columns) {
    var text = "<table><tr>";
    for (var column of columns) {
        text += `<th class="p-2 border border-secondary bg-dark">${column}</th>`;
    }
    text += "</tr>"
    for (var row of data) {
        text += "<tr>";
        for (var col of row) {
            text += `<td class="p-2 border border-secondary">${col}</td>`;
        }
        text += "</tr>";
    }
    text += "</tr></table>";
    return text;
}
