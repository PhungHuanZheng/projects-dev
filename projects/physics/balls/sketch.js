let ball;


function setup() {
    createCanvas(windowWidth, windowHeight);
    
    ball = new Ball(width / 2, height / 2, 32);
}

function draw() {
    frameRate(60);
    background(0);
    
    ball.acc = createVector(0, 9.8 / 60)
    ball.update()

    if (mouseIsPressed) {
        ball.swing(mouseX, mouseY)
    } else {
        ball.internalTimer = 0
    }

    ball.show()
}