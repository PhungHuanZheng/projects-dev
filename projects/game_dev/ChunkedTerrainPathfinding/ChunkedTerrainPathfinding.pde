boolean mapEditingEnabled = false;

float mapSeed;
float mapSmoothness;
float regenerationRadius = 1150;

ChunkedTerrainMap map;
ArrayList<Chunk> chunkPath_;
ArrayList<Chunk> chunkPath = new ArrayList<Chunk>();
ArrayList<Tile> tilePath = new ArrayList<Tile>();

void setup() {
    size(1000, 1000);
    mapSeed = random(width << (int)random(height));
    mapSmoothness = 45;

    map = new ChunkedTerrainMap(new Shape(50, 50), 2, true);
    println(String.format("Map Shape: [%d, %d]", map.shapeInTiles.w, map.shapeInTiles.h));
    println(String.format("Canvas Shape: [%d, %d]", ceil(map.shapeInTiles.w * map.tileLength) + 1, ceil(map.shapeInTiles.h * map.tileLength) + 1));

    // add terrain types to generate
    map.addTerrain("deepWater", 25, new float[]{0, 0.4}, color(6, 66, 115));
    map.addTerrain("water", 10, new float[]{0.4, 0.43}, color(29, 162, 216));
    map.addTerrain("shallowWater", 5, new float[]{0.43, 0.45}, color(168, 216, 189));
    map.addTerrain("sandBank", 3, new float[]{0.45, 0.47}, color(231, 196, 150));
    map.addTerrain("plains", 1, new float[]{0.47, 0.57}, color(98, 188, 47));
    map.addTerrain("marsh", 2, new float[]{0.57, 0.63}, color(138, 133, 40));
    map.addTerrain("mountainFoot", 3, new float[]{0.63, 0.7}, color(131, 106, 68));
    map.addTerrain("mountainLow", 5, new float[]{0.7, 0.74}, color(54, 46, 28));
    map.addTerrain("mountainHigh", 8, new float[]{0.74, 0.81}, color(38, 36, 36));
    map.addTerrain("mountainVeryHigh", 11, new float[]{0.81, 0.85}, color(12, 14, 13));
    map.addTerrain("mountainPeak", 20, new float[]{0.85, 0.9}, color(185, 195, 205));
    map.addTerrain("mountainSnowPeak", 30, new float[]{0.9, 1}, color(255, 250, 250));

    //map.generateTerrain(random(millis() << 23), 45);
    map.generateTerrain(mapSeed, mapSmoothness);
    println(String.format("Map Seed: %d | Map Smoothness: %d", (int)mapSeed, (int)mapSmoothness));

    windowResize(ceil(map.shapeInTiles.w * map.tileLength) + 1, ceil(map.shapeInTiles.h * map.tileLength) + 1);
    map.show(true); // true, false

    // init start and end tiles
    Tile startTile = map.tileAt(0, 0);
    Tile endTile = map.tileAt(map.shapeInTiles.w - 1, map.shapeInTiles.h - 1);

    // do chunk-wise pathfinding and reverse
    chunkPath_ = map.pathfindChunks(startTile, endTile);
    for (int i = chunkPath_.size() - 1; i >= 0; i--) {
        chunkPath.add(chunkPath_.get(i));
    }

    //init neighbours only for chunks in path
    for (int i = 0; i < chunkPath.size() - 1; i++) {
        Chunk nextChunk = chunkPath.get(i + 1);
        Chunk chunk = chunkPath.get(i);

        Tile[] chunkBorder = null;
        Tile[] nextChunkBorder = null;

        // find side of next chunk that's connected to current chunk
        if (nextChunk.pos.x - chunk.pos.x == 1) {
            // if next is on the right
            chunkBorder = chunk.getColumn(chunk.chunkShape.w - 1);
            nextChunkBorder = nextChunk.getColumn(0);
        } else if (nextChunk.pos.x - chunk.pos.x == -1) {
            // if next is on the left
            chunkBorder = chunk.getColumn(0);
            nextChunkBorder = nextChunk.getColumn(nextChunk.chunkShape.w - 1);
        } else if (nextChunk.pos.y - chunk.pos.y == 1) {
            // if next is on the bottom
            chunkBorder = chunk.getRow(chunk.chunkShape.h - 1);
            nextChunkBorder = nextChunk.getRow(0);
        } else if (nextChunk.pos.y - chunk.pos.y == -1) {
            // if next is on the top
            chunkBorder = chunk.getRow(0);
            nextChunkBorder = nextChunk.getRow(nextChunk.chunkShape.h - 1);
        }

        // find pair of tiles between associative arrays with lowest sum
        double minTileSum = Double.POSITIVE_INFINITY;
        Tile minChunkTile = null;
        Tile minNextChunkTile = null;
        for (int j = 0; j < chunkBorder.length; j++) {
            float tileSum = chunkBorder[j].traverseDifficulty + nextChunkBorder[j].traverseDifficulty;
            tileSum += abs(chunkBorder[j].globalPos.x - endTile.globalPos.x) + abs(chunkBorder[j].globalPos.y - endTile.globalPos.y);
            tileSum += abs(nextChunkBorder[j].globalPos.x - endTile.globalPos.x) + abs(nextChunkBorder[j].globalPos.y - endTile.globalPos.y);

            if (tileSum < minTileSum) {
                minTileSum = tileSum;
                minChunkTile = chunkBorder[j];
                minNextChunkTile = nextChunkBorder[j];
            }
        }
        chunk.endTile = minChunkTile;
        nextChunk.startTile = minNextChunkTile;
    }

    // init start and end tiles in their respective chunks
    map.chunkWith(startTile).startTile = startTile;
    map.chunkWith(endTile).endTile = endTile;

    for (Chunk chunk : chunkPath) {
        chunk.initNeighbours();
        ArrayList<Tile> chunkTilePath = chunk.pathfindTiles();

        for (Tile tile : chunkTilePath) {
            tile.clr = color(255);
        }
    }
}


void draw() {
    //background(0);
    //println(frameRate);
    map.show(false); // true, false

    for (int i = 0; i < chunkPath.size(); i++) {
        Chunk chunk = chunkPath.get(i);
        fill(255, 255, 255, 100);
        noStroke();
        rect(
            chunk.pos.x * chunk.chunkShape.w * chunk.tileLength,
            chunk.pos.y * chunk.chunkShape.h * chunk.tileLength,
            chunk.chunkShape.w * chunk.tileLength, chunk.chunkShape.h * chunk.tileLength
            );
    }

    if (mousePressed && mapEditingEnabled) {
        //store tiles to be changed
        ArrayList<Tile> tilesChanged = new ArrayList<Tile>();

        // iterate over tiles in map
        for (int y = 0; y < map.shapeInTiles.h; y++) {
            for (int x = 0; x < map.shapeInTiles.w; x++) {
                Tile tile = map.tileAt(x, y);

                // if close enough to mouse
                float d = dist(mouseX, mouseY, tile.globalPos.x * map.tileLength, tile.globalPos.y * map.tileLength);
                if (d < regenerationRadius && !tile.wasTerraformed) {
                    tilesChanged.add(tile);
                    tile.wasTerraformed = true;
                }
            }
        }

        //regenerate terrain for those tiles
        Tile[] tilesChangedArr = new Tile[tilesChanged.size()];
        tilesChangedArr = tilesChanged.toArray(tilesChangedArr);
        map.regenerateTerrainAt(tilesChangedArr, mapSeed, mapSmoothness, regenerationRadius, "depress");
    }
}

void mouseReleased() {
    // iterate over tiles in map
    for (int y = 0; y < map.shapeInTiles.h; y++) {
        for (int x = 0; x < map.shapeInTiles.w; x++) {
            map.tileAt(x, y).wasTerraformed = false;
        }
    }
}
