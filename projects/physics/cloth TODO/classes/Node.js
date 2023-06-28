class Node {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.isFixed = false;

        this.selectionRadius = 6
    }

    show() {
        fill(255); noStroke();
        circle(this.pos.x, this.pos.y, 3);

        noFill(); stroke(255); strokeWeight(0.5);
        circle(this.pos.x, this.pos.y, this.selectionRadius * 2);
    }
}