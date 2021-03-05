/* file: api.js
 *
 * purpose: provide common functions for multiple pages in qteller
 *
 * history:
 *  06/29/18  jportwood - created
 */

function alert_test() {
  alert("Test0");
}


/**
 *  Iterates through all elements grouped under a class and sets their checked value to true or false
 *
 * @param classID - the ID of the class
 * @param checked - whether the box will be checked, must be either a boolean true or false
 */
function check_all_boxes(classID, checked) {
    var elems = document.getElementsByClassName(classID);
    Array.from(elems).forEach(function (elem) {
        elem.checked = checked;
    });
}