def get_categories(articles):
    d = {}
    for article in articles:
        category = article["category"].split(" / ")
        if category and category[0]:
            if "category" not in d:
                d["category"] = category[0]
                d["children"] = []
            if not d["children"]:
                d["children"].extend(get_categories([{"category": " / ".join(category[1:])}]))
            else:
                categories = get_categories([{"category": " / ".join(category[1:])}])
                control = False
                for i in categories:
                    for j in d["children"]:
                        index = d["children"].index(j)
                        if i["category"] == j["category"]:
                            d["children"][index]["children"].extend(i["children"])
                            control = False
                        else:
                            control = True
                if control:
                    d["children"].extend(categories)
    return [d] if d else []


a = [
    {"category": 'Programming / Web / Jinja'},
    {"category": 'Programming / Web / HTML'},
    {"category": 'Programming / GUI / Tkinter'},
    {"category": 'Programming / GUI / App'}
]


t = get_categories(a)



print(t)


