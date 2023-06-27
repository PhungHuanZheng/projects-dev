class Flock {
    constructor(boidCount, perceptionRadius, coherence, separation, alignment, speed) {
        this.boidCount = boidCount;
        this.perceptionRadius = perceptionRadius;
        this.coherence = coherence;
        this.separation = separation;
        this.alignment = alignment;
        this.speed = speed

        this.boids = [];
        for (let i = 0; i < boidCount; i++) {
            this.boids.push(
                new Boid(
                    random(width), random(height),
                    this.perceptionRadius, this.coherence,
                    this.separation, this.alignment,
                    this.speed
                )
            );
        }
    }

    update() {
        for (let boid of this.boids) {
            boid.update();
            boid.boidColour = color(255);
            let nearbyBoids = [];
            let tooNear = [];

            // get nearby boids, indicate when nearby
            for (let other of this.boids) {
                if (boid == other) continue;

                // if near
                let d = dist(boid.pos.x, boid.pos.y, other.pos.x, other.pos.y);
                if (d <= this.perceptionRadius) {
                    // boid.boidColour = color(255, 0, 0);
                    nearbyBoids.push(other)
                }

                // if too near  
                if (d <= this.perceptionRadius / 2) {
                    // boid.boidColour = color(255, 0, 0);
                    tooNear.push(other)
                }
            }

            // coherence
            if (nearbyBoids.length > 0) {
                let meanVector = createVector(0, 0);
                for (let other of nearbyBoids) {
                    meanVector.add(other.vel);
                }
                meanVector.div(nearbyBoids.length)

                meanVector = p5.Vector.normalize(meanVector)
                meanVector.mult(this.speed)

                // lerp boid's velocity to mean velocity
                boid.vel.x = lerp(boid.vel.x, meanVector.x, this.coherence);
                boid.vel.y = lerp(boid.vel.y, meanVector.y, this.coherence);
            }

            // separation
            if (tooNear.length > 0) {
                let meanVector = createVector(0, 0);
                for (let other of nearbyBoids) {
                    meanVector.add(other.vel);
                }
                meanVector.div(nearbyBoids.length)

                meanVector = p5.Vector.normalize(meanVector)
                meanVector.mult(-this.speed)

                // lerp boid's velocity to mean velocity
                boid.vel.x = lerp(boid.vel.x, meanVector.x, this.separation);
                boid.vel.y = lerp(boid.vel.y, meanVector.y, this.separation);
            }
        }
    }

    show() {
        for (let boid of this.boids) {
            boid.show()
        }
    }
}