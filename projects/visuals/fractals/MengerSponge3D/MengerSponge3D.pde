final static int CANVAS_WIDTH = 500;
final static int CANVAS_HEIGHT = 500;

Sponge sponge;
int rotation = 0;

void settings() {
    size(CANVAS_WIDTH, CANVAS_HEIGHT, P3D);
}

void setup() {
    sponge = new Sponge(width / 2, height / 2, 0, CANVAS_WIDTH);
    sponge.split();
}

void draw() {
    background(0);
    //translate(width / 2, height / 2);
    
    sponge.show(0.01);
    

}
