const COHERENCE = 0.025
const SEPARATION = 0.001


let flock;

function setup() {
    createCanvas(windowWidth, windowHeight);
    
    flock = new Flock(20, 100, COHERENCE, SEPARATION, 1, 5);
}

function draw() {
    background(0)

    flock.update()
    flock.show()
}