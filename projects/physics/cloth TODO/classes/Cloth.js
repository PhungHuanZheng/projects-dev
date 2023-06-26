class Cloth {
    constructor(gridWidth, gridHeight, cellLength, elasticity) {
        this.shape = { w: gridWidth, h: gridHeight };
        this.cellLength = cellLength;
        this.elasticity = elasticity;

        this.originalWidth = gridWidth * this.cellLength;
        this.originalHeight = gridHeight * this.cellLength;

        this.maxCanvasWidth = (this.shape.w - 1) * (this.cellLength * (1 + this.elasticity));
        this.maxCanvaHeight = (this.shape.h - 1) * (this.cellLength * (1 + this.elasticity));

        this.startingX = (width - (this.shape.w * this.cellLength - this.cellLength)) / 2;
        this.startingY = (height - (this.shape.h * this.cellLength - this.cellLength)) / 2;

        this.initData();
    }

    initData() {
        this.data = [];
        for (let y = 0; y < this.shape.h; y++) {
            let rowData = [];
            for (let x = 0; x < this.shape.w; x++) {
                rowData.push(new Point(x, y, this.startingX, this.startingY, this.cellLength, this.elasticity));
            }
            this.data.push(rowData);
        }
        this.#initNeighbours();
    }

    #initNeighbours() {
        // iterate over grid data
        for (let y = 0; y < this.shape.h; y++) {
            for (let x = 0; x < this.shape.w; x++) {
                let cell = this.data[y][x]

                // iterate over 4 adjacent cells
                for (let relTrans of [[-1, 0], [0, -1], [1, 0], [0, 1]]) {
                    try {
                        let otherCell = this.data[y + relTrans[0]][x + relTrans[1]]

                        // if exists, add to neighbours
                        if (otherCell) {
                            cell.neighbours.push(otherCell);
                        }
                    } catch {
                        cell.neighbours.push(null);
                    }
                }
            }
        }
    }

    getRow(index) {
        return this.data[index];
    }

    getRowLength(index) {
        // get row data
        let rowData = this.getRow(index);

        // get distance sum between point connectors
        let distSum = 0;
        for (let i = 0; i < rowData.length; i++) {
            if (rowData[i + 1]) {
                let d = dist(rowData[i].canvasX, 0, rowData[i + 1].canvasX, 0)
                distSum += d;
            }
        }
        return distSum;
    }

    getCol(index) {
        let colData = [];
        for (let y = 0; y < this.shape.h; y++) {
            colData.push(this.data[y][index])
        }
        return colData;
    }

    getColHeight(index) {
        // get col data
        let colData = this.getCol(index);

        // get distance sum between point connectors
        let distSum = 0;
        for (let i = 0; i < colData.length; i++) {
            if (colData[i + 1]) {
                let d = dist(0, colData[i].canvasY, 0, colData[i + 1].canvasY)
                distSum += d;
            }
        }
        return distSum;
    }

    update() {
        // update directions of elastic forces, ['N', 'W', 'S', 'E']
        for (let pt of this.data.flat()) {
            // iterate over neighbours
            for (let neighbour of pt.neighbours) {
                // if invalid, skip
                if (!neighbour) continue;

                // get distance between pt and neighbour
                let d = dist(pt.canvasX, pt.canvasY, neighbour.canvasX, neighbour.canvasY);
                if (d > this.cellLength) {
                    // get force vector
                    let multiplier = d / this.cellLength;
                }
            }
        }

    }

    #redistribute() {
        
    }

    show() {
        for (let point of this.data.flat()) {
            point.show()
        }

        for (let y = 0; y < this.shape.h; y++) {
            for (let x = 0; x < this.shape.w; x++) {
                this.data[y][x].show(this.cellLength)
            }
        }
    }
}


class Point {
    constructor(x, y, startingX, startingY, cellLength, elasticity) {
        this.gridX = x;
        this.gridY = y;

        this.canvasX = this.gridX * cellLength + startingX;
        this.canvasY = this.gridY * cellLength + startingY;


        this.maxCellLength = cellLength * (1 + elasticity);

        this.neighbours = [];

        this.selectionDist = cellLength * 0.5
        this.isBeingDragged = false;
        this.isFixed = false;
    }

    update() {
        if (this.isBeingDragged) {
            this.canvasX = mouseX;
            this.canvasY = mouseY;
        }
    }


    show() {
        noStroke();
        this.isFixed ? fill(255, 0, 0) : this.isBeingDragged ? fill(0, 255, 9) : fill(255);
        circle(this.canvasX, this.canvasY, 5);

        stroke(255); strokeWeight(0.5)
        for (let pt of this.neighbours) {
            if (!pt) continue;
            line(this.canvasX, this.canvasY, pt.canvasX, pt.canvasY)
        }

        noFill(); strokeWeight(0.25)
        circle(this.canvasX, this.canvasY, this.selectionDist);
    }
}