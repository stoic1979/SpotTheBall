var canvas;
var ctx;
var imgBg;
var imgBall;

var ballX 		= 100;
var ballY 		= 100;
var ballWidth   = 80;
var ballHeight  = 80;

var curIndex = "1";
var curType = "EYE";

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

    if(curType == "BALL") {
		console.log("circle");
		ctx.beginPath();
		ctx.strokeStyle = "red";
		ctx.arc(ballX+ballWidth/2, ballY+ballWidth/2, ballWidth/2 + 5, 0,2*Math.PI);
		ctx.stroke();
	}



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
		if(curType == "EYE") {
			if(curIndex-1 == i) {
			ctx.strokeStyle="red";
			console.log("red");
			} else {
			ctx.strokeStyle="#000";
			console.log("black");
			}
		} else {
			ctx.strokeStyle="#000";
		}

        // dont remove this, we may need to draw rect in future
		// ctx.rect(eye.x-5, eye.y-5, 10, 10);
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

function resetAllTextColors() {
	for(var i=1; i<=8; i++) {
		setTextColor("EYE", i, "black"); 
	}

	setTextColor("BALL", 0, "black");
}

function setTextColor(type, val, col) {

	// ball color
	if(type == "BALL") {
		var a = document.getElementById("ball_x");
		a.style.color = col;

		var b = document.getElementById("ball_y");
		b.style.color = col;
	}

	if(type == "EYE") {
		var a = document.getElementById("x" + val);
		a.style.color = col;

		var b = document.getElementById("y" + val);
		b.style.color = col;
	}

}

function setSelectedItem(type, val) {

	console.log("setSelectedItem: type=" + type + ", val=" + val);

	resetAllTextColors();
	setTextColor(type, val, "red");

	curType = type;
	curIndex = val;

	drawScene();
   
	// alert("setSelectedItem: " + val);
}

function handleTextChanged(type, val) {
	console.log("handleTextChanged: type=" + type + ", val=" + val);

	//------------------------------------------
	// EYE
	//------------------------------------------
	if(type == "EYE") {

		var x = document.getElementById("x" + val);
		if(x.value.length > 0) {
			eyes[val-1].x = parseInt(x.value);
		}

		var y = document.getElementById("y" + val);
			if(y.value.length > 0) {
			eyes[val-1].y = parseInt(y.value);
		}
	}

	if(type == "BALL") {

		var x = document.getElementById("ball_x");
		if(x.value.length > 0) {
			ballX = parseInt(x.value);
		}

		var y = document.getElementById("ball_y");
			if(y.value.length > 0) {
			ballY = parseInt(y.value);
		}
	}

	drawScene();

}
  

//-------------------------------------
// Window Loaded
//-------------------------------------
window.onload = function(e){
    canvas  = canvas = document.getElementById("myCanvas");
    setupGameCreator();
    drawScene();
};
