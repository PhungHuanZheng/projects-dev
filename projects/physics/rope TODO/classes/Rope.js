class Rope {
    constructor(x, y, nodeCount, initialDistance, elasticity, ) {
        this.pos = createVector(x, y);
        this.nodeCount = nodeCount;
        this.elasticity = elasticity;

        this.initialDistance = initialDistance;
        this.maxNodeDistance = ((1 + 0.2) * initialDistance);

        this.initNodes();
        this.initNeighbours();
    }

    initNodes() {
        // init rope Node instances
        this.nodes = []
        for (let i = 0; i < this.nodeCount; i++) {
            this.nodes.push(new Node(this.pos.x + (this.initialDistance * i), this.pos.y))
        }
    }

    initNeighbours() {
        for (let i = 0; i < this.nodes.length; i++) {
            for (let trans of [-1, 1]) {
                if (this.nodes[i + trans])
                    this.nodes[i].neighbours.push(this.nodes[i + trans])
                else
                    this.nodes[i].neighbours.push(null)
            }
        }
    }

    getNode(index) {
        return this.nodes[index];
    }

    update() {
        for (let node of this.nodes) {
            if (node.isFixed) continue;
            node.pos.y += 50;

            // constrain to within canvas
            node.pos.x = constrain(node.pos.x, 0, width);
            node.pos.y = constrain(node.pos.y, 0, height);

            // if has both neighbours
            // console.log(node.neighbours.every(n => n != null))
            if (node.neighbours.every(n => n != null)) {
                // check if dists between each neighbour are the same
                let d1 = dist(node.pos.x, node.pos.y, node.neighbours[0].pos.x, node.neighbours[0].pos.y)
                let d2 = dist(node.pos.x, node.pos.y, node.neighbours[1].pos.x, node.neighbours[1].pos.y)

                // if uneven distances
                if (d1 != d2) {
                    // get supposed pos, middle position
                    let middleX = node.neighbours[0].pos.x + ((node.neighbours[1].pos.x - node.neighbours[0].pos.x) / 2);
                    let middleY = node.neighbours[0].pos.y + ((node.neighbours[1].pos.y - node.neighbours[0].pos.y) / 2);
                    
                    // bridge distance between nodes    
                    node.pos.x = lerp(node.pos.x, middleX, 1 - this.elasticity / 2)
                    node.pos.y = lerp(node.pos.y, middleY, 1 - this.elasticity / 2)
                }
            }
        }
    }

    show() {
        for (let node of this.nodes)
            node.show()
    }
}