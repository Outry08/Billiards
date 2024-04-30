function getNames() {
    $("img").remove()
    $("h3").remove()
    $("button").remove()
    $("br").remove()
    $("body").append("<form action=\"shoot.html\" method=\"get\"><h3> Player Names: </h3><label for=\"gamename\">Game Name: </label><input type=\"text\" id=\"gamename\" name=\"gamename\" size=\"10\" /><br><label for=\"p1name\">Player 1 Name: </label><input type=\"text\" id=\"p1name\" name=\"p1name\" size=\"10\" /><br><label for=\"p2name\">Player 2 Name: </label><input type=\"text\" id=\"p2name\" name=\"p2name\" size=\"10\" /><h3> <input type=\"submit\" value=\"Let's Play!\" /> </h3></form>")
    $("body").append("<button style=\"font-size:40px;\"onclick=\"goBack()\">BACK</button>")
}

function chooseGame() {
    $("img").remove()
    $("h3").remove()
    $("button").remove()
    $("br").remove()
    $("body").append("<h3>Choose your game:</h3>")
    "YEET"
    $("body").append("<br><button style=\"font - size: 40px; \"onclick=\"goBack()\">BACK</button>")
}

function goBack() {
    $("form").remove()
    $("button").remove()
    $("h3").remove()
    $("br").remove()
    $("body").append("<h3>By: Ryan Mckinnon</h3>")
    $("body").append("<img src=\"titleTable.svg\" alt=\"Pool Table\"><br>")
    $("body").append("<button onclick=\"getNames()\">NEW GAME</button>")
    $("body").append("<button onclick=\"chooseGame()\">CONTINUE</button>")
}

function loadGame(event) {
    // let xhr = new XMLHttpRequest()
    // let url = "/shoot.html"
    // xhr.open("POST", url, true)
    // xhr.setRequestHeader("Content-Type", "application.json")
    
    // myData = [$(event.target).text()]
    // console.log(myData)
    // myDataS = JSON.stringify(myData)

    // xhr.send(myDataS)

    form = document.createElement("form");
    form.setAttribute("method", "GET");
    form.setAttribute("action", "shoot.html")
    gameName = document.createElement("input")
    gameName.setAttribute("name", "gamename")
    gameName.setAttribute("value", $(event.target).text())
    form.append(gameName)
    $("body").append(form)

    form.submit()
}