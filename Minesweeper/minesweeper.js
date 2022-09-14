/*
 * Minesweeper capable of deployed on the browser
 */

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
  // console.log("Open: " + cell_id);
};

function flagCell(x, y) {
  const cell_id = idFromPos(x, y);
  $(cell_id)[0].dispatchEvent(rightMouseDown);
  $(cell_id)[0].dispatchEvent(rightMouseUp);
  // console.log("Flag: " + cell_id);
}


// Set up board and read/update state

function getCellValue(id) {
    const elem = document.getElementById(id);
    const type = elem.getAttribute('class').slice(-1);
    var val;
    if (type == 'd') val = -1;      // Covered cell
    else if (type == 'g') val = -2; // Flagged Cell
    else if (type == 'h') val = -3; // Mine
    else val = parseInt(type);

    return val;
}

function readData(cells, data) {

}


