let grid;

function setup() {
    createCanvas(windowWidth, windowHeight);
    
    grid = new Grid(5, 5, 120);
}

function draw() {
    background(0);

    grid.show();
    grid.updateLiquids();
}

function mousePressed() {
    // convert canvas coords to grid coords
    let gridX = floor((mouseX - grid.startingX) / grid.cellLength);
    let gridY = floor((mouseY - grid.startingY) / grid.cellLength);

    // rotate at cell clicked
    grid.rotateCell(gridX, gridY)
}