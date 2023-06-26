let ropes = []


function setup() {
    createCanvas(windowWidth, windowHeight);

    for (let i = 0; i < 1; i++) {
        ropes.push(new Rope(100, 100 + (i * 50), 10, 10, 0.1));
        ropes[i].getNode(0).isFixed = true
    }
}

function draw() {
    background(0);

    for (let rope of ropes) {
        rope.update();
        rope.getNode(9).pos = createVector(mouseX, mouseY)

        rope.show()
    }

}