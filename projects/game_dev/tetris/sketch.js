let grid;
let pieces = {};

function setup() {
    createCanvas(windowWidth, windowHeight);
    grid = new Grid(20, 10, 25);

    // init pieces
    pieces['I'] = new Piece(grid, data=[
        [1],
        [1],
        [1],
        [1]
    ])

    
}

function draw() {
    background(0);

    grid.show(true);
}