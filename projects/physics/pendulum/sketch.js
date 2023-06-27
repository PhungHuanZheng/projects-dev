const G = 9.8;

let pendulum;

function setup() {
    createCanvas(windowWidth, windowHeight);
    
    pendulum = new Pendulum(width / 2, 0, 300, 20, PI / 2);
}

function draw() {
    background(0);

    pendulum.update(frameCount, 5)
    pendulum.show()
}