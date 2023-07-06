class HierarchicalGrid {
    /**
     * Creates an instance of `HierarchicalGrid`, contains `Chunk` objects which
     * contain `Tile` objects.
     * 
     * @param {Number} gridLength    Length of grid in tiles.
     * @param {Number} chunkLength   Number of tiles per chunk in grid. 
     */
    constructor(gridLength, tilesPerChunk) {
        this.gridLength = gridLength;
        this.tilesPerChunk = tilesPerChunk;

        // check if "gridLength" is divisivle by "tilesPerChunk"
        if (gridLength % tilesPerChunk !== 0)
            throw new Error(`"gridLength" passed must be divisible by "tilesPerChunk".`)

        // get length of side of tile
        let shortestCanvasSide = height < width ? height : width;
        this.tileCellLength = shortestCanvasSide / gridLength;

        // init chunks
        let lengthInChunks = gridLength / tilesPerChunk;
        this.chunks = [];
        for (let y = 0; y < lengthInChunks; y++) {
            let rowData = []
            for (let x = 0; x < lengthInChunks; x++) {
                let chunk = new Chunk(x, y);
                chunk.tiles = new Array(tilesPerChunk).fill().map(() => new Array(tilesPerChunk).fill(0))
                rowData.push(chunk);
            }
            this.chunks.push(rowData);
        }
        this.flatChunks = this.chunks.flat()

        // init tiles
        this.tiles = [];
        for (let y = 0; y < gridLength; y++) {
            let rowData = [];
            for (let x = 0; x < gridLength; x++) {
                let tile = new Tile(x, y, this.tileCellLength);
                rowData.push(tile);

                // add to corresponding chunk
                let chunk = this.chunks[floor(y / tilesPerChunk)][floor(x / tilesPerChunk)];
                chunk.tiles[y % tilesPerChunk][x % tilesPerChunk] = tile;
            }
            this.tiles.push(rowData);
        }
        this.flatTiles = this.tiles.flat()

        // terrain stuff
        this.terrainTypes = []

        // pathfinding stuff
        this.startTile = null;
        this.endTile = null;
    }

    addTerrain(name, traverseDifficulty, threshold, colour) {
        this.terrainTypes.push({
            'name': name,
            'difficulty': traverseDifficulty,
            'threshold': threshold,
            'colour': colour
        })

        this.terrainTypes.sort(obj_ => obj_.threshold[0])
    }

    generateTerrain(smoothness) {
        // generate noise and colours
        for (let tile of this.flatTiles) {
            let tileNoise = noise(tile.pos.x / smoothness, tile.pos.y / smoothness);
            for (const terrain of this.terrainTypes) {
                if (tileNoise >= terrain.threshold[0] && tileNoise < terrain.threshold[1]) {
                    tile.terrainName = terrain.name;
                    tile.traverseDifficulty = terrain.difficulty;
                    tile.clr = terrain.colour;
                    break;
                }
            }
        }

        // get chunk overall traverse difficulty
        for (let chunk of this.flatChunks) {
            chunk.totalTraverseDifficulty = 0;
            for (let y = 0; y < this.tilesPerChunk; y++) {
                for (let x = 0; x < this.tilesPerChunk; x++) {
                    chunk.totalTraverseDifficulty += chunk.tiles[y][x].traverseDifficulty
                }
            }
        }
    }

    setStartTile(x, y) {
        // reset
        if (this.start) this.start.isStart = false;

        this.start = this.tiles[y][x];
        this.tiles[y][x].isStart = true;
    }
    setEndTile(x, y) {
        // reset
        if (this.end) this.start.isEnd = false;

        this.end = this.tiles[y][x];
        this.tiles[y][x].isEnd = true;
    }

    pathfindChunks() {
        let openSet = [], closedSet = [];

        // iterate till open set exhausted
        while (openSet.length > 0) {
            let lowestIndex = 0;
            for (let i = 0; i < openSet.length; i++) {
                // checking open set for any index with f value 
                // lower than current lowest index f value
                if (openSet[i].f < openSet[lowestIndex].f) {
                    lowestIndex = i;
                }
            }
            let current = openSet[lowestIndex];

            // if reached end goal, stop
            if (current === end) {
                console.log('DONE');
                noLoop();
            } else {
                // else remove spot from openSet, add to closedSet
                for (let i = openSet.length - 1; i >= 0; i--) {
                    if (openSet[i] === current) openSet.splice(i, 1);
                }
                closedSet.push(current);

                let neighbours = current.neighbours;
                // checking every neighbour
                for (let i = 0; i < neighbours.length; i++) {
                    let neighbour = neighbours[i];

                    // added  && !neighbour.isBlocked to check for obstacle
                    if (!closedSet.includes(neighbour) && !neighbour.isBlocked) {
                        let tempG = current.g + 1;

                        if (openSet.includes(neighbour)) {
                            if (tempG < neighbour.g) {
                                neighbour.g = tempG;
                            }
                        } else {
                            neighbour.g = tempG;
                            openSet.push(neighbour);
                        }
                        // make educated guess from current to end
                        // raw euclidean distance for now
                        neighbour.h = heuristic(neighbour, end);
                        // f(n) = g(n) + h(n)
                        neighbour.f = neighbour.g + neighbour.h;
                        // define previous spot of neighbours; define pathing
                        neighbour.previous = current;
                    }
                }
            }
        }
    }

    showChunks() {
        for (const chunk of this.flatChunks) {
            // get middle of chunk
            let chunkLength = this.tileCellLength * this.tilesPerChunk;
            let chunkCenter = createVector(
                chunk.tiles[0][0].pos.x * this.tileCellLength + chunkLength / 2,
                chunk.tiles[0][0].pos.y * this.tileCellLength + chunkLength / 2
            )

            noFill(); stroke(255, 0, 0); strokeWeight(1.5)
            rect(chunk.tiles[0][0].pos.x * this.tileCellLength, chunk.tiles[0][0].pos.y * this.tileCellLength, chunkLength)
            fill(0, 0, 255, 100); noStroke()
            circle(chunkCenter.x, chunkCenter.y, this.tileCellLength)
        }
    }

    showTiles() {
        noStroke()
        for (const tile of this.flatTiles) {
            // fog of war
            // let d = dist(tile.pos.x * this.tileCellLength, tile.pos.y * this.tileCellLength, mouseX, mouseY)
            // if (d > 300) continue;

            tile.show();
        }

    }
}

class Chunk {
    constructor(x, y) {
        this.pos = createVector(x * x, y * y);
        this.tiles = [];

        // terrain stuff
        this.totalTraverseDifficulty = null;

        // pathfinding stuff
        this.f = 0;
        this.g = 0;
        this.h = 0;
    }
}

class Tile {
    constructor(x, y, cellLength) {
        this.pos = createVector(x, y);
        this.cellLength = cellLength;

        // terrain stuff
        this.terrainName = null;
        this.traverseDifficulty = null;
        this.clr = color(0);

        // pathfinding stuff
        this.isStart = false;
        this.isEnd = false;

        this.f = 0;
        this.g = 0;
        this.h = 0;
    }

    show() {
        fill(this.clr); noStroke()

        // if is start/end
        if (this.isStart) fill(0, 255, 0);
        if (this.isEnd) fill(255, 0, 0);

        rect(this.pos.x * this.cellLength, this.pos.y * this.cellLength, this.cellLength);
    }
}

function _array_mean(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
}