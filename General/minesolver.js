function clone(nDArray) {
  const len = nDArray.length;
  var copy = new Array(len);
  for (var i=0; i < len; i++) {
    copy[i] = nDArray[i].slice();
  }
  return copy;
}

function RREF(matrix) {
  // Note:  The input matrix is changed
  const rows = matrix.length;
  const columns = matrix[0].length;
  var pivots = [];
  var lead = 0;
  for (var r = 0; r < rows; r++) {
    if (columns <= lead) {
      return { rref: matrix, piv: pivots };
    }
    var i = r;
    while (matrix[i][lead] == 0) {
      i++;
      if (rows == i) {
        i = r;
        lead++;
        if (columns == lead) {
          return { rref: matrix, piv: pivots };
        }
      }
    }
    pivots.push(lead);

    var tmp = matrix[i];
    matrix[i] = matrix[r];
    matrix[r] = tmp;

    var val = matrix[r][lead];
    for (var j = 0; j < columns; j++) {
      matrix[r][j] /= val;
    }

    for (var i = 0; i < rows; i++) {
      if (i == r) continue;
      val = matrix[i][lead];
      for (var j = 0; j < columns; j++) {
        //console.log(j);
        matrix[i][j] -= val * matrix[r][j];
      }
    }
    lead++;
  }
  return { rref: matrix, piv: pivots };
}

function countNonZeros(row) {
  const lim = row.length;
  var count = 0;
  for (var i = 0; i < lim; i++) {
    if (row[i] != 0) count++;
  }
  return count;
}

function last(array) {
  return array[array.length - 1];
}

function sureShot(board, mineCount) {
  var state = clone(board);
  for (var j = 0; j < mineCount.length; j++) {
    state[j].push(mineCount[j]);
  }
  var sol = RREF(state);
  const rref = sol.rref;
  const pivots = sol.piv;
  var loc = [];
  for (var i = 0; i < pivots.length; i++) {
    if (countNonZeros(rref[i].slice(0, -1)) == 1) {
      loc.push([pivots[i], last(rref[i])]);
      //console.log("Location: %d, Mine: " %(pivots[i]), last(rref[i]));
    }
  }
  return loc;

}


// Interacting with the  board

var leftMouseDown = new MouseEvent('mousedown', {
  view: window,
  bubbles: true,
  cancelable: true
});
var leftMouseUp = new MouseEvent('mouseup', {
  view: window,
  bubbles: true,
  cancelable: true
});
var leftMouseEnter = new MouseEvent('mouseenter', {
  view: window,
  bubbles: true,
  cancelable: true
});
var rightMouseDown = new MouseEvent('mousedown', {
  bubbles: true,
  cancelable: false,
  view: window,
  button: 2,
  buttons: 2
});
var rightMouseUp = new MouseEvent('mouseup', {
  bubbles: true,
  cancelable: false,
  view: window,
  button: 2,
  buttons: 0,
});

function idFromPos(x, y) {
	// Works on minesweeperonline.com
	// For minesweeper.online, use cell_id := 
  const cell_id = "#" + document.getElementById(x + "_" + y).id;
  return cell_id;
}

function openCell(x, y) {
  cell_id = idFromPos(x, y);
  $(cell_id)[0].dispatchEvent(leftMouseDown);
  $(cell_id)[0].dispatchEvent(leftMouseUp);
  //$(cell_id)[0].dispatchEvent(simMouseEnter);
  console.log("Open: " + cell_id);
};

function flagCell(x, y) {
  const cell_id = idFromPos(x, y);
  $(cell_id)[0].dispatchEvent(rightMouseDown);
  $(cell_id)[0].dispatchEvent(rightMouseUp);
  console.log("Flag: " + cell_id);
}

function solveBoard(mines, cells) {
  const count = mines.length;
  var x, y, pos;
  for (var i = 0; i < count; i++) {
    pos = mines[i][0]
    x = cells[pos][0];
    y = cells[pos][1]
    if (mines[i][1] == 0) openCell(x, y);
    else flagCell(x, y);
  }
}


// Test Code
var alpha = [[1, 1, 1, 1, 0], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1]]; // Matrix A
var mineCount = [1, 2, 1]; // Vector B
var loc = sureShot(alpha, mineCount);
var cells = [[0, 1], [0, 2], [0, 3]]; // (x, y) data of the boundary cells
solveBoard(loc, beta)


