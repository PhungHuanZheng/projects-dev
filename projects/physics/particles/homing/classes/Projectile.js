class Projectile {
    constructor(x, y, homingRadius) {
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);

        this.initialMag = null;
        this.homingRadius = homingRadius;
        this.trail = [];
    }

    home(target) {
        if (dist(this.pos.x, this.pos.y, target.pos.x, target.pos.y) < this.homingRadius) {
            let PosDiff = createVector(target.pos.x - this.pos.x, target.pos.y - this.pos.y);
            PosDiff = p5.Vector.normalize(PosDiff);
            PosDiff.mult(15);

            this.vel.x = lerp(this.vel.x, PosDiff.x, 0.15);
            this.vel.y = lerp(this.vel.y, PosDiff.y, 0.15);
        }

        // physics engine
        this.pos.add(this.vel);
        this.vel.add(this.acc);
        this.acc.mult(0);

        
    }

    show(clr) {
        fill(clr); stroke(255); strokeWeight(0.25)
        circle(this.pos.x, this.pos.y, 5);

        this.trail.push(this.pos);
        if (this.trail.length >= 25)
            this.trail.shift()

        beginShape(LINES); stroke(255)
        for (const pt of this.trail) {
            vertex(pt.x, pt.y);
        }
        endShape()
    }
}