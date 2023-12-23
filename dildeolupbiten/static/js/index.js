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
    container.className = "m-4 text-center bg-dark";
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
        btn.className = "btn btn-dark flex-column m-4 col-2 border border-secondary";
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
    result.innerHTML = sum(split.map(i => parseFloat(i.replace(",", "."))));
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

function planning_section(columns, values) {
    var d_flex = document.createElement("div");
    d_flex.data = {};
    var container = document.createElement("div");
    var table_div = document.createElement("div");
    var button_div = document.createElement("div");
    var result_div = document.createElement("div");
    var table = document.createElement("table");
    var trh = document.createElement("tr");
    var trd = document.createElement("tr");
    container.className = "text-center bg-dark";
    table.className = "table-sm table-dark table-bordered container";
    for (var i = 0; i < columns.length; i++) {
        var th = document.createElement("th");
        th.innerHTML = columns[i];
        th.className = "col-3";
        trh.append(th);
        var td = document.createElement("td");
        td.className = "col-3";
        if (columns[i] == "Days") {
            var input = document.createElement("input");
            input.min = 0;
            input.max = 7 * 52;
            input.value = 0;
            input.step = 7;
            input.type = "number";
            input.className += " col form-control bg-dark text-light border-secondary";
            td.append(input);
            d_flex.data[columns[i]] = input;
        } else {
            td.innerHTML = 0;
            d_flex.data[columns[i]] = td;
        }
        trd.append(td);
    }
    table.append(trh);
    table.append(trd);
    table_div.append(table);
    var button = document.createElement("button");
    button.innerHTML = "Create Shift Plan";
    button.className = "col-4 btn btn-dark border-secondary m-4 text-secondary";
    button_div.append(button);
    container.append(table_div);
    container.append(button_div);
    container.append(result_div);
    d_flex.append(container);
    button.onclick = function (e) { request_for_shift_plan(d_flex.data, result_div) }
    return d_flex;
}

function request_for_shift_plan(data, result_div) {
    if (parseFloat(data["Days"].value) % 7 != 0) {
        alert("Select 7 or times of 7!");
        return;
    }
    if (data["Shift"].innerHTML == "0") {
        alert("Fill the inputs!");
        return;
    }
    if (parseInt(data["Days"].value) == 0) {
        alert("Select days!");
        return;
    }
    var form = new FormData();
    for (var child of result_div.children) {
        result_div.removeChild(child);
    }
    form.append("shift_plan", true);
    form.append("Total HC", data["Total HC"].innerHTML);
    form.append("Shift", data["Shift"].innerHTML);
    form.append("Days", data["Days"].value);
    form.append("Off Day", data["Off Day"].innerHTML);
    fetch("/wfm", {
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
    .then(function(plan) {
        if (plan.length == 0) {
            alert("An error occurred");
            return;
        }
        result_div.append(shift_plan_table(plan, data["Shift"].innerHTML, data["Work Hour"], data["Activities"], data["Needs"], data["Trend"], data["main_table"], data["Volumes"], data["aht"], data["plan_section"], data["Input"], data["HC"]));
    })
    .catch(function(error) {
        console.error(error);
    });
}

function shift_plan_table(plan, shifts, work_hour, activities, needs, trend, main_table, volumes, aht, plan_section, input, hc) {
    var [shift_plan, dist] = plan;
    work_hour = parseFloat(work_hour);
    var shifts = shifts.split(",").map(i => parseInt(i));
    var d_flex = document.createElement("div");
    var container = document.createElement("div");
    var table_div = document.createElement("div");
    var table = document.createElement("table");
    var colors = ["#000066", "#ffff66", "#cc6600", "#666600", "#006666"];
    table.className = "table table-sm table-dark table-bordered container";
    table_div.style.maxHeight = "20rem";
    table_div.style.overflowY = "auto";
    container.className = "text-center bg-dark";
    var trh = document.createElement("tr");
    for (var col = 0; col < shift_plan[0].length; col++) {
        var th = document.createElement("th");
        if (col == 0) {
            th.innerHTML = "";
            th.style.width = "5rem";
        } else {
            var label = document.createElement("label");
            label.innerHTML = col
            label.style.width = "3rem";
            th.append(label);
        }
        trh.append(th);
    }
    table.append(trh);
    for (var row = 0; row < shift_plan.length; row++) {
        var tr = document.createElement("tr");
        for (var col = 0; col < shift_plan[row].length + 1; col++) {
            if (col == 1) {
                continue;
            }
            var td = document.createElement("td");
            if (col == 0) {
                var int = row + 1;
                var len = 3 - `${int}`.length;
                var zeros = [...Array(len).keys()].map(i => 0).join("");
                td.innerHTML = (row + 1 < 100) ? `${zeros}${row + 1}` : (row + 1);
                td.style.width = "5rem";
            } else {
                td.innerHTML = shift_plan[row][col - 1];
                td.style.width = "3rem";
                if (shift_plan[row][col - 1] == "OFF") {
                    td.style.background = "#606060"
                } else {
                    td.style.background = colors[shifts.indexOf(shift_plan[row][col - 1])];
                }
            }
            tr.append(td);
        }
        table.append(tr);
    }
    table_div.append(table);
    container.append(table_div);
    d_flex.append(container);
    result_table(d_flex, dist, shifts, colors, work_hour, activities, needs, trend, main_table, volumes, aht, plan_section, input, hc);
    return d_flex;
}

function result_table(parent, dist, shifts, colors, work_hour, activities, needs, trend, main_table, volumes, aht, plan_section, input, hc) {
    var shifts = ["OFF", ...shifts];
    var colors = ["#606060", ...colors];
    var d_flex = document.createElement("div");
    var container = document.createElement("div");
    var table_div = document.createElement("div");
    var table = document.createElement("table");
    table.className = "table table-sm table-dark table-bordered container";
    table_div.style.overflowX = "auto";
    container.className = "text-center bg-dark";
    var trh = document.createElement("tr");
    for (var col = 0; col < dist[0].length + 1; col++) {
        var th = document.createElement("th");
        if (col == 0) {
            th.innerHTML = "";
            th.style.width = "5rem";
        } else {
            var btn = document.createElement("button");
            btn.innerHTML = col
            btn.className = "btn btn-dark";
            btn.style.width = "3rem";
            btn.onclick = function (e) { display_daily_shifts(e, dist, shifts.slice(1, shifts.length), work_hour, activities, needs, trend, main_table, volumes, aht, plan_section, input, hc) };
            th.append(btn);
        }
        trh.append(th);
    }
    table.append(trh);
    for (var row = 0; row < dist.length; row++) {
        var tr = document.createElement("tr");
        for (var col = 0; col < dist[row].length + 1; col++) {
            var td = document.createElement("td");
            if (col == 0) {
                td.innerHTML = shifts[row];
                td.style.background = colors[row];
                td.style.width = "5rem";
            } else {
                td.innerHTML = dist[row][col - 1];
                td.style.width = "3rem";
            }
            tr.append(td);
        }
        table.append(tr);
    }
    table_div.append(table);
    container.append(table_div);
    d_flex.append(container);
    parent.append(d_flex);
    return d_flex;
}

function display_daily_shifts(e, dist, shifts, work_hour, activities, needs, trend, main_table, volumes, aht, plan_section, input, hc) {
    var col = parseInt(e.target.innerHTML) - 1;
    var shift_hc = dist.map(row => row[col]);
    var total_hc = [...Array(24).keys()].map(i => 0);
    shift_hc = shift_hc.slice(1, shift_hc.length);
    shift_hc = [...Array(shift_hc.length).keys()].map(i => [shifts[i], shift_hc[i]]);
    var leak_hour = work_hour - parseInt(work_hour);
    work_hour += leak_hour;
    for (var [shift, hc] of shift_hc) {
        for (var hour = 0; hour < work_hour; hour++) {
            if ((hour + 1 == work_hour) & (leak_hour != 0)) {
                total_hc[(shift + hour) % 24] += (hc * leak_hour);
            } else {
                total_hc[(shift + hour) % 24] += hc;
            }
        }
    }
    var data = {
        "shifts": shifts,
        "activities": activities,
        "work_hour": work_hour,
        "needs": needs,
        "trend": trend,
        "total_hc": total_hc,
        "volumes": volumes,
        "aht": aht,
        "plan_section": plan_section,
        "input": input,
        "hc": hc
    }
    var results = get_results([shifts], null, activities, work_hour, needs, trend, total_hc);
    change_values(null, main_table, results[shifts.join(",")], needs, volumes, aht, trend, plan_section, input, hc);
}

function range_form(parent, columns, main_table, plan_section) {
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
    table_div.className = "m-4";
    function query(media) {
        if (media.matches) {
            container.className = "border border-secondary text-center bg-dark";
        } else {
            container.className = "border border-secondary pt-2 pl-2 pr-2 text-center bg-dark";
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
    btn.onclick = function (e) { analyze(hc.data, trend.data, d_flex.data, offline_activity.data, main_table, plan_section) }
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

function get_coverage(hc, needs, hc_shift) {
    var coverage = [];
    for (var i = 0; i < hc.length; i++) {
        if (hc[i] > needs[i]) {
            coverage.push(hc[i] / needs[i]);
        } else {
            if (hc_shift) {
                coverage.push(hc[i] / needs[i]);
            }
        }
    }
    if (hc_shift) {
        return coverage;
    }
    return (coverage.length == 24) ? coverage : null;
}

function get_results(combs, daily_hc, activities, work_hour, needs, trend, hc_shift) {
    var result = {};
    var leak_hour = work_hour - parseInt(work_hour);
    work_hour = parseInt(work_hour);
    for (var comb of combs) {
        if (!hc_shift) {
            var hc = [...Array(24).keys()].map(i => 0);
        } else {
            var hc = hc_shift;
        }
        for (var hour of comb) {
            if (!hc_shift) {
                for (var i = 0; i < work_hour; i++) {
                    hc[(hour + i) % 24] += daily_hc / comb.length;
                }
                if (leak_hour > 0) {
                    hc[(hour + work_hour) % 24] += (daily_hc / comb.length) * leak_hour;
                }
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
                        if (!hc_shift) {
                            hc[(hour + int) % 24] -= 1/size * (1 - (start - int)) * (daily_hc / comb.length);
                        } else {
                            hc[(hour + int) % 24] *= (1 - 1/size * (1 - (start - int)));
                        }
                        start += 1 - (start - int);
                    } else {
                        if (!hc_shift) {
                            hc[(hour + start) % 24] -= 1/size * (daily_hc / comb.length);
                        } else {
                            hc[(hour + start) % 24] *= 1 - (1 / size);
                        }
                        start += 1;
                    }
                }
                var int = parseInt(end);
                if (int != end) {
                    if (!hc_shift) {
                        hc[(hour + int) % 24] -= 1/size * (1 - (end - int)) * (daily_hc / comb.length);
                    } else {
                        hc[(hour + int) % 24] *= (1 - 1/size * (1 - (end - int)));
                    }
                }
            }
        }
        var coverage = get_coverage(hc, needs, hc_shift);
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

function analyze(hc, trend, input, offline_activity, main_table, plan_section) {
    empty(main_table, "N Shift");
    empty(main_table, "Shift");
    var volume = parseInt(input["Volume"].value);
    var aht = parseFloat(input["AHT"].value);
    var shrinkage = parseFloat(input["Shrinkage"].value);
    var work_hour = parseFloat(input["Work Hour"].value);
    var daily_hc = parseInt(hc["Daily HC"].innerHTML);
    var trend = trend["Trend"].value.split("\n").map(i => parseFloat(i.replace(",", ".")));
    var activities = get_activities(offline_activity);
    var volumes = trend.map(i => i * volume);
    var needs = [...Array(24).keys()].map(i => volumes[i] * aht / 3600);
    var results = {}
    for (var i of [3, 4, 5]) {
        var combs = combinations([...Array(24).keys()], i);
        var result = get_results(combs, daily_hc, activities, work_hour, needs, trend, null);
        if (Object.keys(result).length == 0) {
            continue;
        }
        results[i] = result;
        for (var [k, v] of Object.entries(result)) {
            if (Object.keys(results).length <= 1) {
                var opt = document.createElement("option");
                opt.value = k;
                opt.innerHTML = k;
                main_table.data["Shift"].append(opt);
            }
        }
        var opt = document.createElement("option");
        opt.value = i;
        opt.innerHTML = i;
        main_table.data["N Shift"].append(opt);
    }
    if (Object.keys(results).length == 0) {
        alert("No combination found!");
        return;
    }
    plan_section.data["Total HC"].innerHTML = hc["Total HC"].innerHTML;
    plan_section.data["Shift"].innerHTML = main_table.data["Shift"].value;
    plan_section.data["Work Hour"] = work_hour;
    plan_section.data["Off Day"].innerHTML = input["Off Day"].value;
    plan_section.data["Activities"] = activities;
    plan_section.data["Needs"] = needs;
    plan_section.data["Trend"] = trend;
    plan_section.data["main_table"] = main_table;
    plan_section.data["Volumes"] = volumes;
    plan_section.data["aht"] = aht;
    plan_section.data["plan_section"] = plan_section;
    plan_section.data["Input"] = input;
    plan_section.data["HC"] = hc;
    main_table.data["N Shift"].onchange = function (e) { change_selections(e, main_table, results, needs, volumes, aht, trend, plan_section, input, hc)}
    main_table.data["Shift"].onchange = function (e) { change_values(e, main_table, results, needs, volumes, aht, trend, plan_section, input, hc) }
    change_values(null, main_table, results, needs, volumes, aht, trend, plan_section, input, hc);
}

function change_values(e, main_table, results, needs, volumes, aht, trend, plan_section, input, hc) {
    var n_shift = parseInt(main_table.data["N Shift"].value);
    var values = results.hasOwnProperty(n_shift) ? (e ? results[n_shift][e.target.value] : results[n_shift][Object.keys(results[n_shift])[0]]) : results;
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
    try {
        plan_section.data["Total HC"].innerHTML = hc["Total HC"].innerHTML;
    } catch {
        plan_section.data["Total HC"].innerHTML = hc;
    }

    plan_section.data["Shift"].innerHTML = main_table.data["Shift"].value;
    plan_section.data["Off Day"].innerHTML = input["Off Day"].value;
    main_table.data["chart"].data.datasets[0].data = all["Need"];
    main_table.data["chart"].data.datasets[1].data = all["Actual"];
    main_table.data["chart"].update();
}

function empty(main_table, key) {
    while (main_table.data[key].children.length > 0) {
        var child = main_table.data[key].children[0];
        main_table.data[key].removeChild(child);
    }
}

function change_selections(e, main_table, results, needs, volumes, aht, trend, plan_section, input, hc) {
    empty(main_table, "Shift");
    for (var [k, v] of Object.entries(results[parseInt(e.target.value)]))  {
        var opt = document.createElement("option");
        opt.value = k;
        opt.innerHTML =k;
        main_table.data["Shift"].append(opt);
    }
    change_values(null, main_table, results, needs, volumes, aht, trend, plan_section, input, hc)
}

function create_table(parent, columns, plan_section) {
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
            container.className = "border border-secondary pt-4 pl-4 pr-4 text-center bg-dark";
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
    container.append(plan_section);
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
    container.append(canvas);
    d_flex.append(container);
    document.getElementById(parent).append(d_flex);
    var xValues = [...Array(24).keys()].map(i => (i <= 9) ? `0${i}:00` : `${i}:00`);
    var chart = new Chart("canvas", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [
                {
                    label: "Need",
                    data: [],
                    borderColor: "red",
                    fill: false
                },
                {
                    label: "Actual",
                    data: [],
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
    d_flex.data["chart"] = chart;
    return d_flex;
}

function run() {
    var planning = planning_section(
        columns=["Total HC", "Shift", "Days", "Off Day"],
        values=[]
    );
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
        },
        plan_section=planning
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
        main_table=analysis,
        plan_section=planning
    );
    var col = collapse("main", {"Input": input, "Analysis": analysis});
}

run();

