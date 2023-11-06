class Grid {
    constructor(rows, columns, cellLength) {
        this.shape = [rows, columns];
        this.cellLength = cellLength;

        // populate grid
        this.data = Array.from(Array(rows), () => new Array(columns))
        for (let y = 0; y < rows; y++) {
            for (let x = 0; x < columns; x++) {
                this.data[y][x] = new GridCell(x, y, cellLength);
            }
        }

        // track pieces on grid
        this.activePieces = [];
    }

    cellAt(gridX, gridY) {
        return this.data[gridY][gridX];
    }

    update() {
        for (let i = 0; i < this.activePieces.length; i++) {
            let piece = this.activePieces[i];
            piece.update();
        }
    }

    show(centerGrid) {
        noFill();
        stroke(255);

        // if want to center grid in canvas, do extra calculations
        let xOffset, yOffset;
        if (centerGrid) {
            xOffset = (width / 2) - ((this.shape[1] * this.cellLength) / 2);
            yOffset = (height / 2) - ((this.shape[0] * this.cellLength) / 2);
        }

        for (let y = 0; y < this.shape[0]; y++) {
            for (let x = 0; x < this.shape[1]; x++) {
                let cell = this.cellAt(x, y);
                rect(
                    cell.x * this.cellLength + (centerGrid ? xOffset : 0),
                    cell.y * this.cellLength + (centerGrid ? yOffset : 0),
                    this.cellLength
                );
            }
        }
    }
}

class GridCell {
    constructor(x, y, cellLength) {
        this.x = x;
        this.y = y;
        this.cellLength = cellLength;
    }
}