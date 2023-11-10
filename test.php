<!DOCTYPE html>
<html>
    <head>
        <title>PHP Test</title>
    </head>
    <body>
        <?php echo '<p>Hello World</p>'; ?>
        <br>
        <?php
        $queries = array();
        parse_str($_SERVER['QUERY_STRING'], $queries);
        echo $queries['tester']; ?>
    </body>
</html>
