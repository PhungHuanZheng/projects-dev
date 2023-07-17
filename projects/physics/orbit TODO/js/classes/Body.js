class Body {
    constructor(x, y, mass) {
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);

        this.mass = mass;

        this.trail = []
        this.trailLength = 10;
    }

    update() {
        this.pos.add(this.vel);
        this.vel.add(this.acc);
        this.acc.mult(0);

        // this.pos.x = this.pos.x % width;
        // this.pos.y = this.pos.y % height;

        // bounce off walls cuz why not
        if (this.pos.x <= 10 || this.pos.x >= width - 10)
            this.vel.x *= -1;
        if (this.pos.y <= 10 || this.pos.y >= height - 10)
            this.vel.y *= -1;
    }

    orbit(otherBody) {
        // calculate force between 2 bodies
        let d = dist(this.pos.x, this.pos.y, otherBody.pos.x, otherBody.pos.y);
        let F = (G * this.mass * otherBody.mass) / (d * d);

        // get resulting acceleration multiplier
        let accMult = F / this.mass;

        // get vector for new acceleration, normalize
        let newAcc = createVector(otherBody.pos.x - this.pos.x, otherBody.pos.y - this.pos.y);
        newAcc = p5.Vector.normalize(newAcc);
        newAcc.mult(accMult * 15);

        this.acc = newAcc;
        this.vel.setMag(14.25)
    }

    show(showTrail) {
        fill(255); noStroke();
        circle(this.pos.x, this.pos.y, this.mass);
        this.trail.push(this.pos.copy())

        if (showTrail) {
            noFill(); stroke(255); beginShape();
            for (let i = this.trail.length - 1; i >= 0; i--) {
                vertex(this.trail[i].x, this.trail[i].y);
                if (this.trail.length > this.trailLength) {
                    this.trail.shift()
                }
            }
            endShape();
        }
    }
}