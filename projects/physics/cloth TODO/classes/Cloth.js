class Cloth {
    constructor(clothWidth, clothHeight, constraintLength, elasticity) {
        this.shape = { w: clothWidth, h: clothHeight };
        this.elasticity = elasticity;
        this.constraintLength = constraintLength;

        // get start positions to center cloth on canvas
        this.start = createVector(
            (width - ((clothWidth - 1) * constraintLength)) / 2,
            (height - ((clothHeight - 1) * constraintLength)) / 2,
        )

        // init nodes/point masses
        this.nodes = [];
        for (let y = 0; y < clothHeight; y++) {
            let rowData = [];
            for (let x = 0; x < clothWidth; x++) {
                rowData.push(new Node(
                    this.start.x + x * constraintLength,
                    this.start.y + y * constraintLength
                ));
            }
            this.nodes.push(rowData);
        }
        this.flatNodes = this.nodes.flat()

        // init constraints between nodes
        this.constraints = [];
        for (let y = 0; y < clothHeight; y++) {
            for (let x = 0; x < clothWidth; x++) {
                // get node at index
                let thisNode = this.nodes[y][x];

                // get surrounding 4 nodes
                this.constraints = this.constraints.concat([
                    this.nodes[y - 1] && this.nodes[y - 1][x] ? new Constraint(thisNode, this.nodes[y - 1][x], constraintLength, elasticity, true) : null,
                    this.nodes[y + 1] && this.nodes[y + 1][x] ? new Constraint(thisNode, this.nodes[y + 1][x], constraintLength, elasticity, true) : null,
                    this.nodes[y][x - 1] ? new Constraint(thisNode, this.nodes[y][x - 1], constraintLength, elasticity, false) : null,
                    this.nodes[y][x + 1] ? new Constraint(thisNode, this.nodes[y][x + 1], constraintLength, elasticity, false) : null,
                ])
            }
        }
        this.constraints = this.constraints.filter(obj => obj)
    }

    addFixtures(indexes) {
        for (let index of indexes) {
            this.flatNodes[index].isFixed = true;
        }
    }

    update() {
        for (let node of this.flatNodes) {
            // if fixed node, ignore
            if (node.isFixed) continue;

            // keep within canvas area
            node.pos.x = constrain(node.pos.x, 0, width);
            node.pos.y = constrain(node.pos.y, 0, height);

            // apply gravity
            node.pos.y += 5
        }

        for (let i = 0; i < this.constraints.length; i++) {
            this.constraints[i].updateMidPoint()
            this.constraints[i].updateNodes()

            this.constraints[this.constraints.length - 1 - i].updateMidPoint()
            this.constraints[this.constraints.length - 1 - i].updateNodes()
        }

    }

    show() {
        for (let constraint of this.constraints) {
            constraint.show()
        }
        for (let node of this.flatNodes) {
            node.show()
        }
    }
}