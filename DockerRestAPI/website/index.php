<html>
    <head>
        <title>CIS 322 REST-api project 6: Brevet Calc</title>
    </head>

    <body>
        <h1>Open and Close Times in Database</h1>
        <ul>
            <?php
            $json = file_get_contents('http://web/listall');
            $obj = json_decode($json);
	          $open_times = $obj->open_times;
	    	  $close_times = $obj->close_times;
	    echo "Open times:";
            foreach ($open_times as $l) {
                echo "<li>$l</li>";
	    }
            echo "<br>";
	    echo "Close times:";
            foreach ($close_times as $l) {
                echo "<li>$l</li>";
	    }
            ?>
        </ul>
    </body>
</html>
