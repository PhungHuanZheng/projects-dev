class Boid {
    constructor(x, y, perceptionRadius, coherence, separation, alignment, speed) {
        this.perceptionRadius = perceptionRadius;
        this.coherence = coherence;
        this.separation = separation;
        this.alignment = alignment;
        this.speed = speed;

        this.pos = createVector(x, y);
        this.vel = p5.Vector.normalize(
            createVector(
                random(-width, width),
                random(-height, height)
            )
        );
        this.vel.mult(speed)

        this.trail = [];
        this.trailLength = 100;

        this.boidColour = color(255);
    }

    update() {
        this.pos.add(this.vel);

        if (this.pos.x <= 0 || this.pos.x >= width) this.vel.x *= -1;
        if (this.pos.y <= 0 || this.pos.y >= height) this.vel.y *= -1;
    }

    show(showTrails) {
        fill(this.boidColour); noStroke()
        circle(this.pos.x, this.pos.y, 8);
        this.trail.push({ x: this.pos.x, y: this.pos.y })

        // show perception radius
        noFill(); stroke(255); strokeWeight(0.25)
        circle(this.pos.x, this.pos.y, this.perceptionRadius * 2)

        if (showTrails) {
            // show trail
            beginShape(LINES); stroke(255); strokeWeight(0.5)
            for (let i = this.trail.length - 1; i >= 0; i--) {
                vertex(this.trail[i].x, this.trail[i].y);
                if (this.trail.length > this.trailLength) {
                    this.trail.shift()
                }
            }
            endShape();
        }

        // show moving direction
        let tempVector = p5.Vector.normalize(this.vel);
        tempVector.mult(this.perceptionRadius);

        line(this.pos.x, this.pos.y, this.pos.x + tempVector.x, this.pos.y + tempVector.y);
    }
}