
// set up the drawing technology
var renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);

document.body.appendChild( renderer.domElement );


// set up the scene

var scene = new THREE.Scene();

var geometry = new THREE.BoxGeometry(1,1,1);

var mycolors =
{
	//GOLD: 0xBAB51
GOLD: 0xff00ff
	};
//mycolors.GOLD = 0xBAB518;

var material;

material_props = { color: mycolors.GOLD };
material = new THREE.MeshBasicMaterial( material_props );
//material = new THREE.LineBasicMaterial( material_props );
//material = new THREE.MeshPhongMaterial( material_props );

var phong_props = 
{
	color: 0xBAB518,
	specular: 0x009900,
	shininess: 30,
	shading: THREE.FlatShading
};
//material = new THREE.MeshPhongMaterial( phong_props );

//material = new THREE.MeshPhongMaterial( { color: 0xdddddd, specular: 0x009900, shininess: 30, shading: THREE.FlatShading } );

var cube = new THREE.Mesh(geometry, material);

scene.add(cube);


// setup scene animation
function tick()
{
	cube.rotation.x += .01;
	cube.rotation.y += .02;
}

// set up the view

var camera = new THREE.PerspectiveCamera(
	75,
	window.innerWidth / window.innerHeight, 0.1, 1000 );
	
camera.position.z = 5;


// set up the animation loop
function render()
{
	requestAnimationFrame(render);
	renderer.render(scene,camera);
	
	tick();
}

// run

render();
