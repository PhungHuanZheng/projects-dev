let cloth;
let selected;


function setup() {
    createCanvas(windowWidth, windowHeight);

    cloth = new Cloth(20, 10, 30, 0.9);
    cloth.addFixtures([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19])
}

function draw() {
    background(0);

    cloth.update()
    cloth.show()
}

function mousePressed() {
    // for (let node of cloth.flatNodes) {
    //     let d = dist(mouseX, mouseY, node.pos.x, node.pos.y);
    //     if (d < node.selectionRadius) {
    //         selected = node;
    //         node.pos = createVector(mouseX, mouseY)
    //         break
    //     }
    // }
}

function mouseReleased() {
}

function keyPressed() {
}