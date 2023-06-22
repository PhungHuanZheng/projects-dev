class Grid {
    constructor(gridWidth, gridHeight) {
        this.width = gridWidth;
        this.height = gridHeight;
        
        // build 2D grid structure
        this.data = [];
        for (let y = 0; y < this.height; y++) {
            let rowData = [];
            for (let x = 0; x < this.width; x++) {
                rowData.push(new PipeCell(x, y));
            }
            this.data.push(rowData);
        }
    }

    cellAt(x, y) {
        return this.data[y][x];
    }
}