class PipeCell {
    constructor(x, y, cellLength) {
        this.pos = { x, y };
        this.cellLength = cellLength;

        this.facing_dirs = [];
        this.directions = ['N', 'W', 'S', 'E'];
        this.directions_ = ['N', 'W', 'S', 'E'];

        // get pipe directions
        let dir_count = floor(random(1, 5))
        for (let i = 0; i < dir_count; i++) {
            let chosen_dir = this.directions[floor(random(this.directions.length))];
            
            // remove from selections
            this.facing_dirs.push(chosen_dir);
            this.directions.splice(this.directions.indexOf(chosen_dir), 1);   
        }

        // width of pipe drawn on cells
        this.pipeWidth = 2.5 / 7 * this.cellLength;
        this.pipeOffset = (this.cellLength - this.pipeWidth) / 2;
        
        // game liquid logic
        this.hasWater = false;
        this.isWaterSource = false;

        this.hasLava = false;
        this.isLavaSource = false;

        this.isObsidian = false;
    }

    rotate() {
        // shift directions left by 1
        for (let i = 0; i < this.facing_dirs.length; i++) {
            let dir_index = this.directions_.indexOf(this.facing_dirs[i]);
            let new_dir = this.directions_[(dir_index - 1 + this.directions_.length) % this.directions_.length]; 

            // set new direction
            this.facing_dirs[i] = new_dir;
        }
    }

    show(startingX, startingY) {
        // get starting positions for this cell
        let cellCanvasX = this.pos.x * this.cellLength + startingX;
        let cellCanvasY = this.pos.y * this.cellLength + startingY
        
        rectMode(CORNER); noStroke();
        this.hasWater ? fill(28, 163, 236) : this.hasLava ? fill(255, 102, 0) : fill(140);
        // if 2 or more directions, draw center connector
        if (this.facing_dirs.length >= 2) {
            rect(cellCanvasX + this.pipeOffset, cellCanvasY + this.pipeOffset, this.pipeWidth)
        }

        // draw pipe in directions instantiated
        if (this.facing_dirs.includes('N')) {
            rect(cellCanvasX + this.pipeOffset, cellCanvasY, this.pipeWidth, this.pipeWidth)
        }
        if (this.facing_dirs.includes('W')) {
            rect(cellCanvasX, cellCanvasY + this.pipeOffset, this.pipeWidth, this.pipeWidth)
        }
        if (this.facing_dirs.includes('S')) {
            rect(cellCanvasX + this.pipeOffset, cellCanvasY + 2 * this.pipeOffset, this.pipeWidth, this.pipeWidth)
        }
        if (this.facing_dirs.includes('E')) {
            rect(cellCanvasX + 2 * this.pipeOffset, cellCanvasY + this.pipeOffset, this.pipeWidth, this.pipeWidth)
        }

        // draw box
        rectMode(CORNER); stroke(255); 
        this.isObsidian ? fill(46, 41, 58) : noFill()
        rect(cellCanvasX, cellCanvasY, this.cellLength);
    }   
}