class Target {
    constructor(x, y) {
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);
    }

    update() {
        // physics engine
        this.pos.add(this.vel);
        this.vel.add(this.acc);
        this.acc.mult(0)

        // constrain and bounce
        this.pos.x = constrain(this.pos.x, 0, width);
        if (this.pos.x <= 0 || this.pos.x >= width) this.vel.x *= -1;
        this.pos.y = constrain(this.pos.y, 0, height);
        if (this.pos.y <= 0 || this.pos.y >= height) this.vel.y *= -1;
    }



    show() {
        rectMode(CENTER); fill(255); noStroke();
        rect(this.pos.x, this.pos.y, 25, 1);
        rect(this.pos.x, this.pos.y, 1, 25);
    }
}