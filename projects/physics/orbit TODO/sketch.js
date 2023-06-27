const G = 10

let Earth, Moon;
let asteroids = [];


function setup() {
    createCanvas(windowWidth, windowHeight);

    Earth = new Body(width / 2, height / 2, 50);
    Moon = new Body(width - 150, height / 2, 10);

    for (let i = 0; i < 13; i++) {
        asteroids.push(new Body(100, (10 * i), 5));
        asteroids[i].vel.x = 1;
    }
}

function draw() {
    background(0);

    for (let asteroid of asteroids) {
        asteroid.orbit(Earth)
        // for (let other of asteroids) {
        //     if (asteroid == other) continue;
        //     asteroid.orbit(other);
        // }
        
        asteroid.update()
        asteroid.show(true)
    }

    Moon.show()
    Earth.show()
}

function mouseDragged() {
    Moon.pos = createVector(mouseX, mouseY)
}