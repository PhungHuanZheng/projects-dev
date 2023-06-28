class Constraint {
    constructor(node1, node2, constraintLength, elasticity, isVertical) {
        this.node1 = node1;
        this.node2 = node2;
        this.constraintLength = constraintLength;
        this.elasticity = elasticity;

        this.currentLength = constraintLength;
        this.minLength = (1 - elasticity) * constraintLength;
        this.maxLength = (1 + elasticity) * constraintLength;

        this.isVertical = isVertical;
        this.isHorizontal = !isVertical;

        // get middle point between the nodes
        this.center = createVector(
            (this.node1.pos.x - this.node2.pos.x) / 2 + this.node2.pos.x,
            (this.node1.pos.y - this.node2.pos.y) / 2 + this.node2.pos.y,
        )
    }

    updateMidPoint() {
        this.center = createVector(
            (this.node1.pos.x - this.node2.pos.x) / 2 + this.node2.pos.x,
            (this.node1.pos.y - this.node2.pos.y) / 2 + this.node2.pos.y,
        )
    }

    updateNodes() {
        // get current distance between nodes
        this.currentLength = dist(this.node1.pos.x, this.node1.pos.y, this.node2.pos.x, this.node2.pos.y)

        for (let node of [this.node1, this.node2]) {
            if (node.isFixed) continue;

            let nodePosDiff = this.center.copy().sub(node.pos);
            nodePosDiff.mult(map(this.currentLength, this.minLength, this.maxLength, -0.45, 0.6));
            node.pos.add(nodePosDiff);
        }
    }

    show() {
        strokeWeight(0.75);
        stroke(
            map(this.currentLength, this.minLength, this.maxLength, 0, 255),
            map(this.currentLength, this.minLength, this.maxLength, 255, 0),
            0
        )
        line(this.node1.pos.x, this.node1.pos.y, this.node2.pos.x, this.node2.pos.y)
        
        // fill(255); noStroke()
        // circle(this.center.x, this.center.y, 8)
    }
}