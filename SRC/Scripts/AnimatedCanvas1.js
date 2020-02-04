class Point {
	constructor( xpos, ypos, xvel, yvel, size, ttl) {
		this.xpos = xpos;
		this.ypos = ypos;
		this.xvel = xvel;
		this.yvel = yvel;
		this.size = size;
		this.ottl = ttl ;
		this.cttl = ttl ;
		this.Neighbors = [];
	}
	update( othersPoints ) { 
		this.xpos+=this.xvel;
		this.ypos+=this.ypos;
		this.cttl--;
	
		// this.Neighbors = [];
		// var dist = 0;
		// for(i = 0; i<othersPoints.length; i++){
		// 	dist = (this.xpos - othersPoints[i].xpos())^2 + (this.ypos - othersPoints[i].ypos())^2;
		// 	if( dist < size*100) {
		// 		this.Neighbors.push(othersPoints[i]);
		// 	}
		// }
	}
	intensity(){
		return sqrt(-(this.cttl)(this.cttl - this.ottl)/ Math.pow(this.ottl/2, 2));
	}
}

var	AnimatedCanvas1 = {
	AllPoints : [],
	density: .001,
	entityCap: 0,
	TicksPerSecond: 1,
	MSPerTick: 0,//1000/AnimatedCanvas1.TicksPerSecond,
	AvgTTl: 10,
	ATL: 0 //AnimatedCanvas1.AvgTTl*AnimatedCanvas1.TicksPerSecond
}

function gR(low, high){
	return Math.floor( Math.random() * (high-low+1) )+ low;
}

function EnableAnimatedCanvas1( CanvasElementID ){
	AnimatedCanvas1.MSPerTick = 1000/AnimatedCanvas1.TicksPerSecond;
	AnimatedCanvas1.ATL = AnimatedCanvas1.AvgTTl*AnimatedCanvas1.TicksPerSecond;

	var canvas = document.getElementById(CanvasElementID);
	var ctx = canvas.getContext("2d");
	ctx.shadowBlur = 0;
	ctx.lineWidth = 2;
	
	setInterval( AnimateCanvas1, AnimatedCanvas1.MSPerTick , canvas, ctx);
}

function AnimateCanvas1( canvas, ctx ){

	canvas.width = canvas.scrollWidth;
	canvas.height = canvas.scrollHeight;
	AnimatedCanvas1.entityCap = canvas.height*canvas.width*AnimatedCanvas1.density;
	
	//Cull 
	var index = 0;
	while( index<AnimatedCanvas1.AllPoints.length ){
		if( AnimatedCanvas1.AllPoints[index].cttl <= 0){
			AnimatedCanvas1.AllPoints.splice(index, 1);
		} else {
			index++
		}
	}

	//Create
	while( AnimatedCanvas1.AllPoints.length < AnimatedCanvas1.entityCap ) {
		AnimatedCanvas1.AllPoints.push( new Point( gR( 10, canvas.width), gR(10, canvas.height), gR(-2,2), gR(-2,2), gR(2,5), gR(AnimatedCanvas1.ATL/2,AnimatedCanvas1.ATL*1.5)) );	
	}

	for(i =0; i<AnimatedCanvas1.AllPoints.length; i++){
		AnimatedCanvas1.AllPoints[i].update( [] );
	}

	//Show the state
	for(i =0; i<AnimatedCanvas1.entityCap; i++){
		ctx.beginPath();
		ctx.arc( AnimatedCanvas1.AllPoints[i].xpos, AnimatedCanvas1.AllPoints[i].ypos, AnimatedCanvas1.AllPoints[i].size, 0, 2 * Math.PI, false);
		ctx.fillStyle = 'blue';
		ctx.fill();
		ctx.lineWidth = 2;
		ctx.strokeStyle = 'black';
		ctx.stroke();
	}


}