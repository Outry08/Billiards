let count = 0;
let timer;
let timeRate = 10;
let animating = false;
let drawing = false;
let turnNum;
let prevPlayerNum;
let playerNum;
let resetting = false;
let paused = false;
let prevP1Sunk = 0, prevP2Sunk = 0;
let low1 = -1;
let lowBallStats = "<p>Balls Remaining:</p> <table> <tr> <td> <img class=\"ballImg1 yellow\" src=\"yellowball.svg\" alt=\"Yellow Ball\"> </td> <td> <img class=\"ballImg1 blue\" src=\"blueball.svg\" alt=\"Blue Ball\"> </td> <td> <img class=\"ballImg1 red\" src=\"redball.svg\" alt=\"Red Ball\"> </td> <td> <img class=\"ballImg1 purple\" src=\"purpleball.svg\" alt=\"Purple Ball\"> </td> <td> <img class=\"ballImg1 orange\" src=\"orangeball.svg\" alt=\"Orange Ball\"> </td> <td> <img class=\"ballImg1 green\" src=\"greenball.svg\" alt=\"Green Ball\"> </td> <td> <img class=\"ballImg1 brown\" src=\"brownball.svg\" alt=\"Brown Ball\"> </td> <td style=\"display: none\"> <img class=\"black\" src=\"blackball.svg\" alt=\"Black Ball\" > </td> </tr> </table> <br> <p>Balls Sunk:</p> <table> <tr> <td> <img class=\"ballImg2 yellow\" src=\"yellowball.svg\" alt=\"Yellow Ball\"> </td> <td> <img class=\"ballImg2 blue\" src=\"blueball.svg\" alt=\"Blue Ball\"> </td> <td> <img class=\"ballImg2 red\" src=\"redball.svg\" alt=\"Red Ball\"> </td> <td> <img class=\"ballImg2 purple\" src=\"purpleball.svg\" alt=\"Purple Ball\"> </td> <td> <img class=\"ballImg2 orange\" src=\"orangeball.svg\" alt=\"Orange Ball\"> </td> <td> <img class=\"ballImg2 green\" src=\"greenball.svg\" alt=\"Green Ball\"> </td> <td> <img class=\"ballImg2 brown\" src=\"brownball.svg\" alt=\"Brown Ball\"> </td> </tr> </table>"
let highBallStats = "<p>Balls Remaining:</p> <table> <tr> <td> <img class=\"ballImg1 lightyellow\" src=\"lightyellowball.svg\" alt=\"Light Yellow Ball\"> </td> <td> <img class=\"ballImg1 lightblue\" src=\"lightblueball.svg\" alt=\"Light Blue Ball\"> </td> <td> <img class=\"ballImg1 pink\" src=\"pinkball.svg\" alt=\"Pink Ball\"> </td> <td> <img class=\"ballImg1 mediumpurple\" src=\"mediumpurpleball.svg\" alt=\"Medium Purple Ball\"> </td> <td> <img class=\"ballImg1 lightsalmon\" src=\"lightsalmonball.svg\" alt=\"Light Salmon Ball\"> </td> <td> <img class=\"ballImg1 lightgreen\" src=\"lightgreenball.svg\" alt=\"Light Green Ball\"> </td> <td> <img class=\"ballImg1 sandybrown\" src=\"sandybrownball.svg\" alt=\"Sandy Brown Ball\"> </td> <td style=\"display: none\"> <img class=\"black\" src=\"blackball.svg\" alt=\"Black Ball\"> </td> </tr> </table> <br> <p>Balls Sunk:</p> <table> <tr> <td> <img class=\"ballImg2 lightyellow\" src=\"lightyellowball.svg\" alt=\"Light Yellow Ball\"> </td> <td> <img class=\"ballImg2 lightblue\" src=\"lightblueball.svg\" alt=\"Light Blue Ball\"> </td> <td> <img class=\"ballImg2 pink\" src=\"pinkball.svg\" alt=\"Pink Ball\"> </td> <td> <img class=\"ballImg2 mediumpurple\" src=\"mediumpurpleball.svg\" alt=\"Medium Purple Ball\"> </td> <td> <img class=\"ballImg2 lightsalmon\" src=\"lightsalmonball.svg\" alt=\"Light Salmon Ball\"> </td> <td> <img class=\"ballImg2 lightgreen\" src=\"lightgreenball.svg\" alt=\"Light Green Ball\"> </td> <td> <img class=\"ballImg2 sandybrown\" src=\"sandybrownball.svg\" alt=\"Sandy Brown Ball\"> </td> </tr> </table>"
let firstLoad = true

$(document).ready(
    function () {
        // alert("Raring to go.");

        let queLine, queLine2;
        let queX, queY, queR;
        let mouseX, mouseY;

        // $("body").append("<button onclick=\"start()\">START</button>");
        // $("body").append("<button onclick=\"reset()\">RESET</button>");
        // $("body").append("<button onclick=\"pause()\">STOP</button><br>");
        // $("body").append("<button onclick=\"slow()\">SLOWMO</button><br>");
        // $("body").append("<button onclick=\"backToTitle()\">BACK TO TITLE</button><br>");

        turnNum = Number(($("#turnnum").text()))
        playerNum = Number(($("#playernum").text()))
        if (playerNum != 0) {
            $("#p" + (3 - playerNum) + "name")[0].style.fontSize = "30px";
            $("#p" + (playerNum) + "name")[0].style.fontSize = "50px";
        }
        prevPlayerNum = playerNum;
        low1 = Number(($("#p1low").text()))
        if (low1 == 1) {
            low1 = true
            $("#p1stuff").html(lowBallStats);
            $("#p2stuff").html(highBallStats);
        }
        else if (low1 == 2) {
            low1 = false
            $("#p1stuff").html(highBallStats);
            $("#p2stuff").html(lowBallStats);
        }
        // console.log(turnNum)

        addEventListeners();
        firstLoad = false;

        // function getMousePositionSVG(event, offsetX, offsetY) {

        //     var point = document.createElementNS('http://www.w3.org/2000/svg', 'svg').createSVGPoint();
        //     var offPoint = document.createElementNS('http://www.w3.org/2000/svg', 'svg').createSVGPoint();
        //     point.x = event.clientX - offsetX;
        //     point.y = event.clientY - offsetY;
        //     point = point.matrixTransform(document.createElementNS('http://www.w3.org/2000/svg', 'svg').getScreenCTM().inverse());
        //     offPoint.x = offsetX;
        //     offPoint.y = offsetY;
        //     offPoint = offPoint.matrixTransform(document.createElementNS('http://www.w3.org/2000/svg', 'svg').getScreenCTM().inverse());
        //     // console.clear();
        //     // console.log(point.x, point.y);
        //     // point.x -= offPoint.x;
        //     // point.y -= offPoint.y;
        //     return point;
        // }
    }
);

function addEventListeners(firstLoad) {
    if (!resetting)
        turnNum++;
    console.log("Turn Number: " + turnNum);
    if (document.getElementById("que") != null)
        document.getElementById("que").addEventListener("mousedown", function (event) {
            // <width=((document.getElementById("que").x + event.pagex) / 2) height=100px x= + event.pageX +  y= + event.pageY + fill=white
            // console.log("Happy");
            if (!animating) {
                const svgns = "http://www.w3.org/2000/svg";
                drawing = true;

                let que = document.getElementById("que")
                queLine = document.createElementNS(svgns, "line");
                queLine2 = document.createElementNS(svgns, "line");
                // console.log(event.target.x)
                queR = parseFloat(que.getAttribute("r"))
                queX = parseFloat(que.getAttribute("cx"))
                queY = parseFloat(que.getAttribute("cy"))
            }

        })

    document.addEventListener("mousemove", function (event) {
        if (drawing) {
            // console.log(document.getElementsByTagName("svg")[0].getAttribute("viewBox"));
            viewX = parseFloat(document.getElementsByTagName("svg")[0].getAttribute("viewBox").toString().split(" ")[2])
            viewY = parseFloat(document.getElementsByTagName("svg")[0])

            var rect = document.getElementsByTagName("svg")[0].getBoundingClientRect();
            mouseX = (event.clientX - rect.left) * 2 * (1375 / (rect.bottom - rect.top)) - queR
            mouseY = (event.clientY - rect.top) * 2 * (1375 / (rect.bottom - rect.top)) - queR

            queLine.setAttribute("x1", queX);
            queLine.setAttribute("x2", mouseX);
            queLine.setAttribute("y1", queY);
            queLine.setAttribute("y2", mouseY);
            queLine.setAttribute("stroke", "orange");
            queLine.setAttribute("stroke-width", 20);

            queLine2.setAttribute("x1", queX);
            queLine2.setAttribute("x2", mouseX - (4 * (mouseX - queX)));
            queLine2.setAttribute("y1", queY);
            queLine2.setAttribute("y2", mouseY - (4 * (mouseY - queY)));
            queLine2.setAttribute("stroke", "white");
            queLine2.setAttribute("stroke-width", 5);

            // console.log(event)

            // console.log("Que X: " + queX + " Que Y: " + queY + "\nMouse X: " + mouseX + " Mouse Y: " + mouseY)

            queLine.setAttribute("class", "shotRect");
            queLine2.setAttribute("class", "shotRect");
            // alert("time to draw")
            document.getElementsByTagName("svg")[0].append(queLine)
            document.getElementsByTagName("svg")[0].append(queLine2)

        }
    });

    document.addEventListener("mouseup", function (event) {
        if (drawing) {
            $(".shotRect").remove();
            drawing = false;
            animating = true;
            let xhr = new XMLHttpRequest()
            let url = "/anim.html"
            xhr.open("POST", url, true)
            xhr.setRequestHeader("Content-Type", "application.json")

            // myData = [turnNum, queX, queY, mouseX, mouseY, playerNum, low1]
            myData = [turnNum, queX, queY, mouseX, mouseY, playerNum, $("#gamename").text()]

            myDataS = JSON.stringify(myData)

            xhr.send(myDataS)
            // if (xhr.readyState == 4) {
            //     console.log("HEHEHHEHE");
            // }

            // form = document.createElement("form");
            // form.setAttribute("method", "GET");
            // form.setAttribute("action", "anim.html")
            // tNum = document.createElement("input")
            // tNum.setAttribute("name", "turnNum")
            // tNum.setAttribute("value", turnNum)
            // x1 = document.createElement("input")
            // x1.setAttribute("name", "x1")
            // x1.setAttribute("value", queX)
            // y1 = document.createElement("input")
            // y1.setAttribute("name", "y1")
            // y1.setAttribute("value", queY)
            // x2 = document.createElement("input")
            // x2.setAttribute("name", "x2")
            // x2.setAttribute("value", mouseX)
            // y2 = document.createElement("input")
            // y2.setAttribute("name", "y2")
            // y2.setAttribute("value", mouseY)
            // form.append(tNum)
            // form.append(x1)
            // form.append(y1)
            // form.append(x2)
            // form.append(y2)
            // $("body").append(form)
            // // $.post("anim.html")
            // $(".shotRect").remove();

            // form.submit()

            wait();

            // start();

        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key == "Escape" && drawing) {
            $(".shotRect").remove();
            drawing = false;
        }
    });

    if (!resetting)
        checkBalls();
    // if (turnNum == 1)
    //     switchPlayers();

}

function checkBalls() {

    let allGoneP1 = $("#p1stuff").html() != "";
    let allGoneP2 = $("#p2stuff").html() != "";
    let lowBallsSunk = 7, highBallsSunk = 7;

    // console.log($("#p1stuff").html() == "")

    if ($("#p1stuff").html() != "") {
        for (let i = 0; i < 14; i++) {
            $(".ballImg2")[i].parentElement.style.display = "initial";
            $(".ballImg1")[i].parentElement.style.display = "none";
        }
    }

    for (let i = 0; i < $(".black").length; i++) {
        // $(".black")[i].parentElement.style.display = "none";
    }


    for (let i = 0; i < $(".ball").length; i++) {
        let color = $(".ball")[i].getAttribute("fill");

        if (color != "WHITE" && color != "BLACK") {
            // console.log(color, $("." + color))
            if ($("#p1stuff").html() != "") {
                $("." + color)[0].parentElement.style.display = "initial";
                $("." + color)[1].parentElement.style.display = "none";
            }
            if (color == "YELLOW" || color == "RED" || color == "BLUE" || color == "BROWN" || color == "PURPLE" || color == "ORANGE" || color == "GREEN") {
                // console.log(color);
                if (low1 == true)
                    allGoneP1 = false;
                else if (low1 == false)
                    allGoneP2 = false;
                lowBallsSunk--;
            }
            else {
                // console.log(color);
                if (low1 == true)
                    allGoneP2 = false;
                else if (low1 == false)
                    allGoneP1 = false;
                highBallsSunk--;
            }
        }
    }

    if ($("#p1stuff").html() == "") {
        if (lowBallsSunk > highBallsSunk) {
            if (playerNum == 1) {
                console.log("Low for p1");
                $("#p1stuff").html(lowBallStats);
                $("#p2stuff").html(highBallStats);
                low1 = true;
            }
            else {
                console.log("Low for p2");
                $("#p1stuff").html(highBallStats);
                $("#p2stuff").html(lowBallStats);
                low1 = false;
            }
        }
        else if (highBallsSunk > lowBallsSunk) {
            if (playerNum == 1) {
                console.log("High for p1");
                $("#p1stuff").html(highBallStats);
                $("#p2stuff").html(lowBallStats);
                low1 = false;
            }
            else {
                console.log("High for p2");
                $("#p1stuff").html(lowBallStats);
                $("#p2stuff").html(highBallStats);
                low1 = true;
            }
        }
    }

    // console.log(allGoneP1, allGoneP2)

    if (!animating && !resetting) {
        if (allGoneP1) {
            if (blackExists()) {
                $(".black")[0].parentElement.style.display = "initial";
            }
            else if (playerNum == 1) {
                if ((low1 == true && (lowBallsSunk == prevP1Sunk)) || (low1 == false && (highBallsSunk == prevP1Sunk))) {
                    theWinnerIs(1, 1);
                }
                else {
                    theWinnerIs(2, 2);
                }
            }
        }
        if (allGoneP2) {
            if (blackExists()) {
                $(".black")[1].parentElement.style.display = "initial";
            }
            else if (playerNum == 2) {
                if (highBallsSunk == prevP2Sunk) {
                    theWinnerIs(2, 1);
                }
                else {
                    theWinnerIs(1, 2);
                }
            }
        }

        if (!allGoneP2 && !allGoneP1 && !blackExists()) {
            theWinnerIs(3 - playerNum, 2);
        }

        if (!(((low1 == true && lowBallsSunk > prevP1Sunk && playerNum == 1) || (low1 == false && highBallsSunk > prevP1Sunk && playerNum == 1)) || ((low1 == true && highBallsSunk > prevP2Sunk && playerNum == 2) || (low1 == false && lowBallsSunk > prevP2Sunk && playerNum == 2)))) {
            switchPlayers();
        }

        if (low1 == true) {
            prevP1Sunk = lowBallsSunk;
            prevP2Sunk = highBallsSunk;
        }
        else if (low1 == false) {
            prevP1Sunk = highBallsSunk;
            prevP2Sunk = lowBallsSunk;
        }

    }


}

function switchPlayers() {
    // console.log(turnNum);
    // console.log(playerNum);
    if (turnNum == 1 && playerNum == 0) {
        playerNum = Math.floor(Math.random() * 2) + 1;
        prevPlayerNum = playerNum;
    }
    else if (!firstLoad) {
        prevPlayerNum = playerNum;
        playerNum = 3 - playerNum;

        console.log("PLayer " + playerNum + "'s turn now.")
    }
    // console.log(playerNum);
    // console.log("#p" + (3 - playerNum) + "name");
    // console.log($("#p" + (3 - playerNum) + "name"));
    // console.log($("#p" + (3 - playerNum) + "name")[0].style);
    $("#p" + (3 - playerNum) + "name")[0].style.fontSize = "30px";
    $("#p" + (playerNum) + "name")[0].style.fontSize = "50px";
}

function blackExists() {
    for (let i = 0; i < $(".ball").length; i++) {
        let color = $(".ball")[i].getAttribute("fill");
        if (color == "BLACK")
            return true;
    }

    return false;

}

function theWinnerIs(playerNumber, endInt) {

    // console.log("GAME OVER");
    form = document.createElement("form");
    form.setAttribute("method", "GET");
    form.setAttribute("action", "/victory.html")
    form.style.display = "none"
    winner = document.createElement("input")
    winner.setAttribute("name", "winner")
    winner.setAttribute("value", $("#p" + playerNumber + "name").text())
    loser = document.createElement("input")
    loser.setAttribute("name", "loser")
    loser.setAttribute("value", $("#p" + (3 - playerNumber) + "name").text())
    endInfo = document.createElement("input")
    endInfo.setAttribute("name", "endinfo")
    endInfo.setAttribute("value", endInt)
    gameName = document.createElement("input")
    gameName.setAttribute("name", "gamename")
    gameName.setAttribute("value", $("#gamename").text())

    // console.log("THE WINNER IS: " + $("#p" + playerNumber + "name").text())

    form.append(winner);
    form.append(loser);
    form.append(endInfo);
    form.append(gameName);

    $("body").append(form);

    form.submit()
}

function animate() {
    let xmlSrting
    // for (var i = 0; i < numSVGs; i++) 
    // sleepFor(1);

    // console.log(count)
    // $(".ball").remove()
    // console.log("Removed one");
    if (count < 10) {
        svgRequest = $.get("table0" + count + ".svg", function (data) {
            xmlString = (new XMLSerializer()).serializeToString(data);

            // console.log(xmlString.slice(xmlString.search("<circle class=\"ball\" "), xmlString.search("</svg>")));
            $("svg").remove()
            $("#svgCell").append(xmlString);
            checkBalls();
        });
        svgRequest.fail(end)
    }
    else {
        svgRequest = $.get("table" + count + ".svg", function (data) {
            xmlString = (new XMLSerializer()).serializeToString(data);
            $("svg").remove()
            $("#svgCell").append(xmlString);
            checkBalls();
        });
        svgRequest.fail(end)
    }

    count++;
}

function start() {
    if ((resetting || paused) && !animating) {
        timer = setInterval(animate, timeRate);
        paused = false
    }
}

function wait() {
    waitTimer = setInterval(stopWait, 7000)
}
function stopWait() {
    clearInterval(waitTimer)
    timer = setInterval(animate, timeRate);
    paused = false
}
function reset() {
    // if (!resetting && turnNum > 1) {
    //     turnNum--;
    //     playerNum = prevPlayerNum;
    // }
    if (!animating) {
        resetting = true;
        paused = false;
        clearInterval(timer);
        count = 0;
        animate();
    }
}
function end() {
    clearInterval(timer);
    animating = false;
    count = 0;
    addEventListeners()
    resetting = false;
}
function pause() {
    if (!animating) {
        paused = true;
        clearInterval(timer);
    }
}
// function backToTitle() {
//     form = document.createElement("form");
//     form.setAttribute("method", "GET");
//     form.setAttribute("action", "/title.html")
//     tNum = document.createElement("input")
//     tNum.setAttribute("name", "turnNum")
//     tNum.setAttribute("value", turnNum)

//     form.append(tNum)
//     $("body").append(form)
//     // $.post("anim.html")
//     $(".shotRect").remove();

//     form.submit()
// }

function slow() {
    if (resetting) {
        if (!paused) {
            pause()
            if (timeRate != 10)
                timeRate = 10;
            else
                timeRate = 100;

            start()
        }
        else {
            if (timeRate != 10)
                timeRate = 10;
            else
                timeRate = 100;
        }
    }
}

function backToTitle() {
    if (!animating) {
        form = document.createElement("form");
        form.setAttribute("method", "GET");
        form.setAttribute("action", "/title.html")
        form.style.display = "none"
        p1low = document.createElement("input")
        p1low.setAttribute("name", "p1low")
        p1low.setAttribute("value", low1)
        pNum = document.createElement("input")
        pNum.setAttribute("name", "playernum")
        pNum.setAttribute("value", playerNum)
        gameName = document.createElement("input")
        gameName.setAttribute("name", "gamename")
        gameName.setAttribute("value", $("#gamename").text())
        // console.log("THE WINNER IS: " + $("#p" + playerNumber + "name").text())

        form.append(p1low);
        form.append(pNum);
        form.append(gameName);

        $("body").append(form);

        form.submit()
    }
}

