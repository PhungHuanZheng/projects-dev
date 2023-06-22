class PipeCell {
    directions = ['N', 'W', 'S', 'E']

    constructor(x, y) {
        this.pos = { x, y };
        this.facing_dirs = [];

        // get pipe directions
        let dir_count = floor(random(1, 5))
        console.log(dir_count)
    }
}