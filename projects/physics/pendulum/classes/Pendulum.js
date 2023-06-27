class Pendulum {
    #internalTimer = 0

    constructor(anchorX, anchorY, cordLength, bobMass, initialAngle) {
        this.anchorX = anchorX;
        this.anchorY = anchorY;
        this.cordLength = cordLength;
        this.bobMass = bobMass;
        this.initialAngle = initialAngle;

        // get position from initial angle
        this.bobPos = this.angleToPos(initialAngle)
    }

    getAngleAtTime(t) {
        return this.initialAngle * cos(((2 * PI) / this.T) * t)
    }

    angleToPos(angle) {
        return createVector(this.cordLength * sin(angle) + this.anchorX, this.cordLength * cos(angle) + this.anchorY)
    }

    // get angle of vertical to pendulum
    getTheta() {
        // get x and y difference between anchor and bob
        let diffX = this.bobPos.x - this.anchorX;
        let diffY = this.bobPos.y - this.anchorY;
        return atan(diffX / diffY);
    }

    update(t, interval) {
        if (t % interval == 0) {
            // get position of bob at time t with formula: https://en.wikipedia.org/wiki/Pendulum#Period_of_oscillation,
            // where T is the period of the pendulum given initial conditions
            let period = 2 * PI * sqrt(this.cordLength / G);

            // get angle of pendulum at time t
            let angle = this.initialAngle * cos(((TWO_PI) / period) * this.#internalTimer);

            // get position from angle from points on circle with radius [cordLength]
            this.bobPos = this.angleToPos(angle);
            this.#internalTimer++;

        }
    }

    show() {
        stroke(255);
        line(this.anchorX, this.anchorY, this.bobPos.x, this.bobPos.y);
        fill(255); noStroke();
        circle(this.bobPos.x, this.bobPos.y, this.bobMass)
    }
}