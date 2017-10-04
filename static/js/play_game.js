
$.get( "/admin/get_current_game", function( data ) {
    //alert( "game data:" + data );
    loadGame(data);
});


//####################//
//                    //
//        class       //
//                    //
//####################//
function Point(x,y)
{
    this.x = x;
    this.y = y;
}

var currentGame;

var canvas  = canvas = document.getElementById("myCanvas");
var ctx     = canvas.getContext("2d");
var imgBg   = document.getElementById("bg");
var imgBall = document.getElementById("ball");

//#########################################//
//                                         //
//      print pixel of mouse in logs       //
//                                         //
//#########################################//

// canvas.addEventListener('mousemove', function(evt) {
//        var mousePos = getMousePos(canvas, evt);
//      wwwzzsddda  var message = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;
//        console.log(message);
// }, false);


var ball = new Point(365, 133);
ball.width = 80;
ball.height = 80;

//#########################################//
//                                         //
//               Mouse position            //
//                                         //
//#########################################//
function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}


//#################################################################//
//                                                                 //
//    canvas.addEventListener("keydown", handleKeyDown, true);     //
//                                                                 //
//#################################################################//
function drawScene() {



    console.log("Canvas: " + canvas.width + "X" + canvas.height);

    // use this trick to clear canvas
    canvas.width = canvas.width;
    //canvas.height = canvas.height;

    //#########################################//
    //                                         //
    //         drawing background image        //
    //                                         //
    //#########################################//
    ctx.drawImage(imgBg, 0, 0);

    //#########################################//
    //                                         //
    //         draw eye lines to ball          //
    //                                         //
    //#########################################//
    var eyes = currentGame.eyes;
    for(var i=0; i < eyes.length; i++) {
        var eye = eyes[i];
        //ctx.rect(eye.x, eye.y, 2, 2);
        //ctx.stroke();

        ctx.moveTo(eye.x, eye.y);
        ctx.lineTo(ball.x + ball.width/2, ball.y + ball.height/2);
        ctx.stroke();
    }


    //#########################################//
    //                                         //
    //                drawing ball             //
    //                                         //
    //#########################################//
    ctx.drawImage(imgBall, ball.x, ball.y);

    setBallInForm();

}//drawScene

function logGame(game) {
    console.log("Pic: " + game.pic);
    console.log("Eyes: " + game.eyes);
}


function loadGame(data) {

    console.log("Data: " + data);

    var gameInfo = JSON.parse(data);
    currentGame = gameInfo.game;
    logGame(currentGame);

    $("#bg").attr('src', currentGame.pic);
    drawScene();
}


document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38') {
        console.log("-- up --");
        moveUp();
    }
    else if (e.keyCode == '40') {
        console.log("-- down --");
        moveDown();
    }
    else if (e.keyCode == '37') {
        console.log("-- left --");
        moveLeft();
    }
    else if (e.keyCode == '39') {
        console.log("-- right --");
        moveRight();
    }

}

function moveLeft() {
    if(ball.x -5 < 0) return;
    ball.x -= 5;
    drawScene();
}

function moveRight() {
    if(ball.x + ball.width + 5 > canvas.width) return;
    ball.x += 5;
    drawScene();
}

function moveUp() {
    if(ball.y -5 < 0) return;
    ball.y -= 5;
    drawScene();
}

function moveDown() {
    if(ball.y + ball.height + 5 > canvas.height) return;
    ball.y += 5;
    drawScene();
}
function setBallInForm(){
     var ball_x = document.getElementById("ball_x");
     ball_x.value = "" + ball.x;

 var ball_y= document.getElementById("ball_y");
     ball_y.value = "" + ball.y;

}
//#########################################//
//                                         //
//            move ball with key           //
//                                         //
//#########################################//
window.addEventListener( "keypress", handleKeyup, false );

function handleKeyup(e) {

    console.log( "key" + e.keyCode );

    if (e.keyCode == 97) { // a
        moveLeft();
    }

    if (e.keyCode == 100) { // d
        moveRight();
    }

    if (e.keyCode == 119) { // w
        moveUp();
    }

    if (e.keyCode == 122) { // z
        moveDown();
    }

}
