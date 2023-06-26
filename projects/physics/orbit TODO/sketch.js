const G = 6.67 * (10 ** -11);

let bodies = [];


function setup() {
    createCanvas(windowWidth, windowHeight);

    // bodies.push(new Body(random(width), random(height), 7.34767309 * 10 ** 22))  
    bodies.push(new Body(random(width), random(height), 5.972 * 10 ** 23))
    bodies.push(new Body(random(width), random(height), 5.972 * 10 ** 23))

    // for (let i = 0; i < 20; i++) {
        // bodies.push(new Body(random(width), random(height), 5.972 * 10 ** 10));
    // }
}

function draw() {
    background(0)

    bodies[1].setPos(mouseX, mouseY)

    for (let body of bodies) {
        body.update()
        body.show()

        for (let other of bodies) {
            if (body == other) 
                continue;

            body.orbit(other)
        }
    }
}