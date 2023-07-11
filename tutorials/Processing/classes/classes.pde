DynamicGrid dg;

void setup() {
    size(800, 450);
    dg = new DynamicGrid(2);
    printArray(dg.shape);
    size(dg.canvasWidth, dg.canvasHeight);
}

void draw() {
    background(0);
    
    dg.show();
}
