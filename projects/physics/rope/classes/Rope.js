class Rope {
    constructor(x, y, nodeCount, constraintLength, elasticity) {
        this.pos = createVector(x, y);
        this.nodeCount = nodeCount;
        this.constraintLength = constraintLength;
        this.elasticity = elasticity;

        // init nodes
        this.data = [];
        for (let i = 0; i < nodeCount; i++) {
            this.data.push(new PointMass(x + (constraintLength * i), y))
        }

        // set constraints between nodes
        this.constraints = [];
        for (let i = 0; i < this.data.length; i++) {
            if (!this.data[i + 1]) continue;
            this.constraints.push(new Constraint(this.data[i], this.data[i + 1], this.constraintLength, this.elasticity))
        }
    }

    update() {
        // apply gravity on all points
        for (let node of this.data) {
            // if fixed point, dont update
            if (node.isFixed) continue;

            node.pos.y += 9.8
        }
        
        for (let i = this.constraints.length - 1; i >= 0; i--) {
            this.constraints[i].updateNodes()
            this.constraints[this.constraints.length - 1 - i].updateNodes()

            console.log(i, this.constraints.length - 1 - i)
        }
    }

    show() {
        for (let node of this.data) {
            node.show()
        }

        for (let constraint of this.constraints) {
            constraint.show()
        }
    }
}