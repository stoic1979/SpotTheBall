var canvas;
var ctx;
var imgBg;
var imgBall;
var eyes = [];
var ballX = 100;
var ballY = 100;

var itemIndex;


function setupGameCreator() {
    // draw image on canvas
    console.log("setupGameCreator");

    canvas  = canvas = document.getElementById("myCanvas");
    ctx     = canvas.getContext("2d");
    imgBg   = document.getElementById("bg");
    imgBall = document.getElementById("ball");


    canvas.addEventListener("click", onClick, false);

}

function drawScene() {
    //#########################################//
    //                                         //
    //         drawing background image        //
    //                                         //
    //#########################################//
    ctx.drawImage(imgBg, 0, 0);

    ctx.drawImage(imgBall, ballX, ballY);
}


function onClick(evt) {

    var rect = canvas.getBoundingClientRect();
    var x = evt.clientX - rect.left;
    var y = evt.clientY - rect.top;
    x = parseInt(x);
    y = parseInt(y);

    console.log("(" + x + "," + y + ")");

    var x1 = document.getElementById("x" + itemIndex);
    var y1 = document.getElementById("y" + itemIndex);
    x1.value = "" + x;
    y1.value = "" + y;

}

function setSelectedItem(val) {
    itemIndex = val;
    
   // alert("setSelectedItem: " + val);
}

  

//-------------------------------------
// Window Loaded
//-------------------------------------
window.onload = function(e){
    canvas  = canvas = document.getElementById("myCanvas");
    setupGameCreator();
    drawScene();
};
