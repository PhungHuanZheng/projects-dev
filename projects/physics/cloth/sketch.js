let cloth;
let selected;


function setup() {
    createCanvas(windowWidth, windowHeight);

    cloth = new Cloth(20, 10, 30, 1);
    cloth.addFixtures([0, 10, 19])
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