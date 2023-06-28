class Ball {
    constructor(x, y, radius) {
        this.pos = createVector(x, y);
        this.vel = createVector(10, 0);
        this.acc = createVector(0, 0);

        this.radius = radius;

        this.isSwinging = false;
        this.initialAngle = 0;
        this.period = 0;
        this.internalTimer = 0
    }

    update() {
        this.pos.add(this.vel)
        this.vel.add(this.acc)
        this.acc.mult(0.9);

        this.vel.x *= 0.99;

        this.pos.x = constrain(this.pos.x, this.radius, width - this.radius)
        this.pos.y = constrain(this.pos.y, this.radius, height - this.radius)

        if (this.pos.x <= this.radius || this.pos.x >= width - this.radius) this.vel.x *= -0.9;
        if (this.pos.y <= this.radius || this.pos.y >= height - this.radius) this.vel.y *= -0.9;
    }

    swing(anchorX, anchorY) {
        if (this.internalTimer == 0) {
            // get initial angle relative to anchor vertical
            let H = dist(this.pos.x, this.pos.y, anchorX, anchorY);
            let A = dist(this.pos.x, this.pos.y, anchorX, this.pos.y);
            this.initialAngle = HALF_PI - acos(A / H);

            // correct angle based on anchor position
            if (anchorX - this.pos.x >= 0) {
                this.initialAngle *= -1
            }
        }

        // get pos at time T
        let cordLength = dist(this.pos.x, this.pos.y, anchorX, anchorY);
        this.period = TWO_PI * sqrt(cordLength / 9.8);
        let currentAngle = this.initialAngle * cos(((2 * PI) / this.period) * this.internalTimer / 5);
        let newPos = createVector(cordLength * sin(currentAngle) + anchorX, cordLength * cos(currentAngle) + anchorY)

        // get velocity to move to that pos
        this.vel = newPos.sub(this.pos)
        this.internalTimer++;

        line(this.pos.x, this.pos.y, anchorX, anchorY);
    }

    show() {
        noFill(); stroke(255);
        circle(this.pos.x, this.pos.y, this.radius * 2);
    }
}