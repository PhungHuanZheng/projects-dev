class Grid {
    constructor(gridWidth, gridHeight, cellLength) {
        this.width = gridWidth;
        this.height = gridHeight;
        this.cellLength = cellLength;

        // build 2D grid structure
        this.data = [];
        for (let y = 0; y < this.height; y++) {
            let rowData = [];
            for (let x = 0; x < this.width; x++) {
                rowData.push(new PipeCell(x, y, this.cellLength));
            }
            this.data.push(rowData);
        }

        // starting point to place in center of canvas
        this.startingX = width / 2 - ((this.width * this.cellLength) / 2);
        this.startingY = height / 2 - ((this.height * this.cellLength) / 2);

        // init water and set starting point
        this.waterCells = [this.cellAt(0, 0)];
        this.cellAt(0, 0).hasWater = true;
        this.cellAt(0, 0).isWaterSource = true;
        this.waterGoal = { x: this.width - 1, y: this.height - 1 };

        // init lava and set starting point
        this.lavaCells = [this.cellAt(this.width - 1, 0)];
        this.cellAt(this.width - 1, 0).hasLava = true;
        this.cellAt(this.width - 1, 0).isLavaSource = true;
    }

    cellAt(x, y) {
        // check that x, y within bounds, else silent exit
        if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
            return;
        }

        return this.data[y][x];
    }

    rotateCell(x, y) {
        this.cellAt(x, y).rotate();
        this.clearLiquids()
    }

    clearLiquids() {
        // update water
        for (let i = this.waterCells.length - 1; i >= 0; i--) {
            // if water source cell, ignore
            if (this.waterCells[i].isWaterSource) {
                continue;
            }

            // else remove water
            this.waterCells[i].hasWater = false;
            this.waterCells.splice(i, 1)
        }

        // update lava
        for (let i = this.lavaCells.length - 1; i >= 0; i--) {
            // if water source cell, ignore
            if (this.lavaCells[i].isLavaSource) {
                continue;
            }

            // else remove water
            this.lavaCells[i].hasLava = false;
            this.lavaCells.splice(i, 1)
        }
    }

    updateLiquids() {
        // update water
        for (let i = this.waterCells.length - 1; i >= 0; i--) {
            let waterCell = this.waterCells[i];

            for (let relPos of [[0, -1], [-1, 0], [0, 1], [1, 0]]) {
                let otherCell = this.cellAt(waterCell.pos.x + relPos[0], waterCell.pos.y + relPos[1]);

                // if out of bounds or already water, ignore
                if (!otherCell || otherCell.hasWater || otherCell.isObsidian) continue;

                // if other cell on left
                if (waterCell.pos.x - otherCell.pos.x > 0) {
                    if (waterCell.facing_dirs.includes('W') && otherCell.facing_dirs.includes('E')) {
                        this.waterCells.push(otherCell)
                        otherCell.hasWater = true;
                        break;
                    }
                }

                // if other cell on right
                if (waterCell.pos.x - otherCell.pos.x < 0) {
                    if (waterCell.facing_dirs.includes('E') && otherCell.facing_dirs.includes('W')) {
                        this.waterCells.push(otherCell)
                        otherCell.hasWater = true;
                        break;
                    }
                }

                // if other cell on top
                if (waterCell.pos.y - otherCell.pos.y > 0) {
                    if (waterCell.facing_dirs.includes('N') && otherCell.facing_dirs.includes('S')) {
                        this.waterCells.push(otherCell)
                        otherCell.hasWater = true;
                        break;
                    }
                }

                // if other cell on bottom
                if (waterCell.pos.y - otherCell.pos.y < 0) {
                    if (waterCell.facing_dirs.includes('S') && otherCell.facing_dirs.includes('N')) {
                        this.waterCells.push(otherCell)
                        otherCell.hasWater = true;
                        break;
                    }
                }
            }
        }

        // update lava
        for (let i = this.lavaCells.length - 1; i >= 0; i--) {
            let lavaCell = this.lavaCells[i];

            for (let relPos of [[0, -1], [-1, 0], [0, 1], [1, 0]]) {
                let otherCell = this.cellAt(lavaCell.pos.x + relPos[0], lavaCell.pos.y + relPos[1]);

                // if out of bounds or already water, ignore
                if (!otherCell || otherCell.hasLava || otherCell.isObsidian) continue;

                // if other cell on left
                if (lavaCell.pos.x - otherCell.pos.x > 0) {
                    if (lavaCell.facing_dirs.includes('W') && otherCell.facing_dirs.includes('E')) {
                        this.lavaCells.push(otherCell)
                        otherCell.hasLava = true;
                        break;
                    }
                }

                // if other cell on right
                if (lavaCell.pos.x - otherCell.pos.x < 0) {
                    if (lavaCell.facing_dirs.includes('E') && otherCell.facing_dirs.includes('W')) {
                        this.lavaCells.push(otherCell)
                        otherCell.hasLava = true;
                        break;
                    }
                }

                // if other cell on top
                if (lavaCell.pos.y - otherCell.pos.y > 0) {
                    if (lavaCell.facing_dirs.includes('N') && otherCell.facing_dirs.includes('S')) {
                        this.lavaCells.push(otherCell)
                        otherCell.hasLava = true;
                        break;
                    }
                }

                // if other cell on bottom
                if (lavaCell.pos.y - otherCell.pos.y < 0) {
                    if (lavaCell.facing_dirs.includes('S') && otherCell.facing_dirs.includes('N')) {
                        this.lavaCells.push(otherCell)
                        otherCell.hasLava = true;
                        break;
                    }
                }
            }
        }

        // check for clashes
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                let cell = this.cellAt(x, y);
                
                // check if both is lava and is water
                if (cell.hasWater && cell.hasLava) {
                    // set obsidian, remove rights
                    cell.isObsidian = true;
                    this.clearLiquids();
                    return;
                }
            }
        }
    }

    show() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                this.cellAt(x, y).show(this.startingX, this.startingY);
            }
        }

    }
}