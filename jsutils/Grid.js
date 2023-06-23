class Grid {
    constructor(gridWidth, gridHeight, cellLength) {
        this.shape = { w: gridWidth, h: gridHeight };
        this.cellLength = cellLength;

        // init 2d array with cell data
        this.data = [];
        for (let y = 0; y < this.shape.h; y++) {
            let rowData = [];
            for (let x = 0; x < this.shape.w; x++) {
                rowData.push(new _Cell(x, y));
            }
            this.data.push(rowData);
        }

        // get starting x and y (top left corner)
        this.startingX = (width - (this.shape.w * this.cellLength)) / 2;
        this.startingY = (height - (this.shape.h * this.cellLength)) / 2;

        console.log(width, this.shape.w * this.cellLength)
    }

    getCell(x, y) {
        // if out of bounds, silent ignore
        if (x < 0 || x >= this.shape.w || y < 0 || y >= this.shape.h) {
            return
        }

        return this.data[y][x];
    }

    show() {
        for (let y = 0; y < this.shape.h; y++) {
            for (let x = 0; x < this.shape.w; x++) {
                let cell = this.getCell(x, y);
                cell.show(this.cellLength, this.startingX, this.startingY);
            }
        }
    }
}

class _Cell {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    show(cellLength, startingX, startingY) {
        // offset by starting x and y to put in center
        rectMode(CORNER); noFill(); stroke(0); strokeWeight(0.25);
        rect(this.x * cellLength + startingX, this.y * cellLength + startingY, cellLength)
    }
}