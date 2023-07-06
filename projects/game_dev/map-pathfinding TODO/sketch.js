let grid;
let mapSeed;


function setup() {
    createCanvas(windowWidth, windowHeight);
    frameRate(30);

    if (!mapSeed) {
        mapSeed = generateRandomSeed([new Date().getMilliseconds() << 32, new Date().getMilliseconds() << 23]);
    }
    noiseSeed(mapSeed);
    console.log(`Map Seed: ${mapSeed}`)


    grid = new SquareChunkGrid(90, 5)

    grid.addTerrain('deepWater', 50, [0, 0.25], color(28, 163, 236));
    grid.addTerrain('water', 20, [0.25, 0.3], color(28, 163, 150));
    grid.addTerrain('waterEdge', 2.5, [0.3, 0.34], color(246, 215, 176));
    grid.addTerrain('plains', 1, [0.34, 0.57], color(98, 188, 47));
    grid.addTerrain('marsh', 1.5, [0.57, 0.65], color(138, 133, 40));
    grid.addTerrain('mountainEdge', 2.5, [0.65, 0.68], color(101, 83, 83));
    grid.addTerrain('mountain', 5, [0.68, 0.8], color(155, 118, 83));
    grid.addTerrain('mountainPeak', 10, [0.8, 1], color(127, 131, 134));

    grid.generateTerrain(30);

    // set start and end tiles
    let startTile = grid.getTile(floor(random(grid.tilesPerSide)), floor(random(grid.tilesPerSide)))
    startTile.isStart = true;
    startTile.chunk.isStart = true;

    let endTile = grid.getTile(floor(random(grid.tilesPerSide)), floor(random(grid.tilesPerSide)))
    endTile.isEnd = true;
    endTile.chunk.isEnd = true;

    createCanvas(grid.tilesPerSide * grid.tileLength, grid.tilesPerSide * grid.tileLength);
}

function draw() {
    background(0);

    // grid.pathfindChunks()
    grid.show(false)
    // grid.showChunks()

    // noLoop()
}

function generateRandomSeed(state) {
    let t = state[0];
    let s = state[1];
    state[0] = s;
    t ^= t << 23;		// a
    t ^= t >> 18;		// b -- Again, the shifts and the multipliers are tunable
    t ^= s ^ (s >> 5);	// c
    state[1] = t;
    return t + s;
}