function rgb(r, g, b) {
    return "#" + [r, g, b].map(i => i.toString(16)).map(i => i.length < 2 ? `0${i}` : i).join("")
}

function convert(n, units) {
    return units.length != 0 ? [parseInt(n * units[0]), ...convert(n - parseInt(n * units[0]) / units[0], units.slice(1))] : []
}

function reformat(n) {
    return convert(n, [1, 24, 24 * 60, 24 * 60 * 60]).slice(1).map(i => i < 9 ? "0" + i : i).join(":");
}

function *combinations(iterable, repeat) {
    if (repeat == 0) {
        yield [];
        return;
    }
    for (var i = 0; i < iterable.length; i++) {
        for (var comb of combinations(iterable.slice(i + 1), repeat - 1)) {
            yield [iterable[i], ...comb];
        }
    }
}

function gradient(x, r) {
    var y = x.map(i => i);
    y = y.sort((i, j) => i - j);
    y = r ? y.reverse() : y;
    var object = {};
    for (var i = 0; i < 24; i++) {
        if (i < 12) {
            var color = rgb(255, parseInt(256 * i / 12), 0);
        } else {
            var color = rgb(255 - parseInt(256 * (i - 12) / 12), 255, 0);
        }
        object[y[i]] = color;
    }
    return Object.fromEntries([...Array(24).keys()].map(i => [x[i], object[x[i]]]));
}

function change_colors(table, all) {
    var opt = {
        "AHT": true,
        "Trend": true,
        "Volume": true,
        "Need": true,
        "Actual": true,
        "Coverage": false,
        "Occupancy": true,
        "Idle": false

    }
    for (var [k, v] of Object.entries(opt)) {
        if (["AHT"].includes(k)) {
            continue;
        }
        var graded = gradient(all[k], v);
        for (i = 0; i < 24; i++) {
            table[i][k].style.background = graded[all[k][i].toString()];
            if (["Trend", "Coverage", "Occupancy"].includes(k)) {
                table[i][k].innerHTML = `${Math.round(parseFloat(table[i][k].innerHTML) * 100 * 100) / 100} %`;
            } else if (["Idle"].includes(k)) {
                table[i][k].innerHTML = reformat(parseFloat(table[i][k].innerHTML));
            } else {
                table[i][k].innerHTML = Math.round(parseFloat(table[i][k].innerHTML) * 100) / 100;
            }
        }
    }
}

function headcount() {
    var d_flex = document.createElement("div");
    var container = document.createElement("div");
    var table_div = document.createElement("div");
    var table = document.createElement("table");
    var tr = document.createElement("tr");
    container.className = "border border-dark m-4 pt-2 pl-2 pr-2 text-center bg-dark";
    table.className = "table-sm table-dark table-bordered container";
    d_flex.data = {};
    d_flex.data["sum"] = 0;
    for (var i of ["Total HC", "Daily HC", "Utilization Rate"]) {
        var th = document.createElement("th");
        th.innerHTML = i;
        th.className = "col-2";
        tr.append(th);
    }
    table.append(tr);
    var tr = document.createElement("tr");
    for (var i of ["Total HC", "Daily HC", "Utilization Rate"]) {
        var td = document.createElement("td");
        td.innerHTML = 0;
        td.className = "btn-outline-secondary";
        tr.append(td);
        d_flex.data[i] = td;
    }
    table.append(tr);
    table_div.append(table);
    container.append(table_div);
    d_flex.append(container);
    return d_flex;
}

function activity_form(columns, data) {
    var all = false;
    var d_flex = document.createElement("div");
    var container = document.createElement("div");
    var h3 = document.createElement("h3");
    var table_div = document.createElement("div");
    var table = document.createElement("table");
    var button_div = document.createElement("div");
    container.className = "border border-secondary m-4 pt-2 pl-2 pr-2 text-center bg-dark";
    d_flex.data = [];
    h3.innerHTML = "Offline Activities";
    h3.className = "text-secondary";
    container.append(h3);
    for (var name of ["+", "-"]) {
        var btn = document.createElement("button");
        btn.className = "col-1 btn btn-dark border-secondary m-4";
        btn.innerHTML = name;
        button_div.append(btn);
    }
    container.append(button_div);
    table.className = "table table-dark table-bordered container";
    table_div.style.maxHeight = "20rem";
    table_div.style.overflowY = "auto";
    var tr = document.createElement("tr");
    for (var [k, v] of Object.entries(columns)) {
        if (k != "Select All") {
            var th = document.createElement("th");
            th.innerHTML = k;
            th.className = "col-2"
        } else {
            var th = document.createElement("th");
            var div = document.createElement("div");
            var input = document.createElement("input");
            var label = document.createElement("label");
            div.className = "d-flex flex-column";
            input.type = "checkbox";
            label.innerHTML = k;
            th.className = "col-2";
            div.append(label);
            div.append(input)
            th.append(div);
        }
        tr.append(th);
    }
    table.append(tr);
    table_div.append(table);
    container.append(table_div);
    button_div.children[0].onclick = function (e) {
        var tr = document.createElement("tr");
        var row = {};
        for (var [k, v] of Object.entries(columns)) {
            var td = document.createElement("td");
            var div = document.createElement("div");
            var input = document.createElement("input");
            if (v["type"] == "number") {
                input.min = v["min"];
                input.value = v["min"];
                input.max = v["max"];
                input.step = v["step"];
            }
            input.type = v["type"];
            input.className += " col form-control bg-dark text-light border-secondary";
            if ((k == "Select All") & (all)) {
                input.checked = true;
            }
            div.append(input);
            td.append(div);
            tr.append(td);
            row[k] = input;
        }
        d_flex.data.push(row);
        table.append(tr);
        for (var row of d_flex.data) {
            for (var [k, v] of Object.entries(columns)) {
                if (k != "Name") {
                    row[k].oninput = function (e) { activity_oninput(d_flex, data) };
                }
            }
        }
    }
    button_div.children[1].onclick = function (e) {
        var indexes = [];
        for (var child of table.children) {
            if ((child.children[0].children[0].children[0].checked) & (child.children[1].innerHTML != "Name")) {
                indexes.push([...table.children].indexOf(child));
            }
        }
        var items = indexes.map(i => table.children[i]);
        var rows = indexes.map(i => d_flex.data[i]);
        for (var i = 0; i < items.length; i++) {
            table.removeChild(items[i]);
            d_flex.data.splice(d_flex.data.indexOf(rows[i]), 1);
        }
        activity_oninput(d_flex, data);
    }
    table.children[0].children[0].onclick = function(e) {
        if (e.target.checked) {
            for (var child of table.children) {
                child.children[0].children[0].children[0].checked = true;
                all = true;
            }
        } else {
            for (var child of table.children) {
                child.children[0].children[0].children[0].checked = false;
                all = false;
            }
        }
    }
    d_flex.append(container);
    return d_flex;
}

function activity_oninput(d_flex, data) {
    var sum = 0;
    for (var r of d_flex.data) {
        var dict = Object.fromEntries(["Start", "End", "Interval"].map(i => [i, parseFloat(r[i].value)]))
        if ((dict["End"] - dict["Start"]) * 60 >= dict["Interval"]) {
            sum += dict["Interval"] / 60;
        }
    }
    if (data.hasOwnProperty("d_flex")) {
        var d_flex_data = data["d_flex"].data;
        var volume = parseInt(d_flex_data["Volume"].value);
        var aht = parseFloat(d_flex_data["AHT"].value);
        var shrinkage = parseFloat(d_flex_data["Shrinkage"].value);
        var work_hour = parseFloat(d_flex_data["Work Hour"].value);
        var off_day = parseInt(d_flex_data["Off Day"].value);
        data["Utilization Rate"].innerHTML = Math.round((work_hour - sum) / work_hour * 100) / 100;
        var ur = parseFloat(data["Utilization Rate"].innerHTML);
        var daily_hc = volume * aht / (work_hour * 3600 * (1 - shrinkage) * ur * (7 - off_day) / 7);
        data["Daily HC"].innerHTML = parseInt(daily_hc);
        data["Total HC"].innerHTML = parseInt(daily_hc * (7 / (7 - off_day)) / (1 - shrinkage));
    }
    data["sum"] = sum;
}

function collapse(parent, columns) {
    var accordion = document.createElement("div");
    var right = document.createElement("div");
    accordion.id = "accordion";
    accordion.className = "text-center"
    right.id = "right";
    function query(media) {
        if (media.matches) {
            right.className = "";
        } else {
            right.className = "container";
        }
    }
    var media = window.matchMedia("(max-width: 600px)")
    query(media)
    media.addListener(query)
    for (var [k, v] of Object.entries(columns)) {
        var btn = document.createElement("button");
        var collapse = document.createElement("div");
        btn.className = "btn btn-dark flex-column m-2 col-2 border border-secondary";
        btn.setAttribute("data-toggle", "collapse");
        btn.setAttribute("data-target", `#collapse-${k}`);
        btn.setAttribute("aria-expanded", false);
        btn.setAttribute("aria-controls", `collapse-${k}`);
        btn.innerHTML = k;
        collapse.id = `collapse-${k}`;
        collapse.className = "collapse";
        collapse.setAttribute("data-parent", "#right");
        collapse.setAttribute("aria-labeledby", `heading-${k}`);
        collapse.append(v);
        right.append(collapse);
        accordion.append(btn);
    }
    document.getElementById(parent).append(accordion);
    document.getElementById(parent).append(right);
}

function get_trends(e) {
    return e.target.value.split("\n").map(i => parseFloat(i));
}

function sum(iterable) {
    return iterable.length > 0 ? (iterable[0] + sum(iterable.slice(1))) : 0;
}

function control_row(e, result) {
    var split = e.target.value.split("\n");
    while (split.length > 24) {
        split = split.slice(0, -1);
    }
    e.target.value = split.join("\n");
    result.innerHTML = sum(split.map(i => parseFloat(i)));
}

function trend_form() {
    var d_flex = document.createElement("div");
    var container = document.createElement("div");
    var table = document.createElement("table");
    var tr = document.createElement("tr");
    var h3 = document.createElement("h3");
    var result = document.createElement("label")
    d_flex.className = "d-flex justify-content-center";
    d_flex.data = {};
    container.className = "border border-secondary m-4 pt-2 pl-2 pr-2 text-center bg-dark";
    table.className = "table-sm table-dark table-bordered container";
    h3.innerHTML = "Trend";
    h3.className = "text-secondary";
    container.append(h3);
    for (var col of [["Hour", 5], ["Trend", 100]]) {
        var td = document.createElement("td");
        var textarea = document.createElement("textarea");
        td.append(textarea);
        tr.append(td);
        textarea.rows = 24;
        textarea.cols = col[1];
        textarea.style.resize = "none";
        textarea.style.outline = "none";
        textarea.style.overflow = "hidden";
        textarea.style.border = "none";
        d_flex.data[col[0]] = textarea;
    }
    table.append(tr);
    d_flex.data["Hour"].readOnly = true;
    d_flex.data["Hour"].className = "table-dark";
    for (var i = 0; i < 24; i++) {
        d_flex.data["Hour"].value += i <= 9 ? `0${i}:00` : `${i}:00` + "\n";
        d_flex.data["Trend"].value += 1/24 + "\n";
    }
    d_flex.data["Trend"].oninput = function (e) { control_row(e, result) };
    d_flex.data["Trend"].onpaste = function (e) { control_row(e, result) };
    d_flex.data["Trend"].className = "bg-dark text-light form-control border border-secondary";
    container.append(table);
    result.className = "text-secondary";
    result.innerHTML = sum(d_flex.data["Trend"].value.split("\n").slice(0, -1).map(i => parseFloat(i)));
    container.append(result);
    d_flex.append(container);
    return d_flex;
}

function range_form(parent, columns, main_table) {
    var d_flex = document.createElement("div");
    var hc = headcount();
    var container = document.createElement("div");
    var table_div = document.createElement("div");
    var table = document.createElement("table");
    var tr = document.createElement("tr");
    var count = 0;
    var result_div = document.createElement("div");
    var result = document.createElement("label");
    for (var [k, v] of Object.entries(columns)) {
        var th = document.createElement("th");
        th.innerHTML = k;
        tr.append(th);
    }
    table.append(tr);
    d_flex.data = {};
    table.className = "table table-dark table-bordered container";
    function query(media) {
        if (media.matches) {
            container.className = "border border-secondary text-center bg-dark";
        } else {
            container.className = "border border-secondary m-4 pt-2 pl-2 pr-2 text-center bg-dark";
        }
    }
    var media = window.matchMedia("(max-width: 600px)")
    query(media)
    media.addListener(query)
    container.append(hc);
    result.className = "btn-outline-secondary";
    var tr = document.createElement("tr");
    for (var [k, v] of Object.entries(columns)) {
        var td = document.createElement("td");
        var input = document.createElement("input");
        input.type = v["type"];
        input.min = v["min"];
        input.value = v["min"];
        input.max = v["max"];
        input.step = v["step"];
        input.className = "form-control bg-dark text-light border-secondary";
        d_flex.data[k] = input;
        td.append(input);
        tr.append(td);
    }
    table.append(tr);
    for (var [k, v] of Object.entries(d_flex.data)) {
        v.oninput = function (e) {
            var volume = parseInt(d_flex.data["Volume"].value);
            var aht = parseFloat(d_flex.data["AHT"].value);
            var shrinkage = parseFloat(d_flex.data["Shrinkage"].value);
            var work_hour = parseFloat(d_flex.data["Work Hour"].value);
            var off_day = parseInt(d_flex.data["Off Day"].value);
            var ur = parseFloat(hc.data["Utilization Rate"].innerHTML);
            if (parseFloat(hc.data["sum"]) > 0) {
                hc.data["Utilization Rate"].innerHTML = Math.round((work_hour - parseFloat(hc.data["sum"])) / work_hour * 100) / 100;
            } else if (!ur) {
                hc.data["Utilization Rate"].innerHTML = 1;
                ur = 1;
            }
            var daily_hc = volume * aht / (work_hour * 3600 * (1 - shrinkage) * ur * (7 - off_day) / 7);
            hc.data["Daily HC"].innerHTML = parseInt(daily_hc);
            hc.data["Total HC"].innerHTML = parseInt(daily_hc * (7 / (7 - off_day)) / (1 - shrinkage));
            hc.data["d_flex"] = d_flex;
        }
    }
    table_div.append(table);
    container.append(table_div);
    result_div.append(result);
    container.append(result_div);
    var offline_activity = activity_form(
        columns={
            "Select All": {"type": "checkbox"},
            "Name": {"type": "input"},
            "Start": {"type": "number", "min": 0, "max": 24, "step": .25},
            "End": {"type": "number", "min": 0, "max": 24, "step": .25},
            "Interval": {"type": "number", "min": 0, "max": 24, "step": .25}
        },
        data=hc.data
    )
    container.append(offline_activity);
    d_flex.append(container);
    var trend = trend_form();
    container.append(trend);
    var btn = document.createElement("button");
    btn.className = "btn btn-outline-secondary m-4";
    btn.innerHTML = "Analyze";
    btn.onclick = function (e) { analyze(hc.data, trend.data, d_flex.data, offline_activity.data, main_table) }
    container.append(btn);
    document.getElementById(parent).append(d_flex);
    return d_flex;
}

function get_activities(activities) {
    var table = [];
    for (var row of activities) {
        var row_data = [];
        for (var [k, v] of Object.entries(row)) {
            if (["Start", "End", "Interval"].includes(k)) {
                row_data.push(parseFloat(v.value));
            }
        }
        table.push(row_data);
    }
    return table;
}

function get_coverage(hc, needs) {
    var coverage = [];
    for (var i = 0; i < hc.length; i++) {
        if (hc[i] > needs[i]) {
            coverage.push(hc[i] / needs[i]);
        }
    }
    return (coverage.length == 24) ? coverage : null;
}

function get_results(combs, daily_hc, activities, work_hour, needs, trend) {
    var result = {};
    var leak_hour = work_hour - parseInt(work_hour);
    work_hour = parseInt(work_hour);
    for (var comb of combs) {
        var hc = [...Array(24).keys()].map(i => 0);
        for (var hour of comb) {
            for (var i = 0; i < work_hour; i++) {
                hc[(hour + i) % 24] += daily_hc / comb.length;
            }
            if (leak_hour > 0) {
                hc[(hour + work_hour) % 24] += (daily_hc / comb.length) * leak_hour;
            }
            for (var activity of activities) {
                var start = activity[0];
                var end = activity[1];
                if (end < start) {
                    continue;
                }
                var interval = activity[2];
                var size = (end - start) * (60 / interval);
                while (start != parseInt(end)) {
                    var int = parseInt(start);
                    if (start != int) {
                        hc[(hour + int) % 24] -= 1/size * (1 - (start - int)) * (daily_hc / comb.length);
                        start += 1 - (start - int);
                    } else {
                        hc[(hour + start) % 24] -= 1/size * (daily_hc / comb.length);
                        start += 1;
                    }
                }
                var int = parseInt(end);
                if (int != end) {
                    hc[(hour + int) % 24] -= 1/size * (1 - (end - int)) * (daily_hc / comb.length);
                }
            }
        }
        var coverage = get_coverage(hc, needs);
        if (coverage) {
            var occupancy = coverage.map(i => ((i <= 1) ? 1 : (1 / i)));
            var idle = [...Array(24).keys()].map(i => trend[i] * (1 - occupancy[i]) / occupancy[i]);
            result[comb] = {
                "hc": hc,
                "coverage": coverage,
                "occupancy": occupancy,
                "idle": idle
            }
        }
    }
    return result;
}

function analyze(hc, trend, input, offline_activity, main_table) {
    empty(main_table, "N Shift");
    empty(main_table, "Shift");
    var volume = parseInt(input["Volume"].value);
    var aht = parseFloat(input["AHT"].value);
    var shrinkage = parseFloat(input["Shrinkage"].value);
    var work_hour = parseFloat(input["Work Hour"].value);
    var daily_hc = parseInt(hc["Daily HC"].innerHTML);
    var trend = trend["Trend"].value.split("\n").map(i => parseFloat(i));
    var activities = get_activities(offline_activity);
    var volumes = trend.map(i => i * volume);
    var needs = [...Array(24).keys()].map(i => volumes[i] * aht / (3600 * (1 - shrinkage)));
    var results = {}
    for (var i of [3, 4, 5]) {
        var combs = combinations([...Array(24).keys()], i);
        var result = get_results(combs, daily_hc, activities, work_hour, needs, trend);
        if (Object.keys(result).length == 0) {
            continue;
        }
        results[i] = result;
        for (var [k, v] of Object.entries(result)) {
            var opt = document.createElement("option");
            opt.value = k;
            opt.innerHTML = k;
            main_table.data["Shift"].append(opt);
        }
        var opt = document.createElement("option");
        opt.value = i;
        opt.innerHTML = i;
        main_table.data["N Shift"].append(opt);
    }
    main_table.data["N Shift"].onchange = function (e) { change_selections(e, main_table, results)}
    main_table.data["Shift"].onchange = function (e) { change_values(e, main_table, results, needs, volumes, aht, trend) }
    change_values(null, main_table, results, needs, volumes, aht, trend);
}

function change_values(e, main_table, results, needs, volumes, aht, trend) {
    var n_shift = parseInt(main_table.data["N Shift"].value);
    var values = e ? results[n_shift][e.target.value] : results[n_shift][Object.keys(results[n_shift])[0]];
    var all = {
        "AHT": [...Array(24).keys()].map(i => aht),
        "Trend": trend,
        "Volume": volumes,
        "Need": needs.map(i => Math.round(i * 100) / 100),
        "Actual": values["hc"],
        "Coverage": values["coverage"],
        "Occupancy": values["occupancy"],
        "Idle": values["idle"]
    }
    for (var i = 0; i < 24; i++) {
        for (var col of main_table.columns) {
            main_table.data[i][col].innerHTML = all[col][i];
        }
    }
    change_colors(main_table.data, all);
    main_table.data["container"].append(main_table.data["canvas"]);
    var xValues = [...Array(24).keys()].map(i => (i <= 9) ? `0${i}:00` : `${i}:00`);
    new Chart("canvas", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [
                {
                    label: "Need",
                    data: all["Need"],
                    borderColor: "red",
                    fill: false
                },
                {
                    label: "Actual",
                    data: all["Actual"],
                    borderColor: "green",
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Time"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "HC"
                    }
                }
            }
        }
    });
}

function empty(main_table, key) {
    while (main_table.data[key].children.length > 0) {
        var child = main_table.data[key].children[0];
        main_table.data[key].removeChild(child);
    }
}

function change_selections(e, main_table, results) {
    empty(main_table, "Shift");
    for (var [k, v] of Object.entries(results[parseInt(e.target.value)]))  {
        var opt = document.createElement("option");
        opt.value = k;
        opt.innerHTML =k;
        main_table.data["Shift"].append(opt);
    }
}

function create_table(parent, columns) {
    var d_flex = document.createElement("div");
    d_flex.columns = [...Object.keys(columns)].slice(1);
    var container = document.createElement("div");
    var table_div = document.createElement("div");
    var table = document.createElement("table");
    var tr = document.createElement("tr");
    var select_div = document.createElement("div");
    table_div.style.overflowX = "scroll";
    var state = {"value": false};
    function query(media) {
        if (media.matches) {
            container.className = "border border-secondary text-center bg-dark";
        } else {
            container.className = "border border-secondary m-4 pt-2 pl-2 pr-2 text-center bg-dark";
        }
    }
    var media = window.matchMedia("(max-width: 600px)")
    query(media)
    media.addListener(query)
    table.className = "table-sm table-dark table-bordered container";
    d_flex.data = {};
    var _table = document.createElement("table");
    _table.className = "table-sm table-dark table container"
    var _tr = document.createElement("tr");
    for (var i of ["N Shift", "Shift"]) {
        var th = document.createElement("th");
        th.innerHTML = i;
        th.className = "col-4";
        _tr.append(th);
    }
    _table.append(_tr);
    var _tr = document.createElement("tr");
    for (var i of ["N Shift", "Shift"]) {
        var td = document.createElement("td");
        var select = document.createElement("select");
        select.className = "btn bg-dark border-secondary my-2 col-6";
        d_flex.data[i] = select;
        td.append(select);
        _tr.append(td);
    }
    _table.append(_tr);
    select_div.append(_table);
    container.append(select_div);
    var tr = document.createElement("tr");
    for (var [k, v] of Object.entries(columns)) {
        var th = document.createElement("th");
        th.innerHTML = k;
        tr.append(th);
    }
    table.append(tr);
    for (var i = 0; i < 24; i++) {
        d_flex.data[i] = {}
        var tr = document.createElement("tr");
        for (var [k, v] of Object.entries(columns)) {
            var td = document.createElement("td");
            td.innerHTML = 0;
            if (k == "Time") {
                td.innerHTML = v["values"][i];
            }
            tr.append(td);
            td.className = "btn-outline-secondary"
            d_flex.data[i][k] = td;
        }
        d_flex.data[i]["Time"].style.background = "#aacb9a";
        table.append(tr);
    }
    table_div.append(table);
    var canvas = document.createElement("canvas");
    canvas.id = "canvas";
    canvas.className = "my-4 p-4 border border-secondary table-dark rounded";
    d_flex.data["canvas"] = canvas;
    d_flex.data["container"] = container;
    container.append(table_div);
    d_flex.append(container);
    document.getElementById(parent).append(d_flex);
    return d_flex;
}

function run() {
    var analysis = create_table(
        "main",
        columns={
            "Time": {"values": [...Array(24).keys()].map(i => i <= 9 ? `0${i}:00` : `${i}:00`)},
            "AHT": {},
            "Trend": {},
            "Volume": {},
            "Need": {},
            "Actual": {},
            "Coverage": {},
            "Occupancy": {},
            "Idle": {}
        }
    )
    var input = range_form(
        "main",
        columns={
            "Volume": {"min": 0, "max": 1000000, "step": 1, "type": "number"},
            "AHT": {"min": 0, "max": 360, "step": .01, "type": "number"},
            "Shrinkage": {"min": 0, "max": 1, "step": .01, "type": "number"},
            "Work Hour": {"min": 0, "max": 24, "step": .25, "type": "number"},
            "Off Day": {"min": 0, "max": 7, "step": 1, "type": "number"},
        },
        main_table=analysis
    );
    var col = collapse("main", {"Input": input, "Analysis": analysis});
}

run();

