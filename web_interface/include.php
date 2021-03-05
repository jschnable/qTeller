<?php
/* file: include.php
 *
 * purpose: provide common functions for multiple pages in qteller
 *
 * history:
 *  06/29/18  jportwood - created
 */

 /**
  * For debugging
  */
function dump($var) {
    echo "<pre>";
    var_dump($var);
    echo "</pre>";
}

/**
 * Returns a class identifier to group all the checkboxes from each source together
 */
function translateClass($source) {
    switch (true) {
        case stristr($source, 'Stelpflug 2015'):
            return "stelp2015";
        case stristr($source, 'Kakumanu 2012'):
            return "kaku2012";
        case stristr($source, 'Johnston 2014'):
            return "john2014";
        case stristr($source, 'Forestan 2016'):
            return "forest2016";
        case stristr($source, 'Waters 2017'):
            return "waters2017";
        case stristr($source, 'Walley 2016'):
            return "walley2016";
	case stristr($source, 'Lin 2017'):
            return "lin2017";
	case stristr($source, 'Nam Consortium'):
            return "namconsortium";

    }
}

?>
