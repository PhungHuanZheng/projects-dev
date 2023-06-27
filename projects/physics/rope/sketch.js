let rope;


function setup() {
    createCanvas(windowWidth, windowHeight);
    
    rope = new Rope(100, 100, 5, 50, 0.5);
    rope.data[0].isFixed = true;
    rope.data[rope.data.length - 1].isFixed = true;
}

function draw() {
    background(0);


    rope.update()
    // rope.data[rope.data.length - 1].pos = createVector(mouseX, mouseY)

    rope.show()
}