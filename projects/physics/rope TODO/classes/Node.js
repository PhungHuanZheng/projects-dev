class Node {
    constructor(x, y,) {
        this.pos = createVector(x, y);
        this.neighbours = [];

        this.isFixed = false;
    }

    show() {
        fill(255); noStroke(); 
        circle(this.pos.x, this.pos.y, 10);

        if (this.neighbours[1]) {
            stroke(255);
            line(this.pos.x, this.pos.y, this.neighbours[1].pos.x, this.neighbours[1].pos.y)
        }
    }
}