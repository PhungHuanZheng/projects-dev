let cloth;
let selected;

function setup() {
    createCanvas(windowWidth, windowHeight);

    cloth = new Cloth(10, 5, 40, 0.2)
}

function draw() {
    background(0)

    for (let pt of cloth.data.flat()) {
        pt.update()
    }
    cloth.update()
    cloth.show()
}

function mousePressed() {
    // iterate over points in cloth
    for (let pt of cloth.data.flat()) {
        // if point is fixed, ignore
        if (pt.isFixed) continue;

        // if within selection distance
        let d = dist(mouseX, mouseY, pt.canvasX, pt.canvasY);
        if (d < pt.selectionDist / 2) {
            pt.isBeingDragged = true;
            selected = pt;
        }
    }
}

function mouseReleased() {
    if (!selected) return;

    selected.isBeingDragged = false;
    selected = undefined;
}

function keyPressed() {
    // iterate over points in cloth
    for (let pt of cloth.data.flat()) {
        // if within selection distance
        let d = dist(mouseX, mouseY, pt.canvasX, pt.canvasY);
        if (d < pt.selectionDist / 2) {
            pt.isFixed = !pt.isFixed;
        }
    }
}