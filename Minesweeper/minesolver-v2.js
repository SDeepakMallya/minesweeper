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
        matrix[i][j] -= val * matrix[r][j];
      }
    }
    lead++;
  }
  return { rref: matrix, piv: pivots };
}

function countVals(row, val) {
  const lim = row.length;
  var count = 0;
  for (var i = 0; i < lim; i++) {
    if (row[i] == val) count++;
  }
  return count;
}

function last(array) {
  return array[array.length - 1];
}

function deleteRow(array, ind) {
  array.splice(ind, 1);
}

function firstPass(state, mines) {
  // Modifies the input arguments
  var rows = state.length;
  var cols = state[0].length;
  var loc = []
  for (var i=0; i < rows; i++) {
    if (mines[i] == 0) {
      // If mines[i] = 0, the locations corresponding to ones are all mine-free.
      for (var j=0; j < cols; j++) {
        if (state[i][j] == 1) {
          loc.push([j, 0]) // Set location j mine-free
          for (var k=0; k<rows; k++) {
            state[k][j] = 0;
          }
        }
      }
      deleteRow(state, i);
      deleteRow(mines, i);
      rows--;
    }
    else if (countVals(state[i], 1) == mines[i]) {
      // If number of ones = mines[i], all the locations corresponding to ones are mines.
      for (var j=0; j < cols; j++) {
        if (state[i][j] == 1) {
          loc.push([j, 1]) // Set a mine at location j
          for (var k=0; k < rows; k++) {
            // if (state[k][j] == 1) mines[k] -= 1;
      mines[k] -= state[k][j];// Update the mine counts
            state[k][j] = 0;
          }
        }
      }
      deleteRow(state, i);
      deleteRow(mines, i);
      rows--;
    }
  }
  return loc;
}

function fastPass(state) {
  var mines = [];
  var rows = state.length;
  var cols = state[0].length - 1;
  for (var  i=0; i < rows; i++) {
    mines.push(state[i].pop());
  }

  var loc = [];
  var pos, neg;
  for (var i=0; i < rows; i++) {
    pos = countVals(state[i], 1); // Counts 1's in the row (>0 since in RREF, leading entry = 1 except for zero rows).
    neg = -countVals(state[i], -1); // Negative of the counts of -1's in the row.
    if (mines[i] == 0) {
      if (neg == 0 & pos > 0) {
        // If neg = 0 and mines[i] = 0, all locations corresponding to 1 are mine-free.
        for (var j=0; j < cols; j++) {
          if (state[i][j] == 1) {
            loc.push([j, 0]) // Set location j mine-free
            for (var k=0; k<rows; k++) {
              state[k][j] = 0;
            }
          }
        }
    // Delete current row and start from Row 0 (May not be necessary)
        deleteRow(state, i);
        deleteRow(mines, i);
        rows--;
        i = 0;
      }
    }
    else {
      if (pos == mines[i]) {
        // When mines != 0, if mines[i] = pos, (Unlikely to happen in RREF)
        // Locations corresponding to 1 are mines and those corresponding to -1 are mine-free.
        for (var j=0; j < cols; j++) {
          if (state[i][j] == 1) {
            loc.push([j, 1]) // Set a mine at location j
            for (var k=0; k < rows; k++) {
              // if (state[k][j] == 1) mines[k] -= 1;
        mines[k] -= state[k][j]; // Update the mine counts
              state[k][j] = 0;
            }
          }
          else if (state[i][j] == -1) {
            loc.push([j, 0]); // Set location j mine-free
            for (var k=0; k < rows; k++) {
              state[k][j] = 0;
            }
          }
        }
        // Delete the current row and start from Row 0 (May not be necessary)
        deleteRow(state, i);
        deleteRow(mines, i);
        rows--;
        i = 0;
      }
      else if (neg == mines[i]) {
        // When mines != 0, if mines[i] = neg, 
        // Locations corresponding to 1 are mines and those corresponding to -1 are mine-free.
        for (var j=0; j < cols; j++) {
          if (state[i][j] == -1) {
            loc.push([j, 1]);
            for (var k=0; k < rows; k++) {
              // if (state[k][j] == 1) mines[k] -= 1;
        mines[k] -= state[k][j];// Update the mine counts
              state[k][j] = 0;
            }
          }
          else if (state[i][j] == 1) {
            loc.push([j, 0]);
            for (var k=0; k < rows; k++) {
              state[k][j] = 0;
            }
          }
        }
        // Delete the current row and start from Row 0 (May not be necessary)
        deleteRow(state, i);
        deleteRow(mines, i);
        rows--;
        i = 0;
      }
    }
  }
  return loc;

}

function sureShot(board, mineCount) {
  var state = clone(board);
  var loc = firstPass(state, mineCount) // Locations of mines from first inspection

  for (var j = 0; j < mineCount.length; j++) {
    state[j].push(mineCount[j]);
  }
  var sol = RREF(state);
  const rref = sol.rref;
  loc = loc.concat(fastPass(state));
  return loc;
}


// Interaction with the  board

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
var alpha = [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
[1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1]]; // Matrix A
var mineCount = [3,3,1,2,1,3,1,3]; // Vector B
var loc = sureShot(alpha, mineCount);
var cells = [[0, 1], [0, 2], [0, 3]]; // (x, y) data of the boundary cells
console.log(loc);

alpha = [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]; // Matrix A (alternate representation of the same board)
mineCount = [3,3,3,1,2,1,3,1];
loc = sureShot(alpha, mineCount);
console.log(loc);
//solveBoard(loc, beta) // Open/Flag the cells
