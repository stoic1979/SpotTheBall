var canvas;
var ctx;
var imgBg;
var imgBall;

var ballX 		= 100;
var ballY 		= 100;
var ballWidth   = 80;
var ballHeight  = 80;

var curIndex;
var curType = "";

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


//-----------------------------------------------
// initially we have 8 eyes with default values
//-----------------------------------------------
var eyes = [
	 new Point(-1, -1),
 	 new Point(-1, -1),
	 new Point(-1, -1),
	 new Point(-1, -1),
	 new Point(-1, -1),
	 new Point(-1, -1),
	 new Point(-1, -1),
	 new Point(-1, -1)
];



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


    //#########################################//
    //                                         //
    //         draw eye rect and               //
    //         eye lines to ball               //
    //                                         //
    //#########################################//
    for(var i=0; i < eyes.length; i++) {
        var eye = eyes[i];

		if(eye.x == -1 || eye.y == -1) continue;

		console.log("EYE: " + eye.x + "," + eye.y);

		ctx.beginPath();
		if(curType == "EYE" && curIndex-1 == i) {
			ctx.strokeStyle="red";
			console.log("red");
		} else {
			ctx.strokeStyle="#000";
			console.log("black");
		}

		ctx.rect(eye.x-5, eye.y-5, 10, 10);
        //ctx.stroke();

        ctx.moveTo(eye.x, eye.y);
        ctx.lineTo(ballX + ballWidth/2, ballY + ballHeight/2);

	

        ctx.stroke();
    }
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
		eyes[curIndex-1].x = x;
		eyes[curIndex-1].y = y;
	} else {
		x1 = document.getElementById("ball_x");
	    y1 = document.getElementById("ball_y");
		ballX = x - ballWidth/2;
		ballY = y - ballHeight/2;		
	}

    x1.value = "" + x;
    y1.value = "" + y;

	drawScene();
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
