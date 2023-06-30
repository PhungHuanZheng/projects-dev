// https://editor.p5js.org/djuliette/sketches/_qLu82KW5

class Matrix {
    constructor(rows, cols) {
        this._rows = rows;
        this._cols = cols;

        this.data = new Array(rows).fill().map(
            () => new Array(cols).fill(0)
        )
    }

    get shape() { return [this._rows, this._columns]; }

    static fromArray(arr) {
        let M = new Matrix(arr.length, 1)
        M.data = arr.map(v => [v])
        return M
    }

    copy() {
        let M = new Matrix(this._rows, this._cols);
        for (let y = 0; y < this.rows; y++) {
            for (let x = 0; x < this.cols; x++) {
                M.data[y][x] = this.data[y][x];
            }
        }
        return M;
    }

    add(M, inplace = false) {
        // validate input matrix
        if (!(M instanceof Matrix)) throw Error(`Expecting object of type "${this.constructor.name}", got object of type "${M.constructor.name}" instead.`);
        
        if (!inplace) {
            // return a copy

        }
    }

}


new Matrix(2, 2).add(new Matrix(2, 2))