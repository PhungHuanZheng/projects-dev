class Constraint {
    constructor(node1, node2, constraintLength, elasticity) {
        this.node1 = node1;
        this.node2 = node2;
        this.constraintLength = constraintLength;
        this.elasticity = elasticity;
    }

    updateNodes() {
        // attract/repel nodes depending on distance between
        let centerPoint = createVector(
            ((this.node1.pos.x - this.node2.pos.x) / 2) + this.node2.pos.x,
            ((this.node1.pos.y - this.node2.pos.y) / 2) + this.node2.pos.y
        );
        // circle(centerPoint.x, centerPoint.y, 10)

        for (let node of [this.node1, this.node2]) {
            // distance between node and center
            let distanceBetween = dist(node.pos.x, node.pos.y, centerPoint.x, centerPoint.y);
            let minDistance = ((1 - this.elasticity) * this.constraintLength) / 2;
            let maxDistance = ((1 + this.elasticity) * this.constraintLength) / 2;

            // get force acting on node
            let force = createVector(centerPoint.x - node.pos.x, centerPoint.y - node.pos.y);
            let multiplier = map(distanceBetween, minDistance, maxDistance, 15, -15);
            force = p5.Vector.normalize(force)
            force.mult(multiplier)

            if (!node.isFixed) node.pos.sub(force)
        }
    }   

    show() {
        let distanceBetween = dist(this.node1.pos.x, this.node1.pos.y, this.node2.pos.x, this.node2.pos.y);
        let minDistance = (1 - this.elasticity) * this.constraintLength;
        let maxDistance = (1 + this.elasticity) * this.constraintLength;

        let r = map(distanceBetween, minDistance, maxDistance, 0, 255);
        let g = 255 - r;

        stroke(r, g, 0);
        line(this.node1.pos.x, this.node1.pos.y, this.node2.pos.x, this.node2.pos.y)
    }
}