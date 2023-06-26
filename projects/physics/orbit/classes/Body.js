class Body {
    constructor(x, y, mass) {
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);

        this.mass = mass;
        this.size = sqrt(mass) / 50000000000

        this.trail = [];
    }

    update() {
        this.pos.add(this.vel);
        this.vel.add(this.acc);
        this.acc.mult(0);

        // bounce off walls cuz why not
        if (this.pos.x <= 10 || this.pos.x >= width - 10)
            this.vel.x *= -1;
        if (this.pos.y <= 10 || this.pos.y >= height - 10)
            this.vel.y *= -1;
    }

    setPos(x, y) {
        this.pos.x = x;
        this.pos.y = y;
    }

    orbit(otherBody) {
        // calculate force between 2 bodies
        let d = dist(this.pos.x, this.pos.y, otherBody.pos.x, otherBody.pos.y);
        let F = (G * this.mass * otherBody.mass) / (d * d)

        // get resulting acceleration multiplier
        let accMult = F / this.mass;

        // get vector for new acceleration, normalize
        let newAcc = createVector(otherBody.pos.x - this.pos.x, otherBody.pos.y - this.pos.y);
        newAcc = p5.Vector.normalize(newAcc);
        newAcc.mult(accMult * 0.000000000001);

        this.acc = newAcc;


    }

    show() {
        fill(255); stroke(255);
        circle(this.pos.x, this.pos.y, this.size);

        this.trail.push({ x: this.pos.x, y: this.pos.y });
        if (this.trail.length >= 500)
            this.trail.shift()

        beginShape(); noFill()
        for (let pt of this.trail) {
            vertex(pt.x, pt.y);
        }
        endShape();
    }
}