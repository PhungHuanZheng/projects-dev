class SquareChunkGrid {
    constructor(tilesPerSide, tilesPerChunkSide) {
        // check params
        if (tilesPerSide % tilesPerChunkSide !== 0)
            throw new Error(`Parameter 'tilesPerSide' must be divisible by 'tilesPerChunkSide' passed, got remainder of ${tilesPerSide % tilesPerChunkSide}.`)

        // basic init setup
        this.tilesPerSide = tilesPerSide;
        this.tilesPerChunkSide = tilesPerChunkSide;
        this.chunksPerSide = tilesPerSide / tilesPerChunkSide;

        // canvas display
        let shorterSide = height < width ? height : width;
        this.tileLength = shorterSide / this.tilesPerSide;

        // init chunks
        this.chunks = [];
        for (let y = 0; y < this.chunksPerSide; y++) {
            let rowData = [];
            for (let x = 0; x < this.chunksPerSide; x++) {
                // init new chunk and its tiles
                rowData.push(new _Chunk(x, y, tilesPerChunkSide, this.tileLength))
            }
            this.chunks.push(rowData)
        }

        // convenient tile iteration access
        this.tiles = [];
        for (let chunk of this.chunks.flat()) {
            for (let tile of chunk.tiles.flat()) {
                this.tiles.push(tile);
            }
        }

        // terrain storage
        this.terrainTypes = []
    }

    getTile(x, y) {
        let tileChunk = this.chunks[floor(y / this.tilesPerChunkSide)][floor(x / this.tilesPerChunkSide)]
        return tileChunk.tiles[floor(y % tileChunk.tilesPerSide)][floor(x % tileChunk.tilesPerSide)]
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
        for (let tile of this.tiles) {
            let tileNoise = noise(tile.gridPos.x / smoothness, tile.gridPos.y / smoothness);
            for (const terrain of this.terrainTypes) {
                if (tileNoise >= terrain.threshold[0] && tileNoise < terrain.threshold[1]) {
                    tile.terrainName = terrain.name;
                    tile.traverseDifficulty = terrain.difficulty;
                    tile.clr = terrain.colour;
                    break;
                }
            }
        }
    }

    initNeighbours() {
        // iterate over grid
        for (let yC = 0; yC < this.chunksPerSide; yC++) {
            for (let xC = 0; xC < this.chunksPerSide; xC++) {
                let chunk = this.chunks[yC][xC];

                // iterate over relativve positions
                for (let [j, i] of [[-1, 0], [0, -1], [1, 0], [0, 1]]) {
                    if (!this.chunks[yC + j] || !this.chunks[yC + j][xC + i]) continue;

                    // add to chunk neighbours
                    chunk.neighbours.push(this.chunks[yC + j][xC + i]);
                }

                // iterate over tiles in chunk
                for (let yT = 0; yT < chunk.tilesPerSide; yT++) {
                    for (let xT = 0; xT < chunk.tilesPerSide; xT++) {
                        let tile = chunk.tiles[yT][xT]

                        // iterate over relativve positions
                        for (let [j, i] of [[-1, 0], [0, -1], [1, 0], [0, 1]]) {
                            if (!chunk.tiles[yT + j] || !chunk.tiles[yT + j][xT + i]) continue;

                            // add to chunk neighbours
                            tile.neighbours.push(chunk.tiles[yT + j][xT + i]);
                        }
                    }
                }
            }
        }
    }

    pathfindChunks() {
        let openSet = [], closedSet = [];
        openSet.push()
    }

    show(drawChunks) {
        for (let tile of this.tiles) {
            // draw tile
            noStroke()

            if (tile.isStart) { fill(0, 255, 0); stroke(255) }
            else if (tile.isEnd) { fill(255, 0, 0); stroke(255) }
            else fill(tile.clr);

            rect(tile.gridPos.x * this.tileLength, tile.gridPos.y * this.tileLength, this.tileLength);
        }

        if (drawChunks) {
            for (let y = 0; y < this.chunksPerSide; y++) {
                for (let x = 0; x < this.chunksPerSide; x++) {
                    let chunk = this.chunks[y][x]

                    // draw bounding box
                    noFill(); stroke(255, 0, 0); strokeWeight(1.25);
                    let chunkLength = chunk.tilesPerSide * this.tileLength;
                    rect(chunk.pos.x * chunkLength, chunk.pos.y * chunkLength, chunkLength);

                    // draw marker
                    fill(0, 0, 255, 100); noStroke();
                    circle(chunk.pos.x * chunkLength + chunkLength / 2, chunk.pos.y * chunkLength + chunkLength / 2, 10)
                }
            }
        }
    }
}

class _Chunk {
    constructor(x, y, tilesPerSide, tileLength) {
        this.pos = createVector(x, y);
        this.tilesPerSide = tilesPerSide;

        // init tiles
        this.tiles = []
        for (let y = 0; y < tilesPerSide; y++) {
            let rowData = [];
            for (let x = 0; x < tilesPerSide; x++) {
                rowData.push(new _Tile(x, y, tileLength, this))
            }
            this.tiles.push(rowData)
        }

        // neighbours
        this.neighbours = [];
        this.isStart = false;
        this.isEnd = false;
    }
}

class _Tile {
    constructor(x, y, tileLength, chunk) {
        this.chunk = chunk;
        this.chunkPos = createVector(x, y);
        this.gridPos = createVector(chunk.pos.x * chunk.tilesPerSide + x, chunk.pos.y * chunk.tilesPerSide + y);
        this.tileLength = tileLength;

        this.clr = color(0);
        this.terrainName = null;
        this.traverseDifficulty = null;

        this.neighbours = []
        this.isStart = false;
        this.isEnd = false;
    }
}