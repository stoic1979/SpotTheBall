var canvas;
var ctx;
var imgBg;
var imgBall;

var eyes 	 	= [];
var ballX 		= 100;
var ballY 		= 100;
var ballWidth   = 80;
var ballHeight  = 80;

var curIndex;
var curType = "";


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


	//------------------------------------
	// magical way of clearing canvas !!!
	//------------------------------------
	canvas.width = canvas.width;

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
	
	var x1, y1;

		if(curType == "EYE") {
    	 	x1 = document.getElementById("x" + curIndex);
	     	y1 = document.getElementById("y" + curIndex);
		} else {
			x1 = document.getElementById("ball_x");
	        y1 = document.getElementById("ball_y");
			ballX = x - ballWidth/2;
			ballY = y - ballHeight/2;
			drawScene();
		}

    x1.value = "" + x;
    y1.value = "" + y;
}

function setSelectedItem(type, val) {

	console.log("setSelectedItem: type=" + type + ", val=" + val);

	curType = type;
	curIndex = val;
   
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
