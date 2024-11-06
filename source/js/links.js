function shuffle(arr) {
    let i = arr.length;
    while (i) {
        let j = Math.floor(Math.random() * i--);
        [arr[j], arr[i]] = [arr[i], arr[j]];
    }
}

function renderlink(data) {
    var name, avatar, site, li = "";
    shuffle(data);
    for (var i = 0; i < data.length; i++) {
        name = data[i].name;
        avatar = data[i].avatar;
        site = data[i].site;
        tip = data[i].tip ? data[i].tip : "";
        // const li_str = `
        //     <div class="card hover-tip">
        //         <a href="${site}" target="_blank>"
        //             <div class="thumb" style="background: url('${avatar}');"></div>
        //         </a>
        //         <div class="card-header">
        //             <div>
        //                 <a href="${site}" target="_blank">${name}</a>
        //             </div>
        //         </div>
        //         <span class="tip-text">${tip}</span>
        //     </div>
        // `;
        li += '<div class="card hover-tip">' + '<a href="' + site + '" target="_blank">' + '<div class="thumb" style="background: url( ' + avatar + ');">' + '</div>' + '</a>' + '<div class="card-header">' + '<div><a href="' + site + '" target="_blank">' + name + '</a></div>' + '</div>' + '<span class="tip-text">' + tip + '</span></div>';
    }
    document.querySelector(".link-navigation").innerHTML = li;
}

fetch('/links/links.json')
    .then(response => response.json())
    .then(res => renderlink(res));
