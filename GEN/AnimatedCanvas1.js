class Point {
	constructor( xpos, ypos, xvel, yvel, size, ttl) {
		this.xpos = xpos;
		this.ypos = ypos;
		this.xvel = xvel;
		this.yvel = yvel;
		this.MaxSize = size;
		this.dttl = 4/Math.pow(ttl,2);
		this.ottl = ttl ;
		this.cttl = ttl ;
	}
	size(){
		return this.intensity()*this.MaxSize;
	}
	update(dt) { 
		this.xpos += dt*this.xvel;
		this.ypos += dt*this.yvel;
		this.cttl -= dt;
	}
	intensity(){
		return Math.max((this.cttl)*(this.ottl-this.cttl)*this.dttl, 0.01);
	}
}

var	AnimatedCanvas1 = {
	AllPoints : [],
	minSize: 3,
	maxSize: 8,
	density: .0001,
	entityCap: 0,
	TicksPerSecond: 60,
	SecondsPerTick: 1/60,//1000/AnimatedCanvas1.TicksPerSecond,
	AvgTTl: 16,
	AvgVel: 4,
	minRGB: 0x0F8A88,
	maxRGB: 0xc0ffee,
	linkLength: 96,
	mouseDown: 0,
	mouseX: 0,
	mouseY: 0,
}
	
function sRGB( min, max, ratio ){
	delta = max-min;
	tempString = (min+(((delta&0xff0000)*ratio)&0xff0000)+(((delta&0x00ff00)*ratio)&0x00ff00)+(((delta&0x0000ff)*ratio)&0x0000ff)).toString(16);
	while (tempString.length < 6) { tempString = "0"+ tempString;}
	return "#"+ tempString;
}

function gR(low, high){
	return Math.random()*(high-low) + low;
}

function createPointAtMouse(){
	if( AnimatedCanvas1.mouseDown == 0){
		return;
	}
	AnimatedCanvas1.AllPoints.push( new Point( 
		AnimatedCanvas1.mouseX, AnimatedCanvas1.mouseY, 
		gR(-5,5)*AnimatedCanvas1.AvgVel, gR(-5,5)*AnimatedCanvas1.AvgVel, 
		gR(AnimatedCanvas1.minSize,AnimatedCanvas1.maxSize), gR(AnimatedCanvas1.AvgTTl*0.2,AnimatedCanvas1.AvgTTl*0.6)) 
	);	
}

function EnableAnimatedCanvas1( CanvasElementID ){
	
	var canvas = document.getElementById(CanvasElementID);
	var ctx = canvas.getContext("2d");
	ctx.shadowBlur = 0;
	ctx.lineWidth = 2;
	
	AnimatedCanvas1.SecondsPerTick = 1/AnimatedCanvas1.TicksPerSecond;
	setInterval( AnimateCanvas1,     AnimatedCanvas1.SecondsPerTick*1000 , canvas, ctx);
	setInterval( createPointAtMouse, AnimatedCanvas1.SecondsPerTick*7000 , canvas, ctx);
		
	
	
	mosposf = function(event) {
		const rect = canvas.getBoundingClientRect();
		AnimatedCanvas1.mouseX = event.clientX - rect.left;
		AnimatedCanvas1.mouseY = event.clientY - rect.top;
	}
	
	canvas.addEventListener('mousedown', function(event) {
		AnimatedCanvas1.mouseDown = 1;
		mosposf(event);
		createPointAtMouse();
	});
	
	document.body.addEventListener('mouseup', function(event) {
		AnimatedCanvas1.mouseDown = 0;
	});
	
	document.body.addEventListener('mouseleave', function(event) {
		AnimatedCanvas1.mouseDown = 0;
	});
	
	document.body.addEventListener('mousemove', function(event) {
		mosposf(event);
	});
}

function AnimateCanvas1( canvas, ctx ){

	//Clear canvas and update internal size as needed
	if( canvas.width != canvas.scrollWidth || canvas.height != canvas.scrollHeight){
		canvas.width = canvas.scrollWidth;
		canvas.height = canvas.scrollHeight;
	} else {
		ctx.clearRect(0, 0, canvas.width, canvas.height)
	}
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
		AnimatedCanvas1.AllPoints.push( new Point( 
			gR( 10, canvas.width), gR(10, canvas.height), 
			gR(-1,1)*AnimatedCanvas1.AvgVel, gR(-1,1)*AnimatedCanvas1.AvgVel, 
			gR(AnimatedCanvas1.minSize,AnimatedCanvas1.maxSize), gR(AnimatedCanvas1.AvgTTl/2,AnimatedCanvas1.AvgTTl*1.5)) );	
	}

	//Update
	var dict = {}; //Key Format (int) = x+y*canvas.width
	var div = AnimatedCanvas1.linkLength;
	var lim = div*div;
	var ymult = Math.floor(canvas.width/div);

	for(i=0; i<AnimatedCanvas1.AllPoints.length; i++){
		AnimatedCanvas1.AllPoints[i].update(AnimatedCanvas1.SecondsPerTick);
		var r = AnimatedCanvas1.AllPoints[i];
		var index = Math.floor(r.xpos/div)+ymult*Math.floor(r.ypos/div);
		dict[index] = dict[index] || [];
		dict[index].push( [r.xpos, r.ypos, r.intensity()] )

		var dx,dy;
		for(dx=-1;dx<2;dx++){
			for(dy=-1;dy<2;dy++){
				if(dx==0&&dy==0) {continue;}
				if( dict[index+dx+dy*ymult] ) {
					dict[index+dx+dy*ymult].push( [r.xpos, r.ypos, r.intensity()] )
				}
			}
		}
	}

	for (var key of Object.keys(dict)) {
		var points = dict[key];
		var p1,p2;
		for(p1=0; p1<points.length;p1++){
			for(p2=p1+1; p2<points.length;p2++){
				var dist = Math.pow(points[p1][0]-points[p2][0],2) + Math.pow(points[p1][1]-points[p2][1],2); 
				if( dist <= lim){
					ctx.beginPath();
					ctx.strokeStyle = sRGB(AnimatedCanvas1.minRGB, AnimatedCanvas1.maxRGB, Math.min(Math.pow(1-dist/lim, 3), points[p1][2],points[p2][2]) );
					ctx.moveTo(points[p1][0], points[p1][1]);
					ctx.lineTo(points[p2][0], points[p2][1]);
					ctx.stroke();
				}
			}
		}
	}

	//Show the state
	for(i=0; i<AnimatedCanvas1.AllPoints.length; i++){
		ctx.beginPath();
		ctx.arc( AnimatedCanvas1.AllPoints[i].xpos, AnimatedCanvas1.AllPoints[i].ypos, AnimatedCanvas1.AllPoints[i].size(), 0, 2 * Math.PI, false);
		ctx.fillStyle = sRGB(AnimatedCanvas1.minRGB, AnimatedCanvas1.maxRGB, AnimatedCanvas1.AllPoints[i].intensity() *.9 );
		ctx.fill();
		ctx.lineWidth = 2;
		ctx.strokeStyle = sRGB(AnimatedCanvas1.minRGB, AnimatedCanvas1.maxRGB, AnimatedCanvas1.AllPoints[i].intensity() );
		ctx.stroke();
	}


}
