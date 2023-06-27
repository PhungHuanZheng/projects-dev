const G = 9.8;

let pendulums = []

function setup() {
    createCanvas(windowWidth, windowHeight);

    for (let i = 0; i < 40; i++) {
        pendulums.push(new Pendulum(width / 2, 0, 20 + i * 20, 20, HALF_PI))
    }
}

function draw() {
    background(0);

    for (const p of pendulums) {
        p.update(frameCount, 5)
        p.show()
    }

}