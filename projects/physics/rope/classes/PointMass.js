class PointMass {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.isFixed = false;
    }

    show() {
        fill(255); noStroke();
        circle(this.pos.x, this.pos.y, 5);
    }
}